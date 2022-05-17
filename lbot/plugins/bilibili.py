from nonebot import Bot, get_driver, require
from bilibili_api.live import LiveRoom
from bilibili_api import Credential


SESSDATA = "2b25d162%2C1659958362%2Ca6de3%2A21"
BILI_JCT = "8a02b6b5ddbdae362ffd57b1836f599e"
BUVID3 = "AUTO6916444063509430"
credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
lr = LiveRoom(10413051,credential)

num = {
     'num1': 0,
     'num2': 0
}

readnum1 = require("nonebot_plugin_apscheduler").scheduler
@readnum1.scheduled_job("cron", hour=22,minute=35)
async def loadnum1():
    num['num1'] = await get_dahanghai_num()


readnum2 = require("nonebot_plugin_apscheduler").scheduler
@readnum2.scheduled_job("cron", hour=22, minute=36)
async def loadnum2():
    num['num2'] = await get_dahanghai_num()
    driver = get_driver()
    BOT_ID = str(driver.config.bot_id)
    bot = driver.bots[BOT_ID]
    c = num['num1']-num['num2']
    await bot.send_group_msg(group_id='188937258', message=f'今日掉舰{c}人')



async def get_dahanghai_num():
    data = await lr.get_dahanghai()
    return data['info']['num']
