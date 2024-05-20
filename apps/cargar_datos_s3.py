from pyspark.sql import SparkSession
import sys

aws_access_key_id = 'test'
aws_secret_access_key = 'test'

def cargar_datos_a_s3(bucket_name):

    # Crear una sesión de Spark
    spark = SparkSession.builder \
        .appName("SPARK S3") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://tema5-localstack-1:4566") \
        .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
        .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.jars.packages", "org.apache.spark:spark-hadoop-cloud_2.13:3.5.1,software.amazon.awssdk:s3:2.25.11") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.driver.extraClassPath", "/opt/spark/jars/s3-2.25.11.jar") \
        .config("spark.executor.extraClassPath", "/opt/spark/jars/s3-2.25.11.jar") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    # Ruta a los archivos locales
    ruta_restaurantes = "/opt/spark-data/restaurantes.json"
    ruta_habitaciones = "/opt/spark-data/habitaciones.csv"

    # Cargar el archivo JSON
    df_restaurantes = spark.read.json(ruta_restaurantes)

    # Cargar el archivo CSV
    df_habitaciones = spark.read.csv(ruta_habitaciones, header=True, inferSchema=True)

    # Especificar la ruta S3
    ruta_s3_restaurantes = f"s3a://{bucket_name}/restaurantes/"
    ruta_s3_habitaciones = f"s3a://{bucket_name}/habitaciones/"

    # Guardar los DataFrames en S3
    df_restaurantes.write.mode("overwrite").json(ruta_s3_restaurantes)
    df_habitaciones.write.mode("overwrite").csv(ruta_s3_habitaciones)

    print(f"Archivos cargados exitosamente a {bucket_name}")

    # Cerrar la sesión de Spark
    spark.stop()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: cargar_datos_s3.py <nombre_bucket>")
        sys.exit(1)

    nombre_bucket = sys.argv[1]
    cargar_datos_a_s3(nombre_bucket)
