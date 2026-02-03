import requests
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
import re
from .MDrank import rank_button

import json
import requests
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot

pkhelp = on_command("排行榜", aliases={"phb"}, priority=2, block=True)
pkrank = on_command("战力榜", aliases={"zlb", "ranking"}, priority=2, block=True)
teamrank = on_command("军团榜", aliases={"jtb", "teamranking"}, priority=2, block=True)
reputationrank = on_command("声望榜", aliases={"swb"}, priority=2, block=True)
ranka = on_command("a", priority=3, block=True)# 临时指令a
newrank = on_command("新区", aliases={"新区榜","新区排行榜"}, priority=4, block=True)


# 排行榜help
@pkhelp.handle()
async def handle_function(args: Message = CommandArg()):
    if original_message := args.extract_plain_text():
        
        # 国服查询
        if any(keyword in original_message for keyword in ('gs','GS','Gs','国服')):
            match = re.search(r'国服([\d,\-，]+)', original_message)  # 支持中文逗号匹配
            if match:
                num = match.group(1).replace('，', ',')  # 统一转为英文逗号
                # 多区查询显示"合查"，单区显示"X区"
                if ',' in num or '-' in num:
                    title = "【战力榜-国服合查】"
                else:
                    title = f"【战力榜-国服{num}区】"
                url = 'http://127.0.0.1/ranklocal.php'
                data = {"zone": 1, "loarea": num}
                res = requests.post(url=url, data=data)
                await pkhelp.finish(f"\n*****{title}*****\n{res.text}")
            else:
                url = 'http://127.0.0.1/ranksort.php'
                data = {"zone": 1}
                res = requests.post(url=url, data=data)
                await pkhelp.finish(f"\n*****【战力榜-国服】*****\n{res.text}")
                
        # 国际服查询
        elif any(keyword in original_message for keyword in ('ws','WS','Ws','国际服')):
            match = re.search(r'国际服([\d,\-，]+)', original_message)
            if match:
                num = match.group(1).replace('，', ',')
                if ',' in num or '-' in num:
                    title = "【战力榜-国际服合查】"
                else:
                    title = f"【战力榜-国际服{num}区】"
                url = 'http://127.0.0.1/ranklocal.php'
                data = {"zone": 2, "loarea": num}
                res = requests.post(url=url, data=data)
                await pkhelp.finish(f"\n*****{title}*****\n{res.text}")
            else:
                url = 'http://127.0.0.1/ranksort.php'
                data = {"zone": 2}
                res = requests.post(url=url, data=data)
                await pkhelp.finish(f"\n****【战力榜-国际服】****\n{res.text}")
                
        # 幼儿园查询
        elif any(keyword in original_message for keyword in ('yey','YEY','幼儿园')):
            url = 'http://127.0.0.1/ranksort.php'
            data = {"zone": 9}
            res = requests.post(url=url, data=data)
            await pkhelp.finish(f"\n****【战力榜-幼儿园】****\n{res.text}")
            
        # 全服查询
        elif any(keyword in original_message for keyword in ('all','ALL','All','所有','全部','全游')):
            url = 'http://127.0.0.1/ranksort.php'
            data = {"zone": 10}
            res = requests.post(url=url, data=data)
            await pkhelp.finish(f"\n****【战力榜-所有服】****\n{res.text}")
            
        # 英文服查询
        elif any(keyword in original_message for keyword in ('es','ES','Es','英文服')):
            match = re.search(r'英文服([\d,\-，]+)', original_message)
            if match:
                num = match.group(1).replace('，', ',')
                if ',' in num or '-' in num:
                    title = "【战力榜-英文服合查】"
                else:
                    title = f"【战力榜-英文服{num}区】"
                url = 'http://127.0.0.1/ranklocal.php'
                data = {"zone": 3, "loarea": num}
                res = requests.post(url=url, data=data)
                await pkhelp.finish(f"\n*****{title}*****\n{res.text}")
            else:
                url = 'http://127.0.0.1/ranksort.php'
                data = {"zone": 3}
                res = requests.post(url=url, data=data)
                await pkhelp.finish(f"\n****【战力榜-英文服】****\n{res.text}")
    else:
        await pkhelp.finish(f"\n排行榜查询指令：\n【1】/战力榜+区服\n【2】/声望榜+区服\n【3】/军团榜+区服\n区服：(国服、幼儿园、国际服、英文服)，区服后面可加区号(支持格式：5 或 1,5,9 或 1-20)\nps：查指定区时，幼儿园属于国服")


# 战力榜
@pkrank.handle()
async def handle_function(args: Message = CommandArg()):
    if original_message := args.extract_plain_text():
        
        # 国服查询
        if any(keyword in original_message for keyword in ('gs','GS','Gs','国服')):
            match = re.search(r'国服([\d,\-，]+)', original_message)
            if match:
                num = match.group(1).replace('，', ',')
                if ',' in num or '-' in num:
                    title = "【战力榜-国服合查】"
                else:
                    title = f"【战力榜-国服{num}区】"
                url = 'http://127.0.0.1/ranklocal.php'
                data = {"zone": 1, "loarea": num}
                res = requests.post(url=url, data=data)
                await pkrank.finish(f"\n*****{title}*****\n{res.text}")
            else:
                url = 'http://127.0.0.1/ranksort.php'
                data = {"zone": 1}
                res = requests.post(url=url, data=data)
                await pkrank.finish(f"\n*****【战力榜-国服】*****\n{res.text}")
                
        # 国际服查询
        elif any(keyword in original_message for keyword in ('ws','WS','Ws','国际服')):
            match = re.search(r'国际服([\d,\-，]+)', original_message)
            if match:
                num = match.group(1).replace('，', ',')
                if ',' in num or '-' in num:
                    title = "【战力榜-国际服合查】"
                else:
                    title = f"【战力榜-国际服{num}区】"
                url = 'http://127.0.0.1/ranklocal.php'
                data = {"zone": 2, "loarea": num}
                res = requests.post(url=url, data=data)
                await pkrank.finish(f"\n*****{title}*****\n{res.text}")
            else:
                url = 'http://127.0.0.1/ranksort.php'
                data = {"zone": 2}
                res = requests.post(url=url, data=data)
                await pkrank.finish(f"\n****【战力榜-国际服】****\n{res.text}")
                
        # 幼儿园查询
        elif any(keyword in original_message for keyword in ('yey','YEY','幼儿园')):
            url = 'http://127.0.0.1/ranksort.php'
            data = {"zone": 9}
            res = requests.post(url=url, data=data)
            await pkrank.finish(f"\n****【战力榜-幼儿园】****\n{res.text}")
            
        # 全服查询
        elif any(keyword in original_message for keyword in ('all','ALL','All','所有','全部','全游')):
            url = 'http://127.0.0.1/ranksort.php'
            data = {"zone": 10}
            res = requests.post(url=url, data=data)
            await pkrank.finish(f"\n****【战力榜-所有服】****\n{res.text}")
            
        # 英文服查询
        elif any(keyword in original_message for keyword in ('es','ES','Es','英文服')):
            match = re.search(r'英文服([\d,\-，]+)', original_message)
            if match:
                num = match.group(1).replace('，', ',')
                if ',' in num or '-' in num:
                    title = "【战力榜-英文服合查】"
                else:
                    title = f"【战力榜-英文服{num}区】"
                url = 'http://127.0.0.1/ranklocal.php'
                data = {"zone": 3, "loarea": num}
                res = requests.post(url=url, data=data)
                await pkrank.finish(f"\n*****{title}*****\n{res.text}")
            else:
                url = 'http://127.0.0.1/ranksort.php'
                data = {"zone": 3}
                res = requests.post(url=url, data=data)
                await pkrank.finish(f"\n****【战力榜-英文服】****\n{res.text}")
    else:
        await pkrank.finish("请在'/排行榜'后面接上要查询的服务器如：\n/战力榜 国服")
        # await pkrank.finish(f"[CQ:markdown,data=base64://{await rank_button()}]")
            
# 辅助函数：格式化区服显示，超过3个区只显示前3个
def format_zone_display(num_str):
    if ',' in num_str:
        parts = num_str.split(',')
        if len(parts) > 3:
            return f"{','.join(parts[:3])}...等"
    return num_str
            
            #1.[xx][0000][GS0][WS0][ES0]
# 军团榜
@teamrank.handle()
async def handle_function(args: Message = CommandArg()):
    if locstr := args.extract_plain_text():
        original_message = args.extract_plain_text()
        # if locstr in ('gs','GS','Gs','国服'):
        if any(locstr in original_message for locstr in ('gs','GS','Gs','国服')):
            if original_message:
                match = re.search(r'国服(\d+)', original_message)
                if match:
                    num=match.group(1)
                    # print("有数字")
                    # print('有数字'+num)
                    # 如果找到匹配，返回匹配到的数字部分
                    url='http://127.0.0.1/teamranklocal.php'
                    data = {"zone":1,"loarea":num}
                    res = requests.post(url=url, data=data)
                    await teamrank.finish(f"\n*****【军团榜-国服{num}区】*****\n{res.text}")
                    # res = requests.post(url=url,data = data)
                    # await pkrank.finish(f"\n*****【排行榜-国服{num}】*****\n{res.text}")
                else:
                    # print("没有匹配到数字")
                    # 如果没有找到匹配，返回None
                    # return None
                    url='http://127.0.0.1/teamranksort.php'
                    data = {"zone":1}
                    res = requests.post(url=url,data = data)
                    await teamrank.finish(f"\n*****【军团榜-国服】*****\n{res.text}")
        elif any(locstr in original_message for locstr in('ws','WS','Ws','国际服')):
            if original_message:
                match = re.search(r'国际服(\d+)', original_message)
                if match:
                    num=match.group(1)
                    # print("有数字")
                    # print('有数字'+num)
                    # 如果找到匹配，返回匹配到的数字部分
                    url='http://127.0.0.1/teamranklocal.php'
                    data = {"zone":2,"loarea":num}
                    res = requests.post(url=url, data=data)
                    await teamrank.finish(f"\n*****【军团榜-国际服{num}区】*****\n{res.text}")
                else:
                    url='http://127.0.0.1/teamranksort.php'
                    data = {"zone":2}
                    res = requests.post(url=url,data = data)
                    await teamrank.finish(f"\n****【军团榜-国际服】****\n{res.text}")
        elif any(locstr in original_message for locstr in('yey','YEY','幼儿园')):
            if original_message:
                url='http://127.0.0.1/teamranksort.php'
                data = {"zone":9}
                res = requests.post(url=url,data = data)
                await teamrank.finish(f"\n****【军团榜-幼儿园】****\n{res.text}")
        elif any(locstr in original_message for locstr in('all','ALL','All','所有','全部','全游')):
            if original_message:
                url='http://127.0.0.1/teamranksort.php'
                data = {"zone":10}
                res = requests.post(url=url,data = data)
                await teamrank.finish(f"\n****【军团榜-所有服】****\n{res.text}")
        elif any(locstr in original_message for locstr in('es','ES','Es','英文服')):
            # await pkrank.finish("英文服暂未开放查询！")
            if original_message:
                match = re.search(r'英文服(\d+)', original_message)
                if match:
                    num=match.group(1)
                    url='http://127.0.0.1/teamranklocal.php'
                    data = {"zone":3,"loarea":num}
                    res = requests.post(url=url, data=data)
                    await teamrank.finish(f"\n*****【军团榜-英文服{num}区】*****\n{res.text}")
                else:
                    url='http://127.0.0.1/teamranksort.php'
                    data = {"zone":3}
                    res = requests.post(url=url,data = data)
                    await teamrank.finish(f"\n****【军团榜-英文服】****\n{res.text}")
    else:
        await pkrank.finish("请在'/军团榜'后面接上要查询的服务器 如：国服、国际服、英文服")
        # await teamrank.finish(f"[CQ:markdown,data=base64://{await rank_button()}]")
# 声望榜
@reputationrank.handle()
async def handle_function(args: Message = CommandArg()):
    if locstr := args.extract_plain_text():
        original_message = args.extract_plain_text()
        # if locstr in ('gs','GS','Gs','国服'):
        if any(locstr in original_message for locstr in ('gs','GS','Gs','国服')):
            if original_message:
                match = re.search(r'国服(\d+)', original_message)
                if match:
                    num=match.group(1)
                    # print("有数字")
                    # print('有数字'+num)
                    # 如果找到匹配，返回匹配到的数字部分
                    url='http://127.0.0.1/reputationranklocal.php'
                    data = {"zone":1,"loarea":num}
                    res = requests.post(url=url, data=data)
                    await reputationrank.finish(f"\n*****【声望榜-国服{num}区】*****\n{res.text}")
                    # res = requests.post(url=url,data = data)
                    # await pkrank.finish(f"\n*****【排行榜-国服{num}】*****\n{res.text}")
                else:
                    # print("没有匹配到数字")
                    # 如果没有找到匹配，返回None
                    # return None
                    url='http://127.0.0.1/reputationranksort.php'
                    data = {"zone":1}
                    res = requests.post(url=url,data = data)
                    await reputationrank.finish(f"\n*****【声望榜-国服】*****\n{res.text}")
        elif any(locstr in original_message for locstr in('ws','WS','Ws','国际服')):
            if original_message:
                match = re.search(r'国际服(\d+)', original_message)
                if match:
                    num=match.group(1)
                    # print("有数字")
                    # print('有数字'+num)
                    # 如果找到匹配，返回匹配到的数字部分
                    url='http://127.0.0.1/reputationranklocal.php'
                    data = {"zone":2,"loarea":num}
                    res = requests.post(url=url, data=data)
                    await reputationrank.finish(f"\n*****【军团榜-国际服{num}区】*****\n{res.text}")
                else:
                    url='http://127.0.0.1/reputationranksort.php'
                    data = {"zone":2}
                    res = requests.post(url=url,data = data)
                    await reputationrank.finish(f"\n****【声望榜-国际服】****\n{res.text}")
        elif any(locstr in original_message for locstr in('yey','YEY','幼儿园')):
            if original_message:
                url='http://127.0.0.1/reputationranksort.php'
                data = {"zone":9}
                res = requests.post(url=url,data = data)
                await reputationrank.finish(f"\n****【声望榜-幼儿园】****\n{res.text}")
        elif any(locstr in original_message for locstr in('all','ALL','All','所有','全部','全游')):
            if original_message:
                url='http://127.0.0.1/reputationranksort.php'
                data = {"zone":10}
                res = requests.post(url=url,data = data)
                await reputationrank.finish(f"\n****【声望榜-所有服】****\n{res.text}")
        elif any(locstr in original_message for locstr in('es','ES','Es','英文服')):
            # await pkrank.finish("英文服暂未开放查询！")
            if original_message:
                match = re.search(r'英文服(\d+)', original_message)
                if match:
                    num=match.group(1)
                    url='http://127.0.0.1/reputationranklocal.php'
                    data = {"zone":3,"loarea":num}
                    res = requests.post(url=url, data=data)
                    await reputationrank.finish(f"\n*****【声望榜-英文服{num}区】*****\n{res.text}")
                else:
                    url='http://127.0.0.1/reputationranksort.php'
                    data = {"zone":3}
                    res = requests.post(url=url,data = data)
                    await reputationrank.finish(f"\n****【声望榜-英文服】****\n{res.text}")
    else:
        await pkrank.finish("请在'/军团榜'后面接上要查询的服务器 如：国服、国际服、英文服")
        # await reputationrank.finish(f"[CQ:markdown,data=base64://{await rank_button()}]")


@ranka.handle()
async def handlea_function(event: GroupMessageEvent, args: Message = CommandArg()):
    print("ranka")
    uid=event.user_id
    mov=args.extract_plain_text()
    
    file_path = './src/plugins/jsonfile/admin.json'
    with open(file_path, 'r',encoding='utf-8') as json_file:
        jdata = json.load(json_file)
    admin_data = jdata.get('admin', [])
    id_admin = any(entry.get('id') == uid for entry in admin_data)
    
    if id_admin:
        url='http://127.0.0.1/bot/mov/'
        p_data = {
            'mov':mov
            }
        res = requests.post(url,data=p_data,timeout=3)
        await ranka.finish(f"{res.text}")
    else:
        await ranka.finish("权限不足！")
        
@newrank.handle()
async def handleb_function(event: GroupMessageEvent, args: Message = CommandArg()):
    print("newrank")
    uid=event.user_id
    ndata=args.extract_plain_text()
    if args.extract_plain_text():
        file_path = './src/plugins/jsonfile/admin.json'
        with open(file_path, 'r',encoding='utf-8') as json_file:
            jdata = json.load(json_file)
        admin_data = jdata.get('admin', [])
        id_admin = any(entry.get('id') == uid for entry in admin_data)
        
        if id_admin:
            url='http://127.0.0.1/bot/newarea/'
            p_data = {
                'data':ndata
                }
            res = requests.post(url,data=p_data,timeout=3)
            await newrank.finish(f"{res.text}")
        else:
            await newrank.finish("权限不足！")
    else:
        url='http://127.0.0.1/bot/newarea/'
        p_data = {
            'mov':ndata
            }
        res = requests.post(url,data=p_data,timeout=3)
        await newrank.finish(f"{res.text}")