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

@get('/')
async def index(request):
    users = await User.findAll()
    logging.info('  users => %s' % users)
    return {
        '__template__': './test/test.html',
        'users': users
    }