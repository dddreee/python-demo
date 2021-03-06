#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    

    # session = aiohttp.ClientSession()
    # res = await session.post(url, data=data, headers=headers)
    # await session.close()
    # logging.info('  =========== res ============')
    # logging.info(' %s' % res.text())
    # session.close()
    # return res
       
    with aiohttp.ClientSession() as session:
        logging.info('  method => %s' % method)
        if method == 'post':

            async with session.post(url, data=data, headers=headers) as res:
                response_data = await res.text()
                logging.info('  =========== res ============')
                logging.info(' %s' % response_data)
                return response_data
                # return res
        elif method == 'get':
            async with session.get(url, params=data, headers=headers) as res:
                response_data = await res.text()
                logging.info('  =========== res ============')
                logging.info(' %s' % response_data)
                return response_data
        
        return res

@get('/')
async def index(request):
    # logging.info('request => %s' % (request.json()))
    # users = await User.findAll()
    # logging.info('  users => %s' % users)
    return {
        '__template__': './lysic/index.html'
    }

@get('/api/search_songs')
async def search_songs(*, keywords, pageSize=30, type=1, page=1):
    if isinstance(page, str):
        page = int(page)
    if isinstance(pageSize, str):
        pageSize = int(pageSize)
    request_data = {
        'csrf_token': '',
        'limit': pageSize,
        'type': type,
        's': keywords,
        'offset': pageSize*(page - 1)
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
    # loop = asyncio.get_event_loop()
    # res = loop.run_until_complete(netease_request(
    #     'music.163.com',
    #     '/weapi/search/get',
    #     'post',
    #     param
    # ))
    # data = await res.text()
    # logging.info('  ============ RES ==========')
    # logging.info('  %s' % data)
    return json.loads(res)
    


@get('/api/download_lrc')
async def download_lrc(*, request, id, name='这是歌词'):
    logging.info('  param id => {}'.format(id))
    param = encrypted_request({})
    res = await netease_request(
        'music.163.com',
        '/weapi/song/lyric?csrf_token=&os=osx&lv=-1&kv=-1&tv=-1&id=%s' % str(id),
        'post',
        param
        )

    try:
        data = json.loads(res)
        if 'nolyric' in data and data['nolyric']:
            return '没有歌词'
        else:

            lrc = data['lrc']['lyric'].encode('utf-8')
            resp = web.StreamResponse()
            resp.content_type = 'application/octet-stream'
            resp.headers['CONTENT-DISPOSITION'] = 'attachment;filename=%s.lrc' % name
            await resp.prepare(request)
            resp.write(lrc)
            return resp
    except KeyError as key_error:
        logging.warning('   KeyError: %s' % str(key_error) )
        
    
         





@get('/api/user')
async def api_get_user(request):
    users = await User.findAll()
    for u in users:
        u.passwd = '******'
    
    return dict(users = users)