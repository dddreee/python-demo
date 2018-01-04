import orm
import asyncio
from models import User, Comment, Blog

async def test(loop):
    await orm.create_pool(loop=loop, port=3306, user='www-data', password='www-data', db='awesome')
    u = User(name='Test', email='test@example.com', passwd='123456', image='about:blank')
    await u.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()