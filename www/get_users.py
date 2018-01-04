import requests
import json
import asyncio

async def getUsers():
    r = requests.get('https://api.github.com/search/users?q=followers:>1000+location:china&page=1')
    data = dict(r.json())
    users = data['items'];
    total_count = data['total_count']
    if total_count % 30 == 0:
        pages = total_count / 30
    else:
        pages = int(total_count / 30) + 1

    for n in range(pages):
        next_data = requests.get('https://api.github.com/search/users?q=followers:>1000+location:china&page=' + str(n + 2))
        users.extend(dict(next_data.json())['items'])

    print(pages)
    return {'users': users}

    

    
    
    return r

loop = asyncio.get_event_loop()
r = loop.run_until_complete(getUsers())

with open('user.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(r))

# print(r.json())


