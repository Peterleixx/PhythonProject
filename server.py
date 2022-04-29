import socket
import threading

#Assign the port and port of the serser.
Host = '127.0.0.1'
Port = 9999

#Create the TCP server and listen for the connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((Host, Port))
server.listen()
print(f"Server is listenting")

#List for client and the username
clients = []
usernames = []
messages = []


#Method broadcast the message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)
        client.send(f"Message ID: {len(messages)}".encode(ascii))

#Listening for messages from clients
def listen(client):
    while True:
        try: 
            message = client.recv(1024)
            broadcast(message)
            messages.append(message)
            
        except:
            username = usernames[clients.index(client)]
            broadcast(f'{username} left the group'.encode('ascii'))
            usernames.remove(username)
            clients.remove(client)
            client.close()
            break

def history(client):
    pass

# Receiving the connection
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request the username
        client.send('UN'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        usernames.append(name)
        clients.append(client)

        # Print And Broadcast username
        print("Username is {}".format(name))
        broadcast("{} joined!".format(name).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start listening thread that keep listen for the neww message
        thread = threading.Thread(target=listen, args=(client,))
        thread.start()
receive()

    

