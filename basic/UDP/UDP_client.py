from socket import *

# 클라이언트가 무언가 보낼 '서버'의 주소+포트
serverName = 'localhost'
serverPort = 12000

# 클라이언트 소켓 생성 (UDP)
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input('영어 소문자를 입력하세요 : ')

# 입력이 완료되면 소켓이 메시지를 sendto(데이터, (서버ip, 포트)) 메소드로 서버에 보낸다.
print('보내는 중....')
clientSocket.sendto(message.encode(), (serverName, serverPort) )

# 그리고 소켓이 다시 변경된 메시지를 받는다. (서버 주소도 받는다.)
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print('서버에서 수정된 메시지 : ' + modifiedMessage.decode()) 
print(serverAddress)

# 소켓 닫기.
clientSocket.close()






# 굳이 왜 try를 쓴거지?
# try :
#     print('보내는 중....')
#     clientSocket.sendto(message.encode(), (serverName, serverPort) )
#     modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
#     print(modifiedMessage.decode())
# finally:
#     print('-------------')
#     clientSocket.close()