from socket import *

# 클라이언트가 무언가 보낼 '서버'의 주소+포트
serverName = 'localhost'
serverPort = 12000

# 클라이언트 소켓 생성 (TCP)
clientSocket = socket(AF_INET, SOCK_STREAM)
# 클라이언트 소켓을 서버 소켓과 미리 연결 (3 way hand-shaking )
clientSocket.connect( (serverName, serverPort) )

message = input('영어 소문자를 입력하세요 : ')

# 입력이 완료되면 소켓이 메시지를 '미리 연결된' 서버에 보낸다.
print('보내는 중....')
clientSocket.send(message.encode())

# 그리고 소켓이 다시 변경된 메시지를 받는다.
modifiedMessage = clientSocket.recv(1024)
print('서버에서 수정된 메시지 : ' + modifiedMessage.decode()) 

# 소켓 닫기.
clientSocket.close()


