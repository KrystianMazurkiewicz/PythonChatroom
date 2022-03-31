import socket 
import threading
import random
import time



# below are some constant variables.
# one of the "SERVER" variables are commented out. If the server does not work on localhost for whatever reason, 
# then the other "SERVER" variable can be used. In that case that variable has to also change on the client side.
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "localhost"
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "dc"


# we make a socket connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# we bind sockets that are connected to the same server and port, aka address (ADDR)
server.bind(ADDR)



connections_list = []
nicknames_list = []
invited_bots_list = []
positive_things_list = ["play", "help", "train", "work", "laugh", "eat", "sing"]
negative_things_list = ["kill", "fight", "steal", "hack", "bully"]


# this is a function that sends message from the sender to everyone except the client that sent the message.
# we have three parameteres. The "bot" parameter is there to check if the messanger is a bot or not.
# if the messanger is a bot it has to have its own way of formatting the message. 
def message_all(message, sender, bot):

    # in case it is a bot, the sender will have a simply name. 
    # in case it is a real connection the sender will be an object with a lot of info.
    # this matters because we cannot put normal string into connections_list.
    # in addition putting bot name in nicknames would mess up the indexing.
    if not bot:
        index = connections_list.index(sender)
        nickname = nicknames_list[index]

    # for every client in connections_list we want to send a message.
    # except if it is the sender, or if it is bot because then we have to do things different in order to make code short.
    for i in connections_list:
        if bot:
            i.send(f"{sender}: {message}".encode(FORMAT))
        elif i is not sender:
            i.send(f"{nickname}: {message}".encode(FORMAT))
            

# this function handles every message that is being send to the server from the client.
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected to the chatroom.")

    connected = True
    while connected:
        message = conn.recv(2048).decode(FORMAT)

        # if message is "dc" we want to stop the while loop and close the connection. 
        if message == DISCONNECT_MESSAGE:
            connected = False
            return conn.close()
        else:
            # here we check if the message is an invitation. If it is then invitation will be true. 
            invitation = analyze_message(message)

            # if it is not an invitation we want to get a message from all bots.
            if not invitation:
                message_all(message, conn, False)
                verb = find_verb(message)
                activate_bots(verb)

        print(f"[{addr}] {message}")



def analyze_message(message):
    # if message is "invite shyvana", that means we want to invite that bot.
    # we also return true because we want to confirm that the message which was send was an invitation.
    if message.lower() == "invite shyvana":
        invite_shyvana()
        return True
    elif message.lower() == "invite cristiano":
        invite_cristiano()
        return True
    elif message.lower() == "invite samanta":
        invite_samanta()
        return True
    elif message.lower() == "invite holmes":
        invite_holmes()
        return True
    else:
        # otherwise we return False to confirm that the message was not an invitation to a bot.
        return False



# this function takes in the message and finds the verb.
def find_verb(message):

    # here we deconstruct the message into a list with words.
    deconstructed_message = message.split(' ')
    for word in deconstructed_message:

        # if the word exists in the list we will return the word. 
        for i in positive_things_list:
            if word == i:
                print(i)
                return word
        for i in negative_things_list:
            if word == i:
                print(i)
                return word

    # otherwise we return nothing as a string.
    return ""



# this function starts the bots. After this function is executed bots will write something in the chat.
def activate_bots(verb):
    if len(invited_bots_list) == 0:
        return
    
    for i in invited_bots_list:
        if i == "Shyvana":
            time.sleep(.5)       
            shy_shyvana(verb)
        elif i == "Holmes":
            time.sleep(.5)
            happy_holmes(verb)
        elif i == "Samanta":
            time.sleep(.5)
            sad_samanta(verb)
        elif i == "Cristiano":
            time.sleep(.5)
            cruel_cristiano(verb)



# this function is adding this bot to the invited_bots_list.
# the point of having that list is to see which bots were invited and are ready to say something in the chat.
def invite_shyvana():
    for i in invited_bots_list:
        if i == "Shyvana":
            return message_all("Im already invited, I think...", "Shyvana", True)

    invited_bots_list.append("Shyvana")
    message_all("H-hi, e-everyone... Im shy Shyvana...", "Shyvana", True)

def shy_shyvana(verb):
    if verb in positive_things_list:
        positive_answers = [
            f"Did you say {verb}ing? That would be amazing!",
            f"People call me shy, but for once I will not be shy; you said {verb}ing? That would be amazing! I would love to do that!",
            f"{verb}ing sounds awesome, let's do it!",
        ]

        # if the verb is a good verb, a random sentence from positive_answers will be chosen and send to all clients.
        return message_all(random.choice(positive_answers), "Shyvana", True)

    elif verb in negative_things_list:
        negative_answers = [
            f"People call me shy, but for once I will not be shy; {verb}ing sounds terrible! Do not do it or else I will get very mad!",
            f"Did you say {verb}ing? That would be awful!",
            f"{verb}ing sounds terrible, lets not do that!",
        ]

        # if the verb is a bad verb, a random sentence from negative_answers will be chosen and send to all clients.
        return message_all(random.choice(negative_answers), "Shyvana", True)
    else:
        # otherwise the user has not sent a message with a verb in it that can be detected by the program.
        return message_all("Umm,.. Not sure what you meant...", "Shyvana", True)



def invite_samanta():
    for i in invited_bots_list:
        if i == "Samanta":
            return message_all("I am here...", "Samanta", True)

    invited_bots_list.append("Samanta")
    message_all("Hi everyone. Im Samanta", "Samanta", True)

def sad_samanta(verb):
    if verb in positive_things_list:
        positive_answers = [
            f"Someone once told me that{verb}ing is awesome!",
            f"I think {verb}ing would change my mood.",
            f"Did you say {verb}ing? That would be amazing!",
        ]
        return message_all(random.choice(positive_answers), "Samanta", True)

    elif verb in negative_things_list:
        negative_answers = [
            f"I already had a bad day, but {verb}ing would make it even worse!",
            f"Did you say {verb}ing? I think {verb}ing is awful!",
            f"Why would we be {verb}ing? I do not want to do that!",
        ]
        return message_all(random.choice(negative_answers), "Samanta", True)
    else:
        return message_all("I did not understand what you meant", "Samanta", True)



def invite_holmes():
    for i in invited_bots_list:
        if i == "Holmes":
            return message_all("I am here...", "Holmes", True)

    invited_bots_list.append("Holmes")
    message_all("Hi everyone. Im Holmes", "Holmes", True)

def happy_holmes(verb):
    if verb in positive_things_list:
        positive_answers = [
            f"I love {verb}ing and everyone!",
            f"Well, {verb}ing sounds like an awesome activity!",
            f"Did you say {verb}ing? That is the best thing in the entire world!",
        ]
        return message_all(random.choice(positive_answers), "Holmes", True)

    elif verb in negative_things_list:
        negative_answers = [
            f"I had a good day today, but {verb}ing would make it less awesome!",
            f"Did you say {verb}ing? I do not want to do that, it sounds awful!",
            f"There are not many things I hate to do, but {verb}ing would be one of them!",
        ]
        return message_all(random.choice(negative_answers), "Holmes", True)
    else:
        return message_all("What did you mean?", "Holmes", True)



def invite_cristiano():
    for i in invited_bots_list:
        if i == "Cristiano":
            return message_all("I am here...", "Cristiano", True)

    invited_bots_list.append("Cristiano")
    message_all("Hi everyone. Im Cristiano", "Cristiano", True)

def cruel_cristiano(verb):
    if verb in positive_things_list:
        positive_answers = [
            f"Did you say {verb}ing? Sure, why not. Lets do it!",
            f"Why would we be {verb}ing? Pff, whatever. Lets go and do it!",
            f"I think {verb}ing sounds kinda cool.",
        ]
        return message_all(random.choice(positive_answers), "Cristiano", True)

    elif verb in negative_things_list:
        negative_answers = [
            f"Cruel is my second name, but even I would be {verb}ing!",
            f"Did you say {verb}ing? I did not think I would ever say that, but that sounds awful!",
            f"Wow! Where did you come up with that idea? Not even me would enjoy {verb}ing...",
        ]
        return message_all(random.choice(negative_answers), "Cristiano", True)
    else:
        return message_all("What? You have to be more spesific! What do you want to do?", "Cristiano", True)



def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # we accept anyone that connects to the server.
        conn, addr = server.accept()

        # we create a thread to handle all incoming messages from the clients.
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        # here we send a request to the user to choose a username for the chatroom.
        # then we save it in the array as well as the connection which the user comes from.
        conn.send("Type in your nickname: ".encode(FORMAT))
        nickname = conn.recv(2048).decode('utf-8')
        nicknames_list.append(nickname)
        connections_list.append(conn)

print("[STARTING] server is starting...")
start()