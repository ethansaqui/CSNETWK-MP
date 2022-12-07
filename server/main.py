import socket
import serverUtilities
import json


localAddress = "127.0.0.1"
localPort = 12345
bufferSize = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((localAddress, localPort))


utils = serverUtilities.serverUtilities(localAddress, localPort, bufferSize, server)

print("Server is listening...")

continueRunning = True

while(continueRunning):
    message, clientAddress = server.recvfrom(bufferSize)
    # Convert back to JSON
    print(message)
    clientMessage = message.decode()
    clientMessage = json.loads(clientMessage)
    
    continueRunning = utils.parseJsonCommand(clientMessage, clientAddress)
server.close()
    
