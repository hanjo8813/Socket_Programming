from socket import *

# 포트 번호
serverPort = 12000
# 소켓 생성하기
serverSocket = socket(AF_INET, SOCK_DGRAM)
# 소켓에 포트 번호를 할당
serverSocket.bind( ('',serverPort) )

print('서버가 준비되었습니다.')

while True:
    print('--- 입력 대기중 ---')
    # 서버 소켓이 클라이언트에서 보낸 정보를 받는다. (메시지+주소)
    message, clientAddress = serverSocket.recvfrom(2048)
    # 받은 메시지를 변경하고 서버쪽에서 한번 띄워본다.
    modifiedMessage = message.decode().upper()
    print(modifiedMessage)
    print(clientAddress)
    # 변경된 메시지를 클라이언트 주소로 보낸다.
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    # 서버 소켓 닫기
    serverSocket.close()