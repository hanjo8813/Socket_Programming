from socket import *
from itertools import permutations
import random


# init
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12000
serverSocket.bind( ('', serverPort) )
serverSocket.listen(1)

#
print('The server is ready to receive a game request.')

#
connetSocket, addr = serverSocket.accept()

# 
number = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
num_list = list(map(''.join, permutations(number, 4)))
server_answer = num_list[random.randrange(0, len(num_list))]


#
while True :
    #
    msg = connetSocket.recv(1024).decode()
    msg_header = msg[:2]
    msg_body = msg[2:]

    #
    if msg_header == 'MA':
        print('From Client:', msg_body)
        grant_header = 'MB'
        grant_body = 'game_grant'
        grant_msg = grant_header + grant_body
        print('To Client:', grant_body)
        connetSocket.send(grant_msg.encode())
        print('Answer:', server_answer)
        
    #
    #if msg_header == 'MC':

