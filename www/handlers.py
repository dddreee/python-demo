' url handlers '

import re
import time
import json
import logging
import hashlib
import base64
import asyncio

from coroweb import get, post

from models import User, Comment, Blog, next_id

from netease_handles.lysrc import seach_lysrc

@get('/')
async def index(request):
    logging.info('request => %s' % (request.json()))
    users = await User.findAll()
    logging.info('  users => %s' % users)
    return {
        '__template__': './test/test.html',
        'users': users
    }

@post('/test')
async def test(*, id):
    
    return (await seach_lysrc(id))
    

@get('/api/user')
async def api_get_user(request):
    users = await User.findAll()
    for u in users:
        u.passwd = '******'
    
    return dict(users = users)