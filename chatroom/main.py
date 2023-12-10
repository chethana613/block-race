#This module contains the socket connection
import socket
import threading #for multiple process

host = '127.0.0.1' #localhost
port = 8081  #do not use 0 to 40000, as they are reserved
COLOR_PINK = '\033[95m'
COLOR_BLUE = '\033[94m'
COLOR_RESET = '\033[0m'

#starting the server
#AF_INET is for the type of addresses that makes connection (Internet) and SOCK_STREAM is for tcp connections
#AF_INET is for the type of addresses that makes connection (Internet) and SOCK_STREAM is for tcp connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port)) #server is binding
server.listen() #now its in listening mode

instructions = f'{COLOR_BLUE}\nTHESE ARE THE LIST OF INSTRUCTIONS :{COLOR_RESET}\n' \
               f'1.display - to list all the available rooms\n' \
               f'2.leave - to leave the room \n' \
               f'3.join - to join or create a new room\n' \
               f'4.message - message followed by message command\n' \

#now create a empty list and dict for data storage
clients = []
nicknames = []
roomdetails = {}
users = {}
users_in_room = {}

#to broadcast the message
def broadcast(message, roomname):
    for client in roomdetails[roomname].peoples:
        msg = '['+roomname+'] ' +  message
        client.send(msg.encode('utf-8'))