# from kafka import KafkaConsumer
#
# # Set up Kafka consumer
# consumer = KafkaConsumer(
#     'sales_stream',                       # Topic to subscribe to
#     bootstrap_servers=['kafka:9092'], # Kafka broker(s)
#     auto_offset_reset='earliest',        # Start from earliest message
#     enable_auto_commit=True,             # Commit offsets automatically
#     value_deserializer=lambda x: x.decode('utf-8')
# )
#
#
# for message in consumer:
#     print(f"Received message: {message.value}")
#
# consumer.close()
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'clientes_stream',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='my-group'
)

for message in consumer:
    print(f"Received message: {message.value.decode('utf-8')}")
