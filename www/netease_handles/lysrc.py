
import requests
import logging
import asyncio


from .util.netease_crypto import *



async def seach_lysrc(request):
    param = encrypted_request({})
    
    logging.info('  data => %s' % param)

    headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'  # NOQA
        }
    
    r = requests.post('http://music.163.com/weapi/song/lyric?id='+str(id), data=json.dumps(param), headers=headers)
    logging.info('  response => %s' % r.text)
    return r

