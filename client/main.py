import socket
import commands

bufferSize = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(5)
while(True):
    commandString = None
    while commandString == None: 
        commandString = input('Enter a command:\n')
    clientCommands = commands.Commands(client, bufferSize)
    command = clientCommands.tokenizeCommandString(commandString)
    clientCommands.commandSwitch(command)
 
    
