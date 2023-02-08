from email.message import Message
from glob import glob
from nonebot import on_regex,logger,on_message,on_command,get_driver,get_bots
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from bilibili_api import user, sync,Credential
from bilibili_api.live import LiveRoom
import nest_asyncio
#允许多线程回环
nest_asyncio.apply()
#定时任务
from nonebot import require
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
#基础信息
SESSDATA = "2b25d162%2C1659958362%2Ca6de3%2A21"
BILI_JCT = "8a02b6b5ddbdae362ffd57b1836f599e"
BUVID3 = "AUTO6916444063509430"

# 提醒列表
live_list=[
    {
        'user':313248263,# 宇佐紀
        'group':[188937258,756508792],
        'atall':True,
    },
    {
        'user':1816653243,# 棉花糖ame
        'group':[188937258,756508792],
        'atall':False,
    },
    {
        'user':505794,# 冰奶茶
        'group':[188937258,756508792],
        'atall':False,
    },
    {
        'user':5558249,# 天才匣子
        'group':[188937258,756508792],
        'atall':True,
    }
]
# 直播状态初始化
flag=[]
for item in live_list:
        u = user.User(item['user'])
        u_info=sync(u.get_live_info())
        live_statue=u_info['live_room']['liveStatus']#直播状态
        if live_statue:
            flag += [1]
        else:
            flag += [0]

# 定时检测函数
async def check_live():
    bot,=get_bots().values()
    id=0
    for item in live_list:
        u = user.User(item['user'])
        u_info=sync(u.get_live_info())
        name=u_info['name']#主播名字
        live_statue=u_info['live_room']['liveStatus']#直播状态
        cover=u_info['live_room']['cover']#直播封面
        title=u_info['live_room']['title']#直播标题
        url=u_info['live_room']['url'].split('?')[0]#直播地址
        await live_listener(bot,id,live_statue,name,cover,title,url)
        id +=1


# 检查开播
async def live_listener(bot,id,live_statue,name,cover,title,url):
    global flag
    group=live_list[id]['group']
    atall=live_list[id]['atall']

    if live_statue:
        if flag[id] == 0:
            for i in group:
                msg=f"【开播提醒】{name}开播啦,{title}\n[CQ:image,file={cover}]\n直播地址：{url}\n"
                if atall :
                    msg +='[CQ:at,qq=all]'
                await bot.send_group_msg(group_id=i,message=msg)
            flag[id] = 1
    else:
        if flag[id] == 1:
            for i in group:
                await bot.send_group_msg(group_id=i,message=f"【下播提醒】 {name} 下播惹~")
            flag[id] = 0

#直播状态查询
scheduler.add_job(check_live,"interval", seconds=10, id="biliStream", misfire_grace_time=90)
