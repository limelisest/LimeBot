import json
import os
from shutil import which
filename='./data/number_list.json'

data={}
def refresh_data():
    global data
    #判断文件是否存在，不存在则创建文件
    if not os.path.exists(filename):
        file = open(filename, 'w', encoding='utf-8') 
    else:
        with open(filename, 'r', encoding='utf-8') as file:
            data=json.load(file)

def check_number(user_id):
    if user_id in data:
        return True
    else:
        return False

def add_number(user_id,group_id):
    refresh_data()
    global data
    #判断当前是否已经存在user_id
    if user_id not in data:
        data[user_id]=[group_id]#新建
    else:
        if group_id not in data[user_id]:
            data[user_id].append(group_id)  # 添加

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json.dumps(data))

def del_number(user_id,group_id):
    refresh_data()
    global data
    #判断是否存在群员
    if user_id in data:
        if group_id in data[user_id]:
            data[user_id].remove(group_id)
        if data[user_id] == []:
            del data[user_id]
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data))
        return True
    else:
        return False

def load_number(user_id_list,group_id):
    for user_id in user_id_list:
        add_number(user_id,group_id)

def del_all_number():
    os.remove(filename)
    refresh_data()
