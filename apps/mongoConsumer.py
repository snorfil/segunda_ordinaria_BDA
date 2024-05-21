from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, StructField

def consumir_datos_de_kafka():


    spark = SparkSession.builder \
        .appName("mongo consumer") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .config("spark.sql.shuffle.partitions", "2") \
        .config("spark.jars", "opt/spark-apps/drivers/spark-sql-kafka-0-10_2.12-3.2.0.jar,opt/spark-apps/drivers/spark-token-provider-kafka-0-10_2.12-3.2.0.jar") \
        .config("spark.driver.extraClassPath", "/opt/spark-apps/drivers/spark-sql-kafka-0-10_2.12-3.2.0.jar") \
        .config("spark.executor.extraClassPath", "/opt/spark-apps/drivers/spark-sql-kafka-0-10_2.12-3.2.0.jar") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    # Definir el esquema de los datos
    esquema = StructType([
        StructField("id_cliente", StringType(), True),
        StructField("nombre", StringType(), True),
        StructField("direccion", StringType(), True),
        StructField("preferencias_alimenticias", StringType(), True)
    ])

    #Leer los datos de Kafka
    df_kafka = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "clientes_stream") \
        .load()

    # Convertir los datos del formato JSON
    df_valores = df_kafka.selectExpr("CAST(value AS STRING)")
    df_datos = df_valores.select(from_json(col("value"), esquema).alias("data")).select("data.*")

    # Procesar los datos
    query = df_datos.writeStream \
        .format("console") \
        .outputMode("append") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    consumir_datos_de_kafka()
