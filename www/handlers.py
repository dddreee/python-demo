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

async def netease_request(host, path, method='post', data={}):
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
    url = 'http://%s%s' % (host, path)

    logging.info('  ============ API ==========')
    logging.info('  %s' % url)
    
    
    async with aiohttp.ClientSession() as session:
        if method == 'post':

            async with session.post(url, data=data, headers=headers) as res:
                return res
        elif method == 'get':
            async with session.get(url, params=data, headers=headers) as res:
                return res

@get('/')
async def index(request):
    logging.info('request => %s' % (request.json()))
    users = await User.findAll()
    logging.info('  users => %s' % users)
    return {
        '__template__': './test/test.html',
        'users': users
    }

@get('/api/search_songs')
async def search_songs(*, keywords, limit=30, type=1, offset=0):
    request_data = {
        'csrf_token': '',
        'limit': limit,
        'type': type,
        's': keywords,
        'offset': offset
    }
    logging.info('  ============ REQ ==========')
    logging.info('  %s' % request_data)
    param = encrypted_request(request_data)

    res = await netease_request(
        'music.163.com',
        '/weapi/search/get',
        'post',
        param
    )
    data = await res.text()
    logging.info('  ============ RES ==========')
    logging.info('  %s' % data)
    return json.loads(data)
    


@get('/api/download_lrc')
async def test(*, request, id, name='这是歌词'):
    logging.info('  param id => {}'.format(id))
    param = encrypted_request({})
    res = await netease_request(
        'music.163.com',
        '/weapi/song/lyric?csrf_token=&os=osx&lv=-1&kv=-1&tv=-1&id=%s' % str(id),
        'post',
        param
        )
    data = json.loads(await res.text())
            
    lrc = data['lrc']['lyric'].encode('utf-8')
    res = web.StreamResponse()
    res.content_type = 'application/octet-stream'
    res.headers['CONTENT-DISPOSITION'] = 'attachment;filename=%s.lrc' % name

    await res.prepare(request)
    res.write(lrc)
        
    return res


    # async with aiohttp.ClientSession() as session:
        # async with session.post('http://music.163.com/weapi/song/lyric?csrf_token=&os=osx&lv=-1&kv=-1&tv=-1&id='+str(id), data=param, headers=headers) as res:
            
            





@get('/api/user')
async def api_get_user(request):
    users = await User.findAll()
    for u in users:
        u.passwd = '******'
    
    return dict(users = users)