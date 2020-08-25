'''
完整版
'''
import socket
import select
from preLogging import getLogger as logger

'''
    自定义的类型
'''
logger = logger("Tcprecord","app.log")
LISTEN_PORT=9877
LIMIT_CONNECT =32
SOCKET_TIMEOUT = 120

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setblocking(True)
s.bind((s.getsockname()[0], LISTEN_PORT))
s.listen(5)
logger.info("the tcp server is listening on %s:%d",s.getsockname()[0],LISTEN_PORT)
logger.warning("now that can build a select socket and wish me can build successfully in a first time")

#s为监听套接字
read_server = [s]
write_server = []
exception_server = []
time_sock={}
counter =1
while 1:
    #readySocket只记录准备好的套接字
    readySocket = read_server
    readsocket,writeable,exception = select.select(readySocket,write_server,exception_server,SOCKET_TIMEOUT)
    if not readsocket:
        #maybe it is a deny attck!we can detect it and record it right now!
        for attack_server in read_server:
            if attack_server == s:
                continue
            else:
                #超时就关闭
                logger.warning("the server in %s:%d maybe use a deny attack!",attack_server.getpeername()[0],attack_server.getpeername()[1])
                read_server.remove(attack_server)
                attack_server.close()
                #print(attack_server)
    for rd_server in readsocket:
        if rd_server.fileno() == s.fileno():
            if len(read_server) <= LIMIT_CONNECT-1:
                cli,addr = s.accept()
                logger.info("client login the listening list %s:%d",addr[0],addr[1])
                read_server.append(cli)
            else:
                #deal too many socket and we set the MAX limition is 32
                cli, addr = s.accept()
                data = ("there too many conntion and please connection soon.....").encode()
                cli.send(data)
                cli.close()

        else:
            data = rd_server.recv(1024)
            if not data:
                logger.warning("the %s:%d closed the connection....",rd_server.getpeername()[0],rd_server.getpeername()[1])
                read_server.remove(rd_server)
                rd_server.close()
            else:
                logger.warning("receive %s from %s:%d", data, rd_server.getpeername()[0], rd_server.getpeername()[1])

s.close()



