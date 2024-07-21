import pika
import time
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_LOG_FILE = BASE_DIR / 'app.log'


def setup_logger(log_file=DEFAULT_LOG_FILE):
    file_log = logging.FileHandler(log_file)
    console_out = logging.StreamHandler()

    logging.basicConfig(
        handlers=(file_log, console_out),
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)
    return logger


logger = setup_logger()


def write_log(message):
    logger.info(message)


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


def consumer():
    def callback(ch, method, properties, body):
        message = body.decode('utf-8')
        if "red" in message.lower():
            write_log(message)

    channel.basic_consume(
        queue='fast_api_queue',
        on_message_callback=callback,
        auto_ack=True
    )

    print('Waiting for messages')

    channel.start_consuming()


if __name__ == "__main__":
    consumer()
