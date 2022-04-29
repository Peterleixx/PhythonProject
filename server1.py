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



#Method broadcast the message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

#Listening for messages from clients
def listen(client):
    while True:
        try: 
            #Send a message to check connection
            message = client.recv(1024)
            broadcast(message)
        except:
            username = usernames[clients.index(client)]
            broadcast(f'{username} left the group'.encode('ascii'))
            usernames.remove(username)
            clients.remove(client)
            client.close()
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('UN'.encode('ascii'))
        name = client.recv(1024)
        usernames.append(name)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Username is {}".format(name))
        broadcast("{} joined!".format(name).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=listen, args=(client,))
        thread.start()
receive()