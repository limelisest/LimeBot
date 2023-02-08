import ast
from itertools import count
from tokenize import group
from loguru import logger
from nonebot import on_message, on_regex,on_command
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, PrivateMessageEvent
from nonebot.adapters.onebot.v11.permission import PRIVATE_FRIEND, GROUP_MEMBER
from nonebot.adapters.onebot.v11.message import Message

title = on_command('我想要一个一个头衔叫', priority=1, block=True)
@title.handle()
async def _(bot:Bot,event:GroupMessageEvent):
    if f'{event.group_id}' in ['756508792']:
        msg=str(event.get_message())
        #需要的头衔
        stitle=msg.split('我想要一个一个头衔叫')[-1].replace(' ','') 
        #读取真字符串长度
        lenTxt = len(stitle) 
        lenTxt_utf8 = len(stitle.encode('utf-8')) 
        stitle_size = int((lenTxt_utf8 - lenTxt)/2 + lenTxt)

        uid=event.get_user_id()#用户ID
        #获取申请人的等级
        temp = await bot.get_group_member_info(group_id=event.group_id,user_id=uid,no_cache=True)
        temp = ast.literal_eval(str(temp))
        ntitle=temp['title']
        #判断是否拥有头衔
        if ntitle is '':
            #判断字符串长度
            if 0 <stitle_size<=12:
                await bot.set_group_special_title(
                    group_id=event.group_id,
                    user_id=uid,
                    special_title=stitle,
                    duration=-1,
                )
                await title.finish(Message(f'现在你的头衔是[{stitle}]了！'))
            elif stitle_size == 0 :
                await title.finish(Message(f'申请格式：\n \\我想要一个一个头衔叫[头衔]\n例子：\我想要一个一个头衔叫 我是猪'))
            else:
                await title.finish(Message(f'你这个有点长，要不再想想？'))
        else:
            await title.finish(Message(f'你已经有了头衔了，唉嘿~'))
        
