import socket
import serverUtilities
import json

localAddress = "127.0.0.1"
localPort = 5000
bufferSize = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((localAddress, localPort))

utils = serverUtilities.serverUtilities(localAddress, localPort, bufferSize)

print("Server is listening...")

while(True): 
    message, clientAddress = server.recvfrom(bufferSize)
    # Convert back to JSON
    clientMessage = message.decode()
    clientMessage = json.loads(clientMessage.replace("\'","\""))
    
    # Acknowledge client connection
    server.sendto("".encode(), clientAddress)
    
    
    print(type(clientMessage))
    print(clientMessage)
    print(clientAddress)
    