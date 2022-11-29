import socket

localAddress = "127.0.0.1"
localPort = 5000
bufferSize = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((localAddress, localPort))

print("Server is listening...")

while(True): 
    message, address = server.recvfrom(bufferSize)
    clientMessage = f"Client : {message.decode('utf-8')}"
    clientAddress = "Client Address : {}".format(address)

    print(clientMessage)
    print(clientAddress)
    