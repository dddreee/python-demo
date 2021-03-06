#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import datetime

async def demo(loop):
    print('handle start...')
    print(loop.time())
    later = loop.call_at(loop.time() + 1, delayFunc)
    print(dir(later))
    
    await asyncio.sleep(2)
    print(loop.time())
    print('handle complete')


def delayFunc():
    print('run delayFunc...after 1s')
    print(loop.time())




def display_date(end_time, loop):
    print(datetime.datetime.now())
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, display_date, end_time, loop)
    else:
        loop.stop()

loop = asyncio.get_event_loop()

# Schedule the first call to display_date()
end_time = loop.time() + 5.0
loop.call_soon(display_date, end_time, loop)

# Blocking call interrupted by loop.stop()
loop.run_forever()
loop.close()
