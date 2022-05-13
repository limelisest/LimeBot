import ast
import os
from time import sleep
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupRequestEvent, GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent


path = './data/limeliset_group_manager/grouplist'
jianzhang_group='743148064'
useridlist = []
jianzhang_list=[]
async def init(group, bot: Bot):
    global groupidlist
    global jianzhang_list
    groupidlist = group
    # 判断文件是否存在,不存在则创建
    for groupid in groupidlist:
        filename = f'{groupid}.json'
        # 检索文件路径是否存在
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        # 重新创建文件格式：[群号].json
        if os.path.exists(f'{path}/{filename}'):
            os.remove(f'{path}/{filename}')
        if not os.path.exists(f'{path}/{filename}'):
            with open(f'{path}/{filename}', 'w', encoding='utf-8') as file:
                file.close
        
        file = open(f'{path}/{filename}', 'a+', encoding='utf-8')
        # 刷新文件里的成员列表
        userid_list = await bot.call_api('get_group_member_list', **{
            'group_id': groupid
        })  # 从callAPI获取成员列表
        userid_list = ast.literal_eval(str(userid_list))  # 转换数据格式
        for userid in userid_list:  # 写入名单
            file.write(f'{userid["user_id"]}\n')
        file.close()
    
    #读取舰长列表
    userid_list = await bot.call_api('get_group_member_list', **{
        'group_id': groupid
    })  # 从callAPI获取成员列表
    userid_list = ast.literal_eval(str(userid_list))  # 转换数据格式
    for userid in userid_list:  # 写入名单
        jianzhang_list.append(userid)
    
    load_useridlist()


def load_useridlist():
    global useridlist
    global groupidlist
    useridlist.clear()
    for groupid in groupidlist:
        filename = f'{groupid}.json'
        file = open(f'{path}/{filename}', 'r', encoding='utf-8')
        data = file.read()  # 读取文件内容
        for line in data.split('\n'):  # 通过换行符分割
            if line != '':  # 排除空内容
                useridlist.append(line)
        file.close()
    



async def check_userid_in_list(bot: Bot, event: GroupRequestEvent):
    global useridlist
    global jianzhang_list
    try:
        if f'{event.user_id}' in useridlist and not  jianzhang_list:
            await bot.set_group_add_request(
                flag=event.flag,
                sub_type=event.sub_type,
                approve=False,
                reason='禁止重复加群(误报请联系匣子@778571299)')
        else:
            return False   
        return True
    except:
        return False


async def add_userid_in_list(bot: Bot, event: GroupIncreaseNoticeEvent):
    global useridlist
    userid = f'{event.user_id}'
    filename = f'{event.group_id}.json'
    # 列表添加数据
    useridlist.append(f'{userid}')
    # 文件添加数据
    with open(f'{path}/{filename}', 'a+', encoding='utf-8') as file:
        file.write(f'{userid}\n')


async def del_userid_in_list(bot: Bot, event: GroupDecreaseNoticeEvent):
    global useridlist
    userid = f'{event.user_id}'
    filename = f'{event.group_id}.json'
    # 列表删除数据
    useridlist.remove(f'{userid}')

    # 重新读取数据
    os.remove(f'{path}/{filename}')
    with open(f'{path}/{filename}', 'a+', encoding='utf-8') as file:
        # 从文件读取内容删除指定内容后重新覆盖写入
        userid_list = await bot.call_api('get_group_member_list', **{
            'group_id': event.group_id
        })  # 从callAPI获取成员列表
        userid_list = ast.literal_eval(str(userid_list))  # 转换数据格式
        for userid in userid_list:  # 写入名单
            file.write(f'{userid["user_id"]}\n')
    load_useridlist()
