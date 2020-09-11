import asyncio
from datetime import datetime
'''
1、tcp短连接不需要考虑超时问题
2、tcp长连接需要考虑超时
'''
class myServer(asyncio.Protocol):
    def __init__(self):
        self.timeout = 20
        loop = asyncio.get_running_loop()
        loop.call_later(self.timeout,self._timeout,loop)
    def _timeout(self,loop):
        #循环嵌套一下
        if datetime.timestamp(datetime.now())-self.recent < self.timeout+0.5:
            loop.call_later(self.timeout, self._timeout, loop)
        else:
            print("close the port: ", self.transport.get_extra_info('peername'))
            self.transport.close()
    def connection_made(self, transport):
        self.recent = datetime.timestamp(datetime.now())
        peername = transport.get_extra_info('peername')
        print("Connection from {}".format(peername))
        self.transport=transport
    def data_received(self, data):
        self.recent = datetime.timestamp(datetime.now())
        message = data.decode()
        print("Data received: {!r}".format(message))
        #self.transport.close()
    def connection_lost(self, exc):
        self.transport.close()

async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(myServer,'127.0.0.1',8888)

    async with server:
        await server.serve_forever()


asyncio.run(main())
