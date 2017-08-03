"""
Author:weizhanfei
Created:2017/7/26
Purpose:
"""

import asyncio
import os


@asyncio.coroutine
async def co(command):
    # print("Looking for %s" % command)
    await asyncio.sleep(0)
    return os.popen(command).readlines()




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(100):
        tasks.append(asyncio.ensure_future(co("adb -s GSLDU16716015230 shell top -n 1 |findstr com.hele.buyer")))
    loop.run_until_complete(asyncio.wait(tasks))
    for task in tasks:
        print('Task ret: ', task.result())

    loop.close()
