import pika
import time


def connect_with_retry():
    while True:
        try:
            connection_params = pika.ConnectionParameters(
                host='rabbitmq',
                heartbeat=600,  # Установите более длительный интервал сердечных сигналов, например, 600 секунд
                blocked_connection_timeout=300  # Установите таймаут блокировки соединения, например, 300 секунд
            )
            connection = pika.BlockingConnection(connection_params)
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("Connection failed, retrying in 5 seconds...")
            time.sleep(5)


connection = connect_with_retry()
channel = connection.channel()

channel.queue_declare(queue='fast_api_queue')


def enqueue_message(message):
    channel.basic_publish(
        exchange='',
        routing_key='fast_api_queue',
        body=message.encode('utf-8')
    )
