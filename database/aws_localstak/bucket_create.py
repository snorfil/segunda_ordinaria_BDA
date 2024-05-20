import boto3
import argparse
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def crear_bucket(nombre_bucket,region=None):
    try:
        cliente_s3 = boto3.client(
            's3',
            endpoint_url='http://localhost:4566',  # LocalStack endpoint URL
            aws_access_key_id='test',  # dummy access key (LocalStack default)
            aws_secret_access_key='test',  # dummy secret key (LocalStack default)
        )
        if region is None:
            cliente_s3.create_bucket(Bucket=nombre_bucket)
        else:
            ubicacion = {'LocationConstraint': region}
            cliente_s3.create_bucket(Bucket=nombre_bucket, CreateBucketConfiguration=ubicacion)
        print(f"Bucket '{nombre_bucket}' creado exitosamente.")
    except (NoCredentialsError, PartialCredentialsError):
        print("Credenciales no disponibles.")
    except Exception as e:
        print(f"Ocurrió un error al crear el bucket: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crear un bucket en S3.")
    parser.add_argument("nombre_bucket", type=str, help="El nombre del bucket a crear.")
    parser.add_argument("--region", type=str, default=None, help="La región de AWS donde se creará el bucket.")

    args = parser.parse_args()

    crear_bucket(args.nombre_bucket, args.region)
