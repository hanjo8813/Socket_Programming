# CLIENT

from socket import*
import random
import itertools

# initializing Socket
serverPort = 12000
clientSock: socket = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('localhost', serverPort))
# input for starting game
print("Do you want to play a game? [Yes or No]", end=' ')
message = input()

if message == "Yes":
    sendMSG = "request_game"
    print("To Server:", sendMSG)
    clientSock.send(sendMSG.encode('utf-8'))
else:  # if the input message is not "Yes", send Fail message to server and exit game
    sendMSG = "FAIL"
    clientSock.send(sendMSG.encode('utf-8'))
    exit()
# Before starting the game..
getMSG = clientSock.recv(1024)

print("From Server :", getMSG.decode('utf-8'))

# making a list with all available numbers
all_number = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
num_list = list(map(''.join, itertools.permutations(all_number, 3)))
# fetching a index for the answer
answer_idx = random.randrange(0, len(num_list))
answer = num_list[answer_idx]
print("Answer:", answer)

# trials for dividing lists
trial = 0
# strikes and balls for filtering
strike = 0
ball = 0
# strikes and balls for sending
S_strike = 0
S_ball = 0
# flag for quiting game
exitFlag = 0
# lists for game...
filtered = []
serverNUM = []

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

    S = str(S_strike)
    B = str(S_ball)
    # checking ending condition
    if exitFlag == 1:
        print(result)
        clientSock.send(sendMSG.encode('utf-8'))
        print("To Server :", sendMSG)
        break
    else:
        sendMSG = "[" + guess[0] + ", " + guess[1] + ", " + guess[2] + "]" + "/[" + S + ", " + B + "]"
        clientSock.send(sendMSG.encode('utf-8'))
        print("To Server :", sendMSG)
    # receiving/decoding received message
    getMSG = clientSock.recv(1024)
    getSTR = getMSG.decode('utf-8')
    print("From Server :", getSTR)
    # dividing and storing received message
    serverNUM.clear()
    serverNUM.append(getSTR[1])
    serverNUM.append(getSTR[4])
    serverNUM.append(getSTR[7])
    strike = int(getSTR[11])
    ball = int(getSTR[14])

    # counting SERVER strikes, balls
    S_strike = 0
    S_ball = 0

    for i in range(0, 3):
        for j in range(0, 3):
            if answer[i] == serverNUM[j] and i == j:
                S_strike += 1
            elif answer[i] == serverNUM[j] and i != j:
                S_ball += 1
    # counting ended

    # filtering LIST FOR CLIENT
    k = 0
    while k < len(num_list):
        tmp_strike = 0
        tmp_ball = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if guess[i] == num_list[k][j] and i == j:
                    tmp_strike += 1
                elif guess[i] == num_list[k][j] and i != j:
                    tmp_ball += 1

        if tmp_strike == strike and tmp_ball == ball:
            filtered.append(num_list[k])

        k += 1

    num_list.clear()
    for i in filtered:
        num_list.append(i)

    filtered.clear()
    # filtering ended

    # conditions to end game
    if S_strike == 3:
        result = "Client Lose!"
        exitFlag = 1
        sendMSG = "[0, 0, 0]/[3, 0]"

    if strike == 3:
        result = "Client Win!"
        exitFlag = 1
        S = str(S_strike)
        B = str(S_ball)
        sendMSG = "[" + guess[0] + ", " + guess[1] + ", " + guess[2] + "]" + "/[" + S + ", " + B + "]"

    if strike == 3 and S_strike == 3:
        result = "Draw!"
        exitFlag = 1
        S = str(S_strike)
        B = str(S_ball)
        sendMSG = "[" + guess[0] + ", " + guess[1] + ", " + guess[2] + "]" + "/[" + S + ", " + B + "]"

clientSock.close()
exit()
