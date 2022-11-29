import socket
import commands

localAddressPort = ("127.0.0.1", 5000)
bufferSize = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



client.shutdown();