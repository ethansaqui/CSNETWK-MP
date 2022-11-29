import socket
import commands

defaultAddress = "127.0.0.1"
defaultPort = 5000
bufferSize = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while(True):
    commandString = None
    while commandString == None: 
        commandString = input('Enter a command:\n')
    clientCommands = commands.Commands(defaultAddress, defaultPort)
    command = clientCommands.tokenizeCommandString(commandString)
    clientCommands.commandSwitch(command)
