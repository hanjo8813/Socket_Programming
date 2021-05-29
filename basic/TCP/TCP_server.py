from socket import *

# 포트 번호
serverPort = 12000
# 소켓 생성하기
serverSocket = socket(AF_INET, SOCK_STREAM)
# 소켓에 포트 번호를 할당
serverSocket.bind( ('',serverPort) )
# 서버 소켓을 열어두기
serverSocket.listen(1)


print('서버가 준비되었습니다.')

while True:
    print('--- 입력 대기중 ---')
    # 현재 서버소켓에 연결된 소켓(클)을 추출
    clientSocket, addr = serverSocket.accept()
    # 해당 소켓에서 메시지를 받음
    message = clientSocket.recv(1024)
    # 메시지 변경 후 서버측에서 띄워보자
    modifiedMessage = message.decode().upper()
    print(modifiedMessage)
    # 변경된 메시지를 연결된 소켓(클)에 전송
    clientSocket.send(modifiedMessage.encode())
    # 연결 소켓 닫기
    clientSocket.close()
