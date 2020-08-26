import asyncio
'''
    凡是涉及读写操作的都尝试着进行async吧
'''
MAX_CON = 64
CURR_CON = 0
async def Read(reader):
    data = await reader.read(1024)
    return data

async def handle_echo(reader, writer):
    global MAX_CON,CURR_CON
    CURR_CON = CURR_CON+1
    while 1:
        if CURR_CON >= MAX_CON:
            CURR_CON = CURR_CON-1
            print("客户连接数已经满")
            break;
        #用read接收bytes流的数据
        try:
            #预防阻塞攻击
            data = await asyncio.wait_for(Read(reader) ,timeout =100)
        except asyncio.TimeoutError:
            print("用户没有任何信息，可能有拒绝服务攻击关闭套接字")
            break;
        #data = await reader.read(1024)
        #data = await reader.read(1024)
        if data:
            message = data.decode()
            addr = writer.get_extra_info('peername')
            print(f"Received {message!r} from {addr!r}")
        else:
            break
    print("the connection disconnect %s:%d"%(writer.get_extra_info('peername')[0],writer.get_extra_info('peername')[1]))
    CURR_CON = CURR_CON - 1
    print("there is remain %d connection......" %CURR_CON)
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)
    #本质跟I/O差不多都是注册到里面了
    #print(server.sockets[0].fileno())

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())