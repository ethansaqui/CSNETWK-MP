import socket

class serverUtilities:
    
    def __init__(self, localAddress, localPort, bufferSize):
        self.localAddress = localAddress
        self.localPort = localPort
        self.bufferSize = bufferSize
    
        