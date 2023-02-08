from nonebot import on_request,logger
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupRequestEvent
from nonebot.adapters.onebot.v11.message import Message
import ast
# group_enable_list=['188937258','756508792']
group_enable_list=['209986093','726031097','599342554']
quanjiguanid='743148064'


user_join_group = on_request()
@user_join_group.handle()
async def _(bot: Bot, event: GroupRequestEvent):
    if f'{event.group_id}' in group_enable_list:
        logger.info("插件启动成功")
        white_list=[]#白名单（兔屋拳击馆）
        black_list=[]#黑名单（已经加入群的）
        # #获取兔屋拳击馆群名单
        # userid_list = await bot.call_api('get_group_member_list', **{'group_id': quanjiguanid})  # 从callAPI获取成员列表
        # userid_list = ast.literal_eval(str(userid_list))  # 转换数据格式
        # for userid in userid_list:  # 写入名单
        #     white_list.append(f'{userid["user_id"]}')
        # logger.info('获取兔屋拳击馆名单')
        #获取群成员列表
        for groupid in group_enable_list:
            if f'{groupid}' is not f'{event.group_id}':
                userid_list = await bot.call_api('get_group_member_list', **{
                    'group_id': groupid
                    })  # 从callAPI获取成员列表
                userid_list = ast.literal_eval(str(userid_list))  # 转换数据格式
                for userid in userid_list:  # 写入名单
                    black_list.append(f'{userid["user_id"]}')
        logger.info('获取除了申请群以外的群名单')

        #判断加入的人如果在黑名单里
        if f'{event.user_id}' in black_list:
            await bot.call_api('set_group_add_request',**{
                'flag':event.flag,
                'sub_type':event.sub_type,
                'approve':False,
                'reason':'禁止重复加群(误报请联系匣子@778571299)'
                })
            logger.info(f'在群{event.group_id}拒绝了{event.user_id}')
            # await bot.set_group_add_request(
            #     flag=event.flag,
            #     sub_type=event.sub_type,
            #     approve=False,
            #     reason='禁止重复加群(误报请联系匣子@778571299)')
        logger.info(f'结束')