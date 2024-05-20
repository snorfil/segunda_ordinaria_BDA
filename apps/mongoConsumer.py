from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

def consumir_datos_de_kafka():
    # Crear una sesión de Spark
    spark = SparkSession.builder \
        .appName("KafkaMongoConsumer") \
        .config("spark.sql.shuffle.partitions", "2") \
        .getOrCreate()

    # Definir el esquema de los datos
    esquema = StructType([
        StructField("ID", StringType(), True),
        StructField("nombre", StringType(), True),
        StructField("direccion", StringType(), True),
        StructField("preferencias_dieteticas", StringType(), True)
    ])

    # Leer los datos de Kafka
    df_kafka = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "clientes_stream") \
        .option("startingOffsets", "earliest") \
        .load()

    # Convertir los datos del formato JSON
    df_valores = df_kafka.selectExpr("CAST(value AS STRING)")
    df_datos = df_valores.select(from_json(col("value"), esquema).alias("data")).select("data.*")

    # Procesar los datos (aquí puedes agregar transformaciones adicionales)
    df_datos.writeStream \
        .format("console") \
        .outputMode("append") \
        .start() \
        .awaitTermination()

if __name__ == "__main__":
    consumir_datos_de_kafka()
