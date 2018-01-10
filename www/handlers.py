' url handlers '

import re
import time
import json
import logging
import hashlib
import base64
import asyncio
import aiohttp

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
async def test(*, id):
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
        async with session.post('http://music.163.com/weapi/song/lyric?id='+str(id), data=param, headers=headers) as res:
            logging.info('  res.text => %s' % (await res.text()))
            # logging.info('  r.status_code => %s' % res.status_code)
            return res.text

    
    
    

@get('/api/user')
async def api_get_user(request):
    users = await User.findAll()
    for u in users:
        u.passwd = '******'
    
    return dict(users = users)