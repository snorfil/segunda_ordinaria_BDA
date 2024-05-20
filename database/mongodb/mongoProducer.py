from pymongo import MongoClient
from kafka import KafkaProducer
import json
import time

def enviar_datos_a_kafka(intervalo):
    # Conexión a MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['bda']
    collection = db['clientes']

    # Conexión a Kafka
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    total_docs = collection.count_documents({})
    current_index = 0

    while True:
        # Leer el documento actual desde MongoDB
        cliente = collection.find().skip(current_index).limit(1)
        for doc in cliente:
            # Enviar el dato a Kafka
            producer.send('clientes_stream', doc)
            producer.flush()
            print(f"Datos enviados exitosamente a Kafka: {doc}")

        # Incrementar el índice y reiniciarlo si alcanzamos el final
        current_index += 1
        if current_index >= total_docs:
            current_index = 0

        # Esperar el intervalo especificado antes de enviar el siguiente dato
        time.sleep(intervalo)


if __name__ == "__main__":
    # tiempo en segundos
    intervalo = 5
    enviar_datos_a_kafka(intervalo)
