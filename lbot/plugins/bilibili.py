from bilibili_api.live import LiveRoom
from bilibili_api import sync,Credential
import time
import os
import json
SESSDATA = "2b25d162%2C1659958362%2Ca6de3%2A21"
BILI_JCT = "8a02b6b5ddbdae362ffd57b1836f599e"
BUVID3 = "AUTO6916444063509430"
credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
lr = LiveRoom(10413051,credential)

filename = "./data/bilibili_dahanghai_daily/data.csv"

async def main():
    data=f'{time.strftime("%Y%m%d")},{get_dahanghai_num()}\n'
    
    

async def get_dahanghai_num():
   return await lr.get_dahanghai()['info']['num']

sync(main())