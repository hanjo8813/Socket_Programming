import random
from socket import *
import itertools


serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))



list1 = ['1','2','3','4','5','6','7','8','9']

ans = random.sample(list1,3) #Client 정하는 답안(Server가 맞출거)

list2 = list(map(''.join,itertools.permutations(list1,3)))

count = 0

arr = []

outsb = []

out = 0

insb = []  #상대가 준 s,b

prevmessage = []  #내가 전에 한 guess




flag = 0 #1 = server Win , 2 = Draw , 3 = Client Win




while True:

    try:
        if count == 0: #Yes,No 입력부분

            message = input('Do you want to play a game? (Yes or No):')

            if message != 'Yes': #Yes를 안받을때
                clientSocket.send(message.encode()) #No전송해주고 break후에 socket_close
                break
            else:      #input이 Yes라면
                message = 'request_game'

            print('To server:',message)

            clientSocket.send(message.encode())
            modifiedMessage = clientSocket.recv(1024)
            modifiedMessage = modifiedMessage.decode()
            count += 1


        if count == 1:    # 게임 start , 나의 guess,0,0 보내기
            if modifiedMessage == 'ok':
                print('From server:',modifiedMessage)
            else:
                print('reques_game_fail!!!')
                break

            trysend = random.choice(list2)

            outsb.append(0)  #첫 Guess에는 Strike,Ball 0,0으로 해야함.
            outsb.append(0)

            send = '[' + trysend[0] + ', ' + trysend[1] + ', ' + trysend[2] + ']' + '/[' + str(outsb[0]) + ', ' + str(outsb[1]) + ']'
            #send 할것은 문자열리스트로 작성
            message = send
            clientSocket.send(message.encode())
            modifiedMessage= clientSocket.recv(1024)
            modifiedMessage = modifiedMessage.decode()
            prevmessage = modifiedMessage    #나의 Guess에 대하여 Strike,Ball받은걸로 판ㄴ단.
            print('Answer:', ans[0] + ans[1] + ans[2]) #나의 Answer 출력
            print('To server:', send)

            count += 1
            continue

        else:
            insb.clear()   #받은S,B 초기화

            print('From server:', modifiedMessage)

            insb.append(prevmessage[11])
            insb.append(prevmessage[14])  #상대가 준 s,b


            s = 0  #list2 안에서 S,B로 비교하기 위해 0,0으로
            b = 0
            arr.clear()
            ins = int(insb[0])  # 상대가 준 S
            inb = int(insb[1])  # 상대가 준 B


            for i in range(len(list2)):
                tmps = int(0)
                tmpb = int(0)

                if int(list2[i][0]) == int(trysend[0]):
                    tmps = tmps + 1
                if int(list2[i][0]) == int(trysend[1]):
                    tmpb = tmpb + 1
                if int(list2[i][0]) == int(trysend[2]):
                    tmpb = tmpb + 1
                if int(list2[i][1]) == int(trysend[1]):
                    tmps = tmps + 1
                if int(list2[i][1]) == int(trysend[2]):
                    tmpb = tmpb + 1
                if int(list2[i][1]) == int(trysend[0]):
                    tmpb = tmpb + 1
                if int(list2[i][2]) == int(trysend[2]):
                    tmps = tmps + 1
                if int(list2[i][2]) == int(trysend[0]):
                    tmpb = tmpb + 1
                if int(list2[i][2]) == int(trysend[1]):
                    tmpb = tmpb + 1
                if ((tmps != ins) or (tmpb != inb)):
                    arr.append(i)  # delete 할것들의 모음(list2의 인덱스값이 들어있음)


            j = int(len(arr)) - 1  #list2의 len때문에 뒤에서부터 삭제를 해야함.
            if len(list2) > 1:
                while j >= 0:
                    p = int(arr[j])
                    del list2[p]
                    j -= 1

            choicelist = random.choice(list2)  #보낼것을 가능한 경우의수안에서 랜덤으로 선택


            data = prevmessage   #상대의 Guess를 판단해주는 과정

            if ans[0] == (data[1]):
                s = s + 1
            if ans[0] == (data[4]):
                b = b + 1
            if ans[0] == (data[7]):
                b = b + 1
            if ans[1] == (data[4]):
                s = s + 1
            if ans[1] == (data[7]):
                b = b + 1
            if ans[1] == (data[1]):
                b = b + 1
            if ans[2] == (data[7]):
                s = s + 1
            if ans[2] == (data[1]):
                b = b + 1
            if ans[2] == (data[4]):
                b = b + 1

            outsb.clear()
            outsb.append(str(s))
            outsb.append(str(b))

            trysend = choicelist

            count += 1
            send = '[' + trysend[0] + ', ' + trysend[1] + ', ' + trysend[2] + ']' + '/[' + outsb[0] + ', ' + outsb[
                1] + ']'

            message = send
            #flag를 통해서 종료조건을 설정해준다.
            if (ins == 3) and (int(outsb[0])) == 3:
                flag = 2
                print('Draw!')

            elif (ins ==3) and (int(outsb[0])) != 3:
                flag = 3
                print('Client Win!')

            elif (ins != 3) and (int(outsb[0])) == 3:
                flag = 1
                print('Client Lose!')

            print('To server:', send)

            clientSocket.send(message.encode())
            modifiedMessage= clientSocket.recv(1024)
            modifiedMessage = modifiedMessage.decode()
            prevmessage = modifiedMessage





    finally:
        if (flag == 3) or (flag == 1) or (flag == 2):
            break


clientSocket.close()   #while 끝난뒤에 socket닫아주기.