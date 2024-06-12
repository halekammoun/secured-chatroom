import pika

# RabbitMQ server address and credentials
rabbitmq_address = '192.168.17.142'
rabbitmq_port = 15672
rabbitmq_username = 'guest'
rabbitmq_password = 'guest'

# Connection parameters
credentials = pika.PlainCredentials(username=rabbitmq_username, password=rabbitmq_password)
connection_params = pika.ConnectionParameters(host=rabbitmq_address, port=rabbitmq_port, credentials=credentials)

# Establish connection
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare a queue
queue_name = 'test_queue'
channel.queue_declare(queue=queue_name)

# Send a message
message_to_send = 'Hello, RabbitMQ!'
channel.basic_publish(exchange='', routing_key=queue_name, body=message_to_send)
print(f" [x] Sent '{message_to_send}'")

# Define a callback function for receiving messages
def callback(ch, method, properties, body):
    print(f" [x] Received '{body}'")

# Set up a consumer
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# Start consuming (this will block the script)
print(' [*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()

