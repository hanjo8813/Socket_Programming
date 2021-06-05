from socket import *
from itertools import permutations
import random

# ------------------------------------------------ function ------------------------------------------------

# function of make & send MC message 
def send_MC_msg(guess, strike, ball):
    global clientSocket
    MC_header = 'MC'
    MC_body = "[" + guess[0] + ", " + guess[1] + ", " + guess[2] + ", " + guess[3] + "]" + "/[" + str(strike) + ", " + str(ball) + "]"
    print('To Server:', MC_body)
    MC_msg = MC_header + MC_body
    clientSocket.send(MC_msg.encode())
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
clientSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12000

# if server is not ready, quit program
try :
    clientSocket.connect( ('localhost', serverPort) )
except :
    print('Server is not open.')
    quit()

# request start game
confirm = input('Do you want a number baseball game? (Yes or No) : ')
if confirm == 'Yes':
    request_header = 'MA'
    request_body = 'game_request'
    request_msg = request_header + request_body
    print('To Server:', request_body)
    clientSocket.send(request_msg.encode())
else :
    quit()

# init global variables
number = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
client_candidate = list(map(''.join, permutations(number, 4)))
client_answer = client_candidate[random.randrange(0, len(client_candidate))]
client_guess = client_candidate[random.randrange(0, len(client_candidate))]
server_strike = 0
server_ball = 0

while True :
    # parsing message to header & body
    msg = clientSocket.recv(1024).decode()
    msg_header = msg[:2]
    msg_body = msg[2:]

    # game grant
    if msg_header == 'MB':
        print('From Server:', msg_body)
        print('Answer:', client_answer)
        send_MC_msg(client_guess, 0, 0)
    
    # during game
    elif msg_header == 'MC':
        print('From Server:', msg_body)

        # parsing message to guess & my result
        server_guess = msg_body[1] + msg_body[4] + msg_body[7] + msg_body[10]
        client_strike = msg_body[14]
        client_ball = msg_body[17]
        
        # parsing error
        if server_guess != '0000' and len(set(server_guess)) != 4:
            print('Wrong guess (same digits)')
            quit()
        
        # Score the server guess
        server_strike, server_ball = compare_num_str(client_answer, server_guess)

        # Judge game result
        if server_strike == '4' or client_strike =='4':
            if server_strike != '4' and client_strike == '4':
                print('Client Win!')
            if server_strike == '4' and client_strike != '4':
                print('Client Lose!')
                client_guess = '0000'
                server_strike = 4
                server_ball = 0
            if server_strike == '4' and client_strike == '4':
                print('Draw')
            send_MC_msg(client_guess, server_strike, server_ball)
            break
        
        # filtering candidate
        temp_list = [] 
        for candidate in client_candidate:
            temp_strike, temp_ball = compare_num_str(candidate, client_guess)
            if temp_strike == client_strike and temp_ball == client_ball:
                temp_list.append(candidate)
        client_candidate = temp_list
        client_guess = client_candidate[random.randrange(0, len(client_candidate))]
        
        # send client guess & server result
        send_MC_msg(client_guess, server_strike, server_ball)
        
# close socket
clientSocket.close()
quit()