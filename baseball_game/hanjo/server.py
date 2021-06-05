from socket import *
from itertools import permutations
import random
# ------------------------------------------------ function ------------------------------------------------

# function of make & send MC message 
def send_MC_msg(guess, strike, ball):
    global connetSocket
    MC_header = 'MC'
    MC_body = "[" + guess[0] + ", " + guess[1] + ", " + guess[2] + ", " + guess[3] + "]" + "/[" + str(strike) + ", " + str(ball) + "]"
    print('To Client:', MC_body)
    MC_msg = MC_header + MC_body
    connetSocket.send(MC_msg.encode())
    return

# function of score guess
def compare_num_str(str1, str2):
    strike = 0
    ball = 0
    for i, num1 in enumerate(str1):
        for j, num2 in enumerate(str2):
            if num1 == num2:
                if i == j:
                    strike += 1
                else:
                    ball += 1
    return str(strike), str(ball)

# ------------------------------------------------ main ------------------------------------------------

# init socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12000
serverSocket.bind( ('localhost', serverPort) )
serverSocket.listen(1)
print('The server is ready to receive a game request.')

# if connect other client, save connect socket
connetSocket, addr = serverSocket.accept()

# init global variables
number = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
server_candidate = list(map(''.join, permutations(number, 4)))
server_answer = server_candidate[random.randrange(0, len(server_candidate))]
server_guess = ''
client_strike = 0
client_ball = 0

while True :
    # parsing message to header & body
    msg = connetSocket.recv(1024).decode()
    msg_header = msg[:2]
    msg_body = msg[2:]

    # accept request & notify game grant
    if msg_header == 'MA':
        print('From Client:', msg_body)
        grant_header = 'MB'
        grant_body = 'game_grant'
        grant_msg = grant_header + grant_body
        print('To Client:', grant_body)
        connetSocket.send(grant_msg.encode())
        print('Answer:', server_answer)

    # during game
    if msg_header == 'MC':
        print('From Client:', msg_body)

        # parsing message to guess & my result
        client_guess = msg_body[1] + msg_body[4] + msg_body[7] + msg_body[10]
        server_strike = msg_body[14]
        server_ball = msg_body[17]

        # parsing error
        if client_guess != '0000' and len(set(client_guess)) != 4:
            print('Wrong guess (same digits)')
            quit()

        # Judge game result
        if client_strike == '4' or server_strike =='4':
            if client_strike == '4' and server_strike != '4':
                print('Server Lose!')
            elif client_strike != '4' and server_strike == '4':
                print('Server Win!')
            elif client_strike == '4' and server_strike == '4':
                print('Draw!')
            break

        # Score the client guess
        client_strike, client_ball = compare_num_str(server_answer, client_guess)

        # filtering candidate
        if server_guess:
            temp_list = []
            for candidate in server_candidate:
                temp_strike, temp_ball = compare_num_str(candidate, server_guess)
                if temp_strike == server_strike and temp_ball == server_ball:
                    temp_list.append(candidate)
            server_candidate = temp_list
        server_guess = server_candidate[random.randrange(0, len(server_candidate))]

        # send server guess & client result
        send_MC_msg(server_guess, client_strike, client_ball)

# close socket
connetSocket.close()
serverSocket.close()
quit()