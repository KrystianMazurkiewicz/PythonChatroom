import socket
import threading



# below are some constant variables.
# one of the "SERVER" variables are commented out. If the server does not work on localhost for whatever reason, 
# then the other "SERVER" variable can be used. In that case that variable has to also change on the client side.
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "localhost"
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "dc"

# we create a socket.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# we connect socket to defined server and port, aka to specific address (ADDR).
client.connect(ADDR)



# this send function sends messages from client the destination it is connected to.
def send(message):
    message = message.encode(FORMAT)
    client.send(message)
   


# this function recieves messages from whatever it is connected to and decodes the encoded message.
def recieve_message():
    while True:
        message = client.recv(2048).decode(FORMAT)
        print(message)



# this message_constructor function prepares the message that is about to send.
# it also checks if the client wants to disconnect
def message_constructor():
    connected = True
    while connected:
        message = input()
        send(message)
        if message == "dc":
            connected = False



# a thread that gives some of CPUs focus to recieve_message function
recive_thread = threading.Thread(target=recieve_message)
recive_thread.start()

# a thread that gives some of CPUs focus to message_constructor function
start_thread = threading.Thread(target=message_constructor)
start_thread.start()
