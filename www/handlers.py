' url handlers '

import re
import time
import json
import logging
import hashlib
import base64
import asyncio
import aiohttp
from aiohttp import web
# from aiohttp import web, MultiDict
import os

from coroweb import get, post

from models import User, Comment, Blog, next_id

from netease_handles.util.netease_crypto import encrypted_request


@get('/')
async def index(request):
    logging.info('request => %s' % (request.json()))
    users = await User.findAll()
    logging.info('  users => %s' % users)
    return {
        '__template__': './test/test.html',
        'users': users
    }

@get('/test')
async def test(*, request, id, name='这是歌词'):
    logging.info('  param id => {}'.format(id))
    param = encrypted_request({})
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

    async with aiohttp.ClientSession() as session:
        async with session.post('http://music.163.com/weapi/song/lyric?csrf_token=&os=osx&lv=-1&kv=-1&tv=-1&id='+str(id), data=param, headers=headers) as res:
            data = json.loads(await res.text())
            
            lrc = data['lrc']['lyric'].encode('utf-8')
            res = web.StreamResponse()
            res.content_type = 'application/octet-stream'
            res.headers['CONTENT-DISPOSITION'] = 'attachment;filename=%s.lrc' % name
            # res.enable_chunked_encoding()
            
            await res.prepare(request)
            
            # with open('31284016.lrc', 'rb') as f:
            res.write(lrc)
               
            return res
            

            # return data
            
            # return web.Response(
            #     headers = MultiDict({'Content-Disposition': 'Attachment', 'filename': 'test.lrc'}),
            #     body = lrc.encode('utf-8')
            # )

            # logging.info(os.path.abspath('../31284016.lrc'))
            # res = web.FileResponse('31284016.lrc')
            # res.content_type = 'application/octet-stream'
            # res.headers['Content-Disposition'] = 'Attachment;filename=123.lrc'
            # return res
                
            
        
                
            
            # logging.info('  r.status_code => %s' % res.status_code)
            


@get('/api/user')
async def api_get_user(request):
    users = await User.findAll()
    for u in users:
        u.passwd = '******'
    
    return dict(users = users)