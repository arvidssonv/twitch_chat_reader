import socket
import re
import datetime
import threading

def read_chat():
    print('welcome to twitch chat reader')
    channel = '#' + input('channel to join - twitch.tv/')
    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = '' # your twitch username
    token = '' # your authentication key

    twitch_socket = socket.socket()
    twitch_socket.connect((server, port))
    twitch_socket.send(f"PASS {token}\n".encode('utf-8'))
    twitch_socket.send(f"NICK {nickname}\n".encode('utf-8'))
    twitch_socket.send(f"JOIN {channel}\n".encode('utf-8'))

    connected = False

    while True:
        socket_response = twitch_socket.recv(2048).decode('utf-8')
        if socket_response.startswith('PING'):
            twitch_socket.send("PONG\n".encode('utf-8'))
        else:                        
            if 'End of /NAMES list' in socket_response and not connected:
                connected = True
                print('successfully joined', channel)

            if connected:
                if 'End of /NAMES list' in socket_response:
                    pass
                else:
                    message = re.search(r'[^:]+$', socket_response).group(0).rstrip()
                    username = re.search(r'\w+', socket_response).group(0)                        
                    timestamp = datetime.datetime.now()
                    print('[' + timestamp.strftime("%H:%M") + ']' + ' ' + username + '> ' + message)

if __name__ == '__main__':
    exit(read_chat())