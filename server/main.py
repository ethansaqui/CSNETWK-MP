import socket

localAddress = "127.0.0.1"
localPort = 5000
bufferSize = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((localAddress, localPort))

print("Server is listening...")

while(True): 
    message, clientAddress = server.recvfrom(bufferSize)
    clientMessage = message.decode()
    
    # Acknowledge client connection
    server.sendto("".encode(), clientAddress) 
    
    print(clientMessage)
    print(clientAddress)
    