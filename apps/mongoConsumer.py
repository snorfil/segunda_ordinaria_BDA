from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, StructField

def consumir_datos_de_kafka():
    aws_access_key_id = 'test'
    aws_secret_access_key = 'test'

    spark = SparkSession.builder \
        .appName("Streaming from Kafka") \
        .config("spark.streaming.stopGracefullyOnShutdown", True) \
        .config("spark.sql.shuffle.partitions", 4) \
        .config("spark.hadoop.fs.s3a.endpoint", "http://spark-localstack-1:4566") \
        .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
        .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
        .config("spark.jars", "file:///opt/spark/jars/spark-sql-kafka-0-10_2.12-3.2.0.jar,file:///opt/spark/jars/spark-token-provider-kafka-0-10_2.12-3.2.0.jar") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    # Definir el esquema de los datos
    esquema = StructType([
        StructField("ID", StringType(), True),
        StructField("nombre", StringType(), True),
        StructField("direccion", StringType(), True),
        StructField("preferencias_dieteticas", StringType(), True)
    ])


    df_kafka = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "clientes_stream") \
        .option("startingOffsets", "earliest") \
        .load()

    # Convertir los datos del formato JSON
    df_valores = df_kafka.selectExpr("CAST(value AS STRING)")
    df_datos = df_valores.select(from_json(col("value"), esquema).alias("data")).select("data.*")

    # Procesar los datos (aquí puedes agregar transformaciones adicionales)
    query = df_datos.writeStream \
        .format("console") \
        .outputMode("append") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    consumir_datos_de_kafka()
