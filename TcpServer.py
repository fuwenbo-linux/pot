'''
最基本功能的tcp服务器
暂时不包括超时监测
'''
import socket
import select
from preLogging import getLogger as logger

logger = logger("Tcprecord","app.log")
LISTEN_PORT=9877

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setblocking(0)
s.bind((s.getsockname()[0], LISTEN_PORT))
s.listen(5)
logger.info("the tcp server is listening on %s:%d",s.getsockname()[0],LISTEN_PORT)
logger.warning("now that can build a select socket and wish me can build successfully in a first time")

#s为监听套接字
read_server = [s]
write_server = []
exception_server = []
while 1:
    readySocket = read_server
    readsocket,writeable,exception = select.select(readySocket,write_server,exception_server)
    if readsocket is not None:
        for server in readsocket:
            if server==s:
                cli,addr = s.accept()
                #cli.setblocking(0)
                logger.warning("%s:%d connect on server....",addr[0],addr[1])
                read_server.append(cli)
            else:
                ip,port = server.getpeername()
                data = server.recvfrom(1024)
                logger.warning("the client %s:%d send message is : %s", ip,
                               port,data)

s.close()



