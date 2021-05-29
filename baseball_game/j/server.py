# SERVER

from socket import*
import random
import itertools

print("The server is ready to receive a game request.")
# initializing Socket
serverPort = 12000
serverSock: socket = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('localhost', serverPort))
serverSock.listen(1)

connectionSock, addr = serverSock.accept()

# Before starting the game..
getMSG = connectionSock.recv(1024)
message = getMSG.decode('utf-8')
if message == "request_game":
    print("From Client :", message)
else:  # if the received message is not "request_game", exit game
    exit()

sendMSG = "ok"
print("To Client :", sendMSG)
connectionSock.send(sendMSG.encode('utf-8'))

# making a list with all available numbers
all_number = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
num_list = list(map(''.join, itertools.permutations(all_number, 3)))
# fetching a index for the answer
answer_idx = random.randrange(0, len(num_list))
answer = num_list[answer_idx]  # initializing answer
print("Answer:", answer)

# trials are for dividing lists
trial = 0
f_trial = 0
# strike and balls for filtering
strike = 0
ball = 0
# strike and balls for sending
C_strike = 0
C_ball = 0
# flag for quiting game
exitFlag = 0
# lists for game...
filtered = []
clientNUM = []
sent = []

while True:
    # for the first trial
    if trial == 0:
        num_list = list(map(''.join, itertools.permutations(all_number, 3)))
        # fetching index for guessing number by random
        random_idx = random.randrange(0, len(num_list))
        guess = num_list[random_idx]
        trial = 1
    # after the first trial
    else:
        # fetching index for guessing number by random
        random_idx = random.randrange(0, len(num_list))
        guess = num_list[random_idx]

    # receiving/decoding received message
    getMSG = connectionSock.recv(1024)
    getSTR = getMSG.decode('utf-8')

    # divide and store received message
    clientNUM.clear()
    clientNUM.append(getSTR[1])
    clientNUM.append(getSTR[4])
    clientNUM.append(getSTR[7])
    strike = int(getSTR[11])  # received strikes
    ball = int(getSTR[14])  # received balls

    print("From Client :", getSTR)

    # conditions to end game
    if C_strike == 3:
        result = "Server Lose!"
        exitFlag = 1

    if strike == 3:
        result = "Server Win!"
        exitFlag = 1

    if strike == 3 and C_strike == 3:
        result = "Draw!"
        exitFlag = 1

    if exitFlag == 1:
        print(result)
        break

    # counting Strikes and Balls
    C_strike = 0  # strikes of client's number
    C_ball = 0  # balls of client's number

    for i in range(0, 3):
        for j in range(0, 3):
            if answer[i] == clientNUM[j] and i == j:
                C_strike += 1
            elif answer[i] == clientNUM[j] and i != j:
                C_ball += 1
    # counting ended

    # filtering LIST FOR SERVER
    if f_trial == 0:
        f_trial = 1
    else:
        k = 0
        while k < len(num_list):
            tmp_strike = 0
            tmp_ball = 0
            for i in range(0, 3):
                for j in range(0, 3):
                    if sent[i] == num_list[k][j] and i == j:
                        tmp_strike += 1
                    elif sent[i] == num_list[k][j] and i != j:
                        tmp_ball += 1

            if tmp_strike == strike and tmp_ball == ball:
                filtered.append(num_list[k])

            k += 1

        num_list.clear()
        for i in filtered:
            num_list.append(i)

        filtered.clear()
    # filtering ended

    # preparing sending MSG
    S = str(C_strike)
    B = str(C_ball)

    sent.clear()
    for i in guess:
        sent.append(i)
    # sending massage to client
    sendMSG = "[" + guess[0] + ", " + guess[1] + ", " + guess[2] + "]" + "/[" + S + ", " + B + "]"
    print("To Client :", sendMSG)
    connectionSock.send(sendMSG.encode('utf-8'))

connectionSock.close()
serverSock.close()
exit()
