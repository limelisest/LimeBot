from random import random
from nonebot import on_command,logger
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupRequestEvent
from nonebot.adapters.onebot.v11.message import Message

# eatWhat=on_command('今天吃什么', priority=1, block=True)
# @eatWhat.handle()
# async def _(bot:Bot):
#     n=random()