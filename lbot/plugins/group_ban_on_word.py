import re
from nonebot import on_regex,logger,on_message
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
'''
功能：检测到关键词后自动禁言
'''
ban_word=on_regex(re.compile(r'透[你我]|[让给]我透|[想被挨]透|透死你'))
@ban_word.handle()
async def _(bot:Bot,event:GroupMessageEvent):
    if f'{event.group_id}' in ['756508792','726031097']:
        await bot.set_group_ban(
            group_id=event.group_id,
            user_id=event.user_id,
            duration=10*60
            )