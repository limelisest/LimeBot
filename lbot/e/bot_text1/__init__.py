from email.headerregistry import Group
import json
import random
from datetime import date
from re import T
from tokenize import group

from nonebot import Bot,on_keyword,on_notice, on_request
from nonebot.adapters.onebot.v11 import Bot,Event,GroupMessageEvent,PrivateMessageEvent,GroupRequestEvent,GroupIncreaseNoticeEvent,GroupDecreaseNoticeEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN,GROUP_MEMBER,GROUP_OWNER,PRIVATE_FRIEND
from nonebot.rule import to_me
from typing import Union

import ast

from pydantic import Json


def luck_simple(num):
    if num < 18:
        return '大吉'
    elif num < 53:
        return '吉'
    elif num < 58:
        return '半吉'
    elif num < 62:
        return '小吉'
    elif num < 65:
        return '末小吉'
    elif num < 71:
        return '末吉'
    else:
        return '凶'


jrrp = on_keyword(['jrrp', '今日人品','抽签'], permission=GROUP_OWNER | GROUP_ADMIN|GROUP_MEMBER, rule=to_me())
@jrrp.handle()
async def jrrp_handle(bot:Bot,event:Event,gr:GroupMessageEvent):
    rnd=random.Random()
    rnd.seed(int(date.today().strftime("%y%m%d"))+int(event.get_user_id()))
    lucknum = rnd.randint(1,100)
    await jrrp.finish(Message(f'[CQ:at,qq={event.get_user_id()}]您今日的幸运指数是{lucknum}/100,为"{luck_simple(lucknum)}"'))



# test1 = on_keyword("test1",permission=GROUP_OWNER|GROUP_ADMIN|PRIVATE_FRIEND)
# @test1.handle()
# async def test1_handle(bot:Bot,event: Union[PrivateMessageEvent, GroupMessageEvent]):
    
#     # data = await bot.call_api("get_group_info", **{
#     #     'group_id':event.group_id
#     # })
#     # data = ast.literal_eval(str(data))
#     # msg = f"群号  ：{data['group_id']}\
#     #         \n群名称：{data['group_name']}\
#     #         \n成员数：{data['member_count']}"

#     if isinstance(event,PrivateMessageEvent):
#         await test1.finish(Message(f'{event.user_id}'))
#     if isinstance(event,GroupMessageEvent):
#         numdata = await bot.call_api("get_group_member_list", **{
#             'group_id': event.group_id
#         })
#         numdata = ast.literal_eval(str(numdata))
#         msg = "成员:\n"
#         for info in numdata:
#             msg += f"{info['user_id']}\n"
#         await test1.finish(Message(f'群号:{event.group_id}\n{msg}'))

'''
群员增加消息:GroupIncreaseNoticeEvent
群员减少消息:GroupDecreaseNoticeEvent
    字段名	     数据类型  可能的值(减少)	    说明(减少)
    time	    number  (int64)		        事件发生的时间戳
    self_id	    number  (int64)		        收到事件的机器人 QQ 号
    post_type	string	 notice	            上报类型
    notice_type	string	 group_increase	    通知类型
    sub_type	string	 approve、invite	事件子类型，分别表示管理员已同意入群、管理员邀请入群
                     -leave、kick、kick_me  事件子类型，分别表示主动退群、成员被踢、登录号被踢
    group_id	number  (int64)		        群号
    operator_id	number  (int64)		        操作者 QQ 号、如果是自己退出的为user_id
    user_id	    number  (int64)		        加入(退出)者 QQ 号
'''   
test2 = on_notice()
@test2.handle()
async def test2_handle(bot: Bot, event: Union[GroupIncreaseNoticeEvent,GroupDecreaseNoticeEvent]):
    raw = json.loads(event.json())
    t =raw['time']
    sid=raw['self_id']
    stype=raw['sub_type']
    gid=raw['group_id']
    opid=raw['operator_id']
    uid=raw['user_id']

    '''{t}\n{sid}\n{stype}\n{opid}\n{uid}'''
    await bot.call_api("send_group_msg",**{
        'group_id':gid,
        'message':f'{t}\n{sid}\n{stype}\n{opid}\n{uid}'
    })

