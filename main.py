from database.aws_localstack.bucket_create import crear_bucket
from database.mongodb.mongoInsert import insertar_datos_mongodb

crear_bucket("hotel")

insertar_datos_mongodb()

