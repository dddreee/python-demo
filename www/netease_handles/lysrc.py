
import requests
import asyncio


from util.netease_crypto import *



def seach_lysrc(request):
    return encrypted_request(request)

# loop = asyncio
print( seach_lysrc({}))