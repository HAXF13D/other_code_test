import pika
import time


def connect_with_retry():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
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
