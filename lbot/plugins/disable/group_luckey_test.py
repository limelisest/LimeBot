import random
from nonebot import on_message
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.permission import PRIVATE_FRIEND, GROUP_MEMBER

lucklist=[
    {
        'title':'大吉',
        'info':'今天的运气很好呢，打开游戏抽两发说不定就出货了呢？'
    },
    {
        'title':'中吉',
        'info':'今天的运气不错呢，会有好事发生吧！'
    },
    {
        'title':'小吉',
        'info':'今天的运气还行呢，稍微努力一下应该就能得到什么吧！'
    },
]
luck=on_message("抽签")
@luck.handle
def _(bot:Bot,event:GroupMessageEvent):
    i=random.randint(0,2)
    msg=f'你抽到的是{lucklist[i]["title"]}\n{lucklist[i]["info"]}'
    # title=f'{lucklist[i]["title"]}'
    # info=f'{lucklist[i]["info"]}'
    luck.finish(Message(msg))
