import pika
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import os

user = os.getenv("RABBITMQ_USERNAME")
password = os.getenv("RABBITMQ_PASSWORD")

# RabbitMQ server credentials
credentials = pika.PlainCredentials(user, password)
parameters = pika.ConnectionParameters('192.168.17.142', 5672, '/', credentials)

# Establishing connection with RabbitMQ server
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Ensure that the queue exists
channel.queue_declare(queue='hello')

# Load private key
with open('private_key.pem', 'rb') as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

# Load other user's public key
with open('reciever/public_key.pem', 'rb') as key_file:
    other_user_public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

# Define a callback function for processing incoming messages
def callback(ch, method, properties, body):
    decrypted_message = decrypt_message(body, private_key)
    received_messages.insert(tk.END, f"{decrypted_message}\n")

# Tell RabbitMQ that this callback function should receive messages from our 'hello' queue
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

def receive_messages():
    # Non-blocking start to consuming messages
    channel.start_consuming()

def encrypt_message(message, public_key):
    ciphertext = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=padding.SHA256()),
            algorithm=padding.SHA256(),
            label=None
        )
    )

    return ciphertext

def decrypt_message(ciphertext, private_key):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=padding.SHA256()),
            algorithm=padding.SHA256(),
            label=None
        )
    )

    return plaintext.decode('utf-8')

def send_message(message):
    encrypted_message = encrypt_message(message, other_user_public_key)
    channel.basic_publish(exchange='', routing_key='hello', body=encrypted_message)

# Start a thread for receiving messages
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

# Get the username
user = os.getenv("RABBITMQ_USERNAME")

# Create the main window
root = tk.Tk()
root.title("Chat")
root.geometry("1000x600")  # Set the initial size of the window

# Set the background color to plum2
root.configure(bg="plum2")

# Create a label to display the welcome message
welcome_label = tk.Label(root, text=f"Welcome to the chat, {user}!", font=("Arial", 16), bg="plum2", padx=10, pady=10)
welcome_label.grid(row=0, column=0, columnspan=2)

# Create a scrolled text widget to display received messages
received_messages = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
received_messages.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

# Create an entry widget to type messages
message_entry = tk.Entry(root, width=50)
message_entry.grid(row=2, column=0, padx=10, pady=10)

# Create a button to send messages
def send_message_clicked():
    message = message_entry.get()
    if message.lower() == 'exit':
        root.destroy()  # Close the window if the user types "exit"
    else:
        message_entry.delete(0, tk.END)  # Clear the entry after sending the message
        send_message(message)

send_button = tk.Button(root, text="Send", command=send_message_clicked)
send_button.grid(row=2, column=1, padx=10, pady=10)

# Load the image (resize it if needed)
image_path = "chat.png"  # Change this to the path of your image
if tk.PhotoImage(file=image_path):  # Check if the image file is valid
    img = tk.PhotoImage(file=image_path)
    img = img.subsample(4)  # Resize the image by a factor of 4
    tk.Label(root, image=img, bg="plum2").grid(row=0, column=2, rowspan=2, padx=10, pady=10)

# Run the GUI main loop
root.mainloop()

# Stop consuming and close the connection when the GUI is closed
channel.stop_consuming()
connection.close()
