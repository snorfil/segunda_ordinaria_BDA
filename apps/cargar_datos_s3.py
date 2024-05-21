from pyspark.sql import SparkSession
import sys

aws_access_key_id = 'test'
aws_secret_access_key = 'test'
ruta_restaurantes = "/opt/spark-data/json/restaurantes.json"
ruta_habitaciones = "/opt/spark-data/csv/habitaciones.csv"


def cargar_datos_a_s3(bucket_name):
    spark = SparkSession.builder \
        .appName("SPARK S3") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
        .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
        .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.jars.packages",
                "org.apache.spark:spark-hadoop-cloud_2.13:3.5.1,software.amazon.awssdk:s3:2.25.11") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.driver.extraClassPath", "/opt/spark/jars/s3-2.25.11.jar") \
        .config("spark.executor.extraClassPath", "/opt/spark/jars/s3-2.25.11.jar") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    try:
        df3 = spark.read.option("delimiter", ",").option("header", True).csv(ruta_habitaciones)
        df3 \
            .write \
            .option('fs.s3a.committer.name', 'partitioned') \
            .option('fs.s3a.committer.staging.conflict-mode', 'replace') \
            .option("fs.s3a.fast.upload.buffer", "bytebuffer") \
            .mode('overwrite') \
            .csv(path=f's3a://{bucket_name}/habitaciones.csv', sep=',')
    except:
        spark.stop()

    spark.stop()
    # Ruta a los archivos locales

    # df_restaurantes = spark.read.json(ruta_restaurantes)
    # print("X"*50)
    #
    # df_restaurantes.show()
    # print("X"*50)
    #
    # # Mostrar registros corruptos si existen
    # df_restaurantes.filter(df_restaurantes["_corrupt_record"].isNotNull()).show(truncate=False)
    # # Cargar el archivo JSON
    # df_restaurantes = spark.read.json(ruta_restaurantes)
    # print(df_restaurantes)
    #
    # # Cargar el archivo CSV
    # df_habitaciones = spark.read.csv(ruta_habitaciones, header=True, inferSchema=True)
    # print(df_habitaciones)
    # print("X"*50)
    #
    #
    # # Especificar la ruta S3
    # ruta_s3_restaurantes = f"s3a://{bucket_name}/restaurantes/"
    # ruta_s3_habitaciones = f"s3a://{bucket_name}/habitaciones/"
    #
    # # Guardar los DataFrames en S3
    # df_restaurantes.write.mode("overwrite").json(ruta_s3_restaurantes)
    # df_habitaciones.write.mode("overwrite").csv(ruta_s3_habitaciones)
    #
    # print(f"Archivos cargados exitosamente a {bucket_name}")
    #
    # spark.stop()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: cargar_datos_s3.py <nombre_bucket>")
        sys.exit(1)

    nombre_bucket = sys.argv[1]
    cargar_datos_a_s3(nombre_bucket)
