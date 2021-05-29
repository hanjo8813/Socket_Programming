from socket import *
from itertools import permutations
import random


# 
clientSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12000

# 
try :
    clientSocket.connect( ('localhost', serverPort) )
except :
    print('Server is not open.')
    quit()

#
confirm = input('Do you want a number baseball game? (Yes or No) : ')
if confirm == 'Yes':
    request_header = 'MA'
    request_body = 'game_request'
    request_msg = request_header + request_body
    print('To Server:', request_body)
    clientSocket.send(request_msg.encode())
else :
    quit()

#
number = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
num_list = list(map(''.join, permutations(number, 4)))
client_answer = num_list[random.randrange(0, len(num_list))]

#
while True :
    #
    msg = clientSocket.recv(1024).decode()
    msg_header = msg[:2]
    msg_body = msg[2:]

    #
    if msg_header == 'MB':
        print('From Server:', msg_body)
        print('Answer:', client_answer)
        # 첫번째 시도

    #
    #if msg_header == 'MC':



'''
# 입력이 완료되면 소켓이 메시지를 '미리 연결된' 서버에 보낸다.
print('보내는 중....')
clientSocket.send(message.encode())

# 그리고 소켓이 다시 변경된 메시지를 받는다.
modifiedMessage = clientSocket.recv(1024)
print('서버에서 수정된 메시지 : ' + modifiedMessage.decode()) 

# 소켓 닫기.
clientSocket.close()
'''

