import random
from socket import *
import itertools

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('localhost',serverPort))
serverSocket.listen(1)

connectionSock, addr = serverSocket.accept()

print("The server is ready to receive a game request.")

list1 = ['1','2','3','4','5','6','7','8','9']

ans = random.sample(list1,3) #SERVER가 정하는 답안(client가 맞출거)

list2 = list(map(''.join,itertools.permutations(list1,3)))
flag = 0  #gameover condition flag


trysend = random.choice(list2) #내가 맞출 clinet 의 답,초기엔 이렇게 설정 다음은 while 안에서 설정

count = 0
insb = []  #상대가 주는 Strike,Ball 정보
arr = []  #삭제할 것들의 index저장소

sent = ['0','0']

while True:


    message = connectionSock.recv(1024)
    modifiedMessage = message.decode('utf-8')


    if modifiedMessage == 'request_game': #상대가 게임을 요구한다면,(상대가 Yes를 했다면)

        print('From Client:',modifiedMessage)
        modifiedMessage = str('ok')   #건네줄 message는 OK이다.
        print('To Client:',modifiedMessage)
        print('Answer:',ans[0]+ans[1]+ans[2])  #나의 Answer 출력
        connectionSock.send(modifiedMessage.encode())
        count += 1
        continue

    elif modifiedMessage == 'No':  #상대가 No을 선택 했을때,
        print('request_game_fail!!!')
        break

    else: #보통의 Cycle
        insb.clear()  #상대가 준 Strike,Ball
        print('From client:',modifiedMessage)

        insb.append(modifiedMessage[11])  #insb에 상대가 준 Strike,Ball 삽입.
        insb.append(modifiedMessage[14])

        s = 0
        b = 0
        arr.clear() #삭제할 index list 초기화
        ins = int(insb[0]) #상대가 준 S
        inb = int(insb[1]) #상대가 준 B

        for i in range(len(list2)):  #내가 보냈던것과 상대가 준 S,B를 통해 판단하여 불가능한 경우의수 모두 제외하기
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
            if (  (tmps != ins) or (tmpb != inb) ):
                arr.append(i)  #delete 할것들의 모음

        j = int(len(arr)) - 1
        if  len(list2) > 1 and count != 1: #처음에 상대가 주는 0,0은 결과에 영향을 안주기 때문에,
            while j >= 0 :
                p = int(arr[j])
                del list2[p]                #불가능한 경우의수 arr을 통해 list2에서 모두 삭제
                j -= 1

        if len(list2) > 1:
            choicelist = random.choice(list2) #가능한 경우의수중에서 random으로 Guess를 설정,

        data = modifiedMessage  #상대의 Guess를 판단

        if ans[0] == (data[1]):  #나의 Ans와 상대의 Guess를 판단.
            s = s + 1
        if ans[0] == (data[4]):
            b = b + 1
        if ans[0] == (data[7]):
            b = b + 1
        if ans[1] == (data[4]):
            s = s +1
        if ans[1] == (data[7]):
            b = b +1
        if ans[1] == (data[1]):
            b = b +1
        if ans[2] == (data[7]):
            s = s + 1
        if ans[2] == (data[1]):
            b = b + 1
        if ans[2] == (data[4]):
            b = b + 1

        count += 1

        out = [str(s), str(b)]  #상대의 guess에 대한 결과 넘겨주기.

        trysend = choicelist

        if (ins == 3) and (int(sent[0])) == 3:
            flag = 2
            print('Draw!')

        elif (ins == 3) and (int(sent[0])) != 3:
            flag = 3
            print('Server Win!')

        elif (ins != 3) and (int(sent[0])) == 3:
            flag = 1
            print('Server Lose!')


        sent = out  #Game이 끝날때 win,draw,lose 판단 위해 보냈던 결과 가지고있기.

        count += 1

        send = '['+choicelist[0]+', '+choicelist[1] + ', ' + choicelist[2]+']'+'/['+out[0]+', '+ out[1]+']'

        if flag == 0:
            print('To client:',send)

        modifiedMessage = str(send)
        connectionSock.send(modifiedMessage.encode())

        if (flag == 1) or (flag == 2) or (flag == 3):
            break

connectionSock.close()#game_over --> close socket.
