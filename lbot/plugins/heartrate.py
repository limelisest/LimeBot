from nonebot import Bot, on_regex
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, PrivateMessageEvent
from nonebot.adapters.onebot.v11.permission import PRIVATE_FRIEND, GROUP_MEMBER
from nonebot.adapters.onebot.v11.message import Message
from datetime import datetime
import requests
import re
import datetime
from dateutil.parser import parse
api_list = [
    {
        'name': '匣子',
        'api': 'https://pulsoid.net/v1/api/feed/c2d4e49f-b290-4054-843a-c3e928d5eee5'
    },
    {
        'name': '镜子',
        'api': 'https://pulsoid.net/v1/api/feed/c6da8d72-29c2-41ea-a380-2478c3a6a00a'
    },
    {
        'name': '月里',
        'api': 'https://pulsoid.net/v1/api/feed/df6f31c1-5c81-4c78-8f12-3919a0ce46e2'
    },
    {
        'name': '诺诺',
        'api': 'https://pulsoid.net/v1/api/feed/8c78a9fb-e1da-4870-9a2a-6b079e7716c1'
    },
    {
        'name': '沂辰',
        'api': 'https://pulsoid.net/v1/api/feed/853d0814-5c5e-49d9-8980-822be88271ce'
    },
    {
        'name': '58',
        'api': 'https://pulsoid.net/v1/api/feed/1a48d2c4-5135-4cf4-8ac5-c64500139ca1'
    },
    {
        'name': '咩夸',
        'api': 'https://pulsoid.net/v1/api/feed/2961249e-e56b-4ef8-ac9c-65508a02e04a'
    },
    {
        'name': '梦星辰',
        'api': 'https://pulsoid.net/v1/api/feed/d2673ec9-a81b-408c-9c21-4f535ad5e6a6'
    },
    {
        'name': '量子',
        'api': 'https://pulsoid.net/v1/api/feed/5562fd88-4ad5-4656-8ffd-f050a93958d6'
    },
    {
        'name': 'xz',
        'api': 'https://pulsoid.net/v1/api/feed/c4a3694e-55a8-49c3-8336-0d68c172d85c'
    },
]   
myheartrate = on_regex(
    r'^#查[看询]匣子心[跳率]$|^#查[看询]镜子心[跳率]$|^#查[看询]月里心[跳率]$|^#查[看询]诺诺心[跳率]$|^#查[看询]主播心[跳率]$|^#查[看询]沂辰心[跳率]$|^#查[看询]58心[跳率]$|^#查[看询]老头心[跳率]$|^#查[看询]咩夸心[跳率]$|^#查[看询]梦星辰心[跳率]$|^#查[看询]量子心[跳率]$|^#查[看询]xz心[跳率]$')


@myheartrate.handle()
async def myheartrate_handle(bot: Bot, gevent: GroupMessageEvent):
    id = -1
    if re.compile(r'^#查[看询]匣子心[跳率]$').match(str(gevent.message)):
        id = 0
    elif re.compile(r'^#查[看询]镜子心[跳率]$').match(str(gevent.message)):
        id = 1
    elif re.compile(r'^#查[看询]月里心[跳率]$').match(str(gevent.message)):
        id = 2
    elif re.compile(r'^#查[看询]诺诺心[跳率]$|^#查[看询]主播心[跳率]$').match(str(gevent.message)):
        id = 3
    elif re.compile(r'^#查[看询]沂辰心[跳率]$').match(str(gevent.message)):
        id = 4
    elif re.compile(r'^#查[看询]58心[跳率]$|^#查[看询]老头心[跳率]$').match(str(gevent.message)):
        id = 5
    elif re.compile(r'^#查[看询]咩夸心[跳率]$').match(str(gevent.message)):
        id = 6
    elif re.compile(r'^#查[看询]梦星辰心[跳率]$').match(str(gevent.message)):
        id = 7
    elif re.compile(r'^#查[看询]量子心[跳率]$').match(str(gevent.message)):
        id = 8
    elif re.compile(r'^#查[看询]xz心[跳率]$').match(str(gevent.message)):
        id = 9
    name=api_list[id]["name"]
    try:
        
        data = requests.get(api_list[id]["api"], timeout=5)
        jsom_data = data.json()
        bpm=jsom_data["bpm"]
        measured_at = jsom_data["measured_at"]
        #2022-05-12T18:12:00.092Z
        UTC_time = str((parse(measured_at)+datetime.timedelta(hours=8)))[11:16]
        await myheartrate.finish(Message(f'[{UTC_time}]{name}的心率为：{bpm}bpm'))
    except requests.exceptions.ConnectTimeout:
        await myheartrate.finish(Message(f'读不到{name}的心率，所以猜测大概是寄了。'))