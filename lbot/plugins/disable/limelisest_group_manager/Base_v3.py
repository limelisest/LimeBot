import ast
import os
import sqlite3
from time import sleep
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupRequestEvent, GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent
path = './data/limeliset_group_manager'

def db_init():
    conn = sqlite3.connect(f'{path}/group.db')
    cur = conn.cursor()
    sql_text_1 = '''CREATE TABLE scores
           (姓名 TEXT,
            班级 TEXT,
            性别 TEXT,
            语文 NUMBER,
            数学 NUMBER,
            英语 NUMBER);'''
# 执行sql语句
