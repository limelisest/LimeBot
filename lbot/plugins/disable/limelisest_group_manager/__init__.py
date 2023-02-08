from nonebot import Bot, get_driver, on_notice, on_request, on_keyword
from nonebot.adapters.onebot.v11.event import GroupRequestEvent, GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent, PrivateMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER, PRIVATE_FRIEND
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11.message import Message
from .Base_v2 import *
import nonebot
import asyncio
su = nonebot.get_driver().config.superusers
#group_enable_list = ['209986093', '599342554', '726031097']
group_enable_list=['188937258','756508792']

async def start_init():
    driver = get_driver()
    BOT_ID = str(driver.config.bot_id)
    ot = driver.bots[BOT_ID]
    bot=Bot()
    await init(group_enable_list, bot)

asyncio.run(start_init())

admin_init = on_keyword(['$reset'], permission=SUPERUSER | PRIVATE_FRIEND)
@admin_init.handle()
async def admin_init_handle(bot: Bot, event: PrivateMessageEvent):
    await init(group_enable_list, bot)
    await admin_init.finish(Message(f'群员列表初始化完成'))


get_list = on_keyword(['$loadlist'],permission=SUPERUSER | PRIVATE_FRIEND)
@get_list.handle()
async def get_list_handle(bot:Bot,event:PrivateMessageEvent):
    list1=[]
    list_temp = await bot.call_api('get_group_member_list', **{
        'group_id': '743148064'
    })
    list_temp = ast.literal_eval(str(list_temp))  # 转换数据格式
    for userid in list_temp:  # 写入名单
        list1.append(f'{userid}')
    list1=set(list1)

    list2=[]
    list_temp = await bot.call_api('get_group_member_list', **{
        'group_id': '1025168527'
    })
    list_temp = ast.literal_eval(str(list_temp))  # 转换数据格式
    for userid in list_temp:  # 写入名单
        list2.append(f'{userid}')
    list2=set(list2)

    await bot.send_msg(user_id='3090839937',message=f'{list1.intersection(list2)}')

join_group_request = on_request()


@join_group_request.handle()
async def join_group_request_handle(bot: Bot, event: GroupRequestEvent):
    if f'{event.group_id}' in group_enable_list:
        await check_userid_in_list(bot, event)

user_join_group = on_notice()


@user_join_group.handle()
async def user_join_group_handle(bot: Bot, event: GroupIncreaseNoticeEvent):
    if f'{event.group_id}' in group_enable_list:
        await add_userid_in_list(bot, event)

user_exit_group = on_notice()


@user_exit_group.handle()
async def user_exit_group_handle(bot: Bot, event: GroupDecreaseNoticeEvent):
    if f'{event.group_id}' in group_enable_list:
        await del_userid_in_list(bot, event)


