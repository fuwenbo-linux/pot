import asyncio

class Banana:
#别问我为什么是香蕉，因为我这会突然想吃
    def __init__(self):
        self.num = 0
        self.readlock = asyncio.Lock()
        self.setlock = asyncio.Lock()
    def read(self):
        print("the num is:%d" %(self.num))
    async def setbanana(self,num):
        '''
        self.num = self.num + num
        await asyncio.sleep(1)
        self.num = self.num - 1
        不加lock的话理论上应该会是4321，中间的锁操作是模拟一下任务过多的情况
        '''
        async with self.setlock:
            self.num = self.num + num
            await asyncio.sleep(1)
            self.num = self.num - 1

    async def run(self):
        await self.setbanana(1)
        self.read()

task = Banana()

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(task.run(), task.run(), task.run(), task.run()))