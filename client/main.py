import socket
import commands
import threading

bufferSize = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(5)


while(True):
    
    commandString = None
    while commandString == None: 
        commandString = input('')
    clientCommands = commands.Commands(client, bufferSize)
    command = clientCommands.tokenizeCommandString(commandString)
    clientCommands.commandSwitch(command)
    
    thread = threading.Thread(target=clientCommands.threadRecvFromServer)
    thread.daemon = True
    thread.start()
    
    
