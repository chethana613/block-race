from main import *

class User:
    def __init__(self, name):
        self.name = name
        self.roomdetails = []
        self.thisRoom = ''

class Room:
    def __init__(self, name):
        self.peoples = []
        self.nicknames = []
        self.name = name

#Lists the available rooms with nickanmes
def list_all_roomdetails(nickname):
    name = users[nickname]
    print(len(roomdetails))
    if len(roomdetails) == 0:
        name.send('No roomdetails are available to join'.encode('utf-8'))
    else:
        reply = "List of available roomdetails:\n"
        for room in roomdetails:
            room_name = roomdetails[room].name
            nicknames = ', '.join(roomdetails[room].nicknames)
            reply += 'Room' + ' ' + f"{room_name} : {nicknames}\n"
        name.send(f'{reply}'.encode('utf-8'))
        
       
#now to join to other rooms
def join_room(nickname, room_name):
    name = users[nickname]
    user = users_in_room[nickname]
    if room_name not in roomdetails:
        room = Room(room_name)
        room.created_by = nickname  # Store the creator's nickname
        roomdetails[room_name] = room
        room.peoples.append(name)
        room.nicknames.append(nickname)

        user.thisRoom = room_name
        user.roomdetails.append(room)
        name.send(f' Room {room_name} is created'.encode('utf-8'))
        name.send(f' Room {room_name} created by {nickname}'.encode('utf-8'))
    else:
        room = roomdetails[room_name]
        if room_name in user.roomdetails:
            name.send('You are already in the roomroom'.encode('utf-8'))
        else:
            room.peoples.append(name)
            room.nicknames.append(nickname)
            user.thisRoom = room_name
            user.roomdetails.append(room)
            broadcast(f'{nickname} joined the room, which was created by {room.created_by}', room_name)
            

#now to leave the room
def leave_room(nickname):
    user = users_in_room[nickname]
    name = users[nickname]
    if user.thisRoom == '':
        name.send('You are not part of any room'.encode('utf-8'))
    else:
        roomname = user.thisRoom
        room = roomdetails[roomname]
        user.thisRoom = ''
        user.roomdetails.remove(room)
        roomdetails[roomname].peoples.remove(name)
        roomdetails[roomname].nicknames.remove(nickname)
        broadcast(f'{nickname} left the room', roomname)
        name.send('You left the room'.encode('utf-8'))
        #del users_in_room[nickname]


#now to quit the server
def remove_client(nickname):
    nicknames.remove(nickname)
    client = users[nickname]
    user = users_in_room[nickname]
    user.thisRoom = ''
    for room in user.roomdetails:
        print(room.name)
        room.peoples.remove(client)
        print(room.peoples)
        room.nicknames.remove(nickname)
        print(room.nicknames)
        broadcast(f'{nickname} left the room', room.name)


#to handle
def handle(client):
    nick=''
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            args = message.split(" ")
            name = users[args[0]]
            nick = args[0]          
            if 'display' in message:
                list_all_roomdetails(args[0])
            elif 'join' in message:
                join_room(args[0], ' '.join(args[2:]))
            elif 'leave' in message:
                leave_room(args[0])
            else:
                if users_in_room[args[0]].thisRoom == '':
                    name.send('You are not part of any room'.encode('utf-8'))
                else:
                    msg = ' '.join(args[1:])
                    broadcast(f'{args[0]}: {msg}',users_in_room[args[0]].thisRoom)

            #broadcast(message)
        except Exception as e:
            print("exception occured ", e)
            index = clients.index(client)
            clients.remove(client)
            client.close()
            '''nickname = nicknames[index]
            print(f'{nickname} left')
            user = users_in_room[nickname]'''
            '''if user.thisRoom != '':
                roomname = user.thisRoom
                user.thisRoom = ''
                #user.roomdetails.remove(roomname)
                roomdetails[roomname].peoples.remove(name)
                roomdetails[roomname].nicknames.remove(nickname)
                broadcast(f'{nickname} left the room', roomname)'''
            print(f'nick name is {nick}')
            if nick in nicknames:
                remove_client(nick)
            if nick in nicknames:
                nicknames.remove(nick)

            #broadcast(f'{nickname} left the room'.encode('utf-8'))

            break

#main
def recieve():
    while True:
        client, address = server.accept()
        print(f'connected with {str(address)}')
        print(client)
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        user = User(nickname)
        users_in_room[nickname] = user
        users[nickname] = client
        print(f'Nickname of the client is {nickname}')
        #broadcast(f'{nickname} joined the chat'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))
        client.send(instructions.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening...')
recieve()