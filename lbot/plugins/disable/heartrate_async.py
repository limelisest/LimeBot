from nonebot import Bot, on_regex
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, PrivateMessageEvent
from nonebot.adapters.onebot.v11.permission import PRIVATE_FRIEND, GROUP_MEMBER
from nonebot.adapters.onebot.v11.message import Message
from datetime import datetime,timezone
import requests
import re
import datetime
from dateutil.parser import parse
globalwhilelist=['']
api_list = [
    {
        'name': '匣子',
        'api': 'https://pulsoid.net/v1/api/feed/c2d4e49f-b290-4054-843a-c3e928d5eee5',
    },
    {
        'name': '镜子',
        'nickname':'镜宝',
        'api': 'https://pulsoid.net/v1/api/feed/c6da8d72-29c2-41ea-a380-2478c3a6a00a'
    },
    {
        'name': '月里',
        'api': 'https://pulsoid.net/v1/api/feed/df6f31c1-5c81-4c78-8f12-3919a0ce46e2'
    },
    {
        'name': '诺诺',
        'nickname':'主播',
        'api': 'https://pulsoid.net/v1/api/feed/8c78a9fb-e1da-4870-9a2a-6b079e7716c1'
    },
    {
        'name': '沂辰',
        'api': 'https://pulsoid.net/v1/api/feed/853d0814-5c5e-49d9-8980-822be88271ce'
    },
    {
        'name': '58',
        'nickname':'老头',
        'api': 'https://pulsoid.net/v1/api/feed/1a48d2c4-5135-4cf4-8ac5-c64500139ca1'
    },
    {
        'name': '咩夸',
        'api': 'https://pulsoid.net/v1/api/feed/2961249e-e56b-4ef8-ac9c-65508a02e04a'
    },
    {
        'name': '梦星辰',
        'api': 'https://pulsoid.net/v1/api/feed/124ffd74-52ee-4655-916a-0c04aa84dc28'
    },
    {
        'name': '量子',
        'api': 'https://pulsoid.net/v1/api/feed/5562fd88-4ad5-4656-8ffd-f050a93958d6'
    },
    {
        'name': 'xz',
        'api': 'https://pulsoid.net/v1/api/feed/c4a3694e-55a8-49c3-8336-0d68c172d85c'
    },
    {
        'name': '逸糸',
        'api': 'https://pulsoid.net/v1/api/feed/aa7d672c-2481-464e-9b7a-d383bb71f4f5'
    },
    {
        'name': '风汁子',
        'api': 'https://pulsoid.net/v1/api/feed/c35a89e6-80c3-4e8e-9a84-f169528cde6a',
        'onlwhilelist': ['286339601']
    },
    {
        'name': '绿坝',
        'api': 'https://pulsoid.net/v1/api/feed/16e75d0c-fcb4-4a03-b2ae-ba7f50979002',
    },
]   
#把列表的名字都加入到namestr用于配对
namestr=''
for i in range(len(api_list)):
    namestr +=api_list[i]['name']
    if 'nickname' in api_list[i]:
        namestr +='|'+ api_list[i]['nickname']
    if i < len(api_list)-1:
        namestr += '|'
myheartrate = on_regex(re.compile(r'^#查[看询]('+namestr+')心[跳率]$'))
@myheartrate.handle()
async def myheartrate_handle(bot: Bot, gevent: GroupMessageEvent):
    id = -1
    for i in range(len(api_list)):
        if 'nickname' in api_list[i]:
            if re.compile(r'^#查[看询]('+api_list[i]['name']+'|'+api_list[i]['nickname']+')心[跳率]$').match(str(gevent.message)):
                id=i
        else:
            if re.compile(r'^#查[看询]'+api_list[i]['name']+'心[跳率]$').match(str(gevent.message)):
                id = i
    name=api_list[id]["name"]
    try:
        data = requests.get(api_list[id]["api"], timeout=5)
        jsom_data = data.json()
        bpm=jsom_data["bpm"]
        measured_at = jsom_data["measured_at"]
        UTC_time = (parse(measured_at)+datetime.timedelta(hours=8))
        now_time=datetime.datetime.now()
        dhour=int(now_time.hour)-int(UTC_time.hour)
        dminute=int(now_time.minute)-int(UTC_time.minute)
        dday=int(now_time.day)-int(UTC_time.day)
        dmonth=int(now_time.month)-int(UTC_time.month)
        dhourstr=''
        if dminute < 0:
            dminute +=60
            dhour -=1
        if dhour < 0 :
            dhour +=24
            dday -=1
        if dhour !=0:
            dhourstr=f'{dhour}小时'
        if dmonth == 0:
            if dday <= 0:
                if dhour == 0 and dminute == 0:
                    await myheartrate.finish(Message(f'现在{name}的心率为：{bpm}bpm'))
                else:
                    await myheartrate.finish(Message(f'{dhourstr}{dminute}分钟前{name}的心率为：{bpm}bpm'))
            else:
                await myheartrate.finish(Message(f'{name}已经寄了大概{dday}天辣！！'))
        else:
            await myheartrate.finish(Message(f'{name}从上个月寄到了现在！'))
    except requests.exceptions.ConnectTimeout:
        await myheartrate.finish(Message(f'读不到 {name} 的心率，所以猜测大概是寄了。'))

async def get_apidata(api):
    try:
        json_data = requests.get(api["api"], timeout=5).json()
        return json_data
    except requests.exceptions.ConnectTimeout:
        return False
