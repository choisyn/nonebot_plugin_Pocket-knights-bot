import json
import re
import smtplib
import requests
from email.mime.text import MIMEText
from email.header import Header
import mysql.connector
import random
import datetime
from datetime import datetime

from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot

import os

sjlbm = on_command("随机礼包码",aliases={"随机兑换码"}, priority=1, block=True)

@sjlbm.handle()
async def gift_sjlbm(event: GroupMessageEvent):
    # 2024年12月31日16:52:56
    # 随机兑换码：25年1月15日过期  
    print("sdcode")
    """检查是否在有效期内"""
    current_time = datetime.now()
    deadline = datetime(2025, 1, 15, 23, 59, 59)
    if current_time > deadline:
        await sjlbm.finish("\n╮(╯▽╰)╭\n活动已过期~下次要尽快哦！")
        
    # if event.group_id == 282202829:
    if event.group_id==239625765 or event.group_id==282202829:
        file_path = './src/plugins/gift_sdcode/sdcode.txt'
        used_codes_file = './src/plugins/gift_sdcode/used_codes_file.txt'

        # 尝试读取文件内容
        def load_codes_from_file(path):
            if not os.path.exists(path):
                return []
            with open(path, 'r') as file:
                return [line.strip() for line in file.readlines() if line.strip()]
            
        # 保存已使用的兑换码
        def save_used_codes(path, used_codes):
            with open(path, 'w') as file:
                for code in used_codes:
                    file.write(code + '\n')

        # 初始化兑换码列表
        codes = load_codes_from_file(file_path)
        # 尝试加载已使用的兑换码
        used_codes = set(load_codes_from_file(used_codes_file))
        available_codes = list(set(codes) - used_codes)  # 剩余未使用的兑换码

        if not available_codes:
            print("所有兑换码均已抽取完毕！")
            await sjlbm.finish("兑换码已发放完毕!")

        selected_code = random.choice(available_codes)  # 随机抽取
        used_codes.add(selected_code)  # 标记为已使用

        # 显示抽取的兑换码和剩余数量
        print(f"抽取的兑换码: {selected_code}")
        print(f"剩余未抽取的兑换码数量: {len(codes) - len(used_codes)}")
        # 保存已使用的兑换码
        save_used_codes(used_codes_file, used_codes)
        await sjlbm.finish(f"\n剩余:{len(codes) - len(used_codes)}/{len(codes)}\n礼包内容：10级金币卡*500+神奇硬币*50+神奇六星珠子*5+13级宝石袋子*1\n(请在2025年1月15日之前使用!)\n您的兑换码:\n\n{selected_code}")

        
        
