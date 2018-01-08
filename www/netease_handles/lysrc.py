
import requests
import logging
import asyncio


from .util.netease_crypto import *



async def seach_lysrc(request, loop):
    param = encrypted_request(request)
    logging.info('  data => %s' % param)
    
    r = requests.post('https://music.163.com/weapi/song/lyric?csrf_token=', data=param)
    logging.info('  responese => %s' % r.text)
    return r.text

