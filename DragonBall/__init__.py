import random
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from .MDdb import db_button
from PIL import Image
from .picc import extract_and_combine,concatenate_images,overlay_images
import time
import json
import os
import requests
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment

draba = on_command("龙珠", aliases={"开龙珠"}, priority=1, block=True)


@draba.handle()
async def draba_f(event: GroupMessageEvent,args: Message = CommandArg()):
    # 打开文件并加载JSON数据
    uid=event.user_id
    file_path = './src/plugins/DragonBall/image/a.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    # 从加载的JSON数据中获取'times'的值
    times_da = data['tiktime']
    dbnum = data['dbnum']
    dbcd = data['dbcd']
    if (times_da+dbcd)>time.time():
        await draba.finish('请勿频繁使用该功能！')
    else:
        data['tiktime'] = time.time()  # 更改为新的值
        # 将更新后的数据写回文件
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    
    if args.extract_plain_text():
        num = is_number(args.extract_plain_text())
    else:
        num = 5
    print(int(num))
        
    if int(num) > dbnum:
        num=30
    elif int(num) < 1:
        num=5
        
    # 提交物品变更
    url='http://bot.ddata.top/hxyxgame/item/using.php'
    p_data = {
        'uid':uid,
        'itemid':26019,
        'amount':{num}
        }
    res = requests.post(url,data=p_data,timeout=3).json()
    if res['d']=='2':
        await draba.finish('该物品不存在，请签到获取吧！')
    elif res['d']=='0':
        await draba.finish('物品数量不足！\n当前剩余:'+res['amount'])
    elif res['d']=='1':
        amount=res['amount']
        
    str1='开启['+str(num)+']个7p龙珠：\r'
    timestamp = str(time.time())
    str2=radomdrba_f(int(num),timestamp)
    # str3='【结果仅供娱乐！】'
    stra=str1# +str2
    
    # 获取图片大小
    img = Image.open('./src/plugins/DragonBall/image/final_pic.jpg')
    # a, b = img.size
    # await draba.finish(f"[CQ:markdown,data=base64://{await db_button(stra,a,b,timestamp,amount)}]")
    # http://bot.ddata.top/image/final_pic{timestamp}.jpg
    dimage=f"[CQ:image,file=http://bot.ddata.top/image/final_pic{timestamp}.jpg]"
    dimage2=f"http://bot.ddata.top/image/final_pic{timestamp}.jpg"
    # idata={
    #     "image":"[CQ:image,file=https://cos1.chois.top/QQ%E6%88%AA%E5%9B%BE20231218190038.png]"
    # }
    # await draba.finish(f"{dimage2}\n{str1}\n背包剩余:{amount}个\n(结果仅供娱乐！)")
    await draba.finish(MessageSegment.image(dimage2)+f"\n{str1}\n背包剩余:{amount}个\n(结果仅供娱乐！)")


def is_number(s):
    try:
        int(s)
        return s
    except ValueError:
        return 5
    
def radomdrba_f(i,ts):
    # 初始化物品数量
    item_a = 0#魔罗
    item_b = 0#大罗
    item_c = 0#肥龙
    item_d = 0#石头票
    item_e = 0#8星主角箱
    item_f = 0#符石袋
    strs=''
    if int(i)<=0:
        strs='你开个🔨开'
    for _ in range(int(i)):
        
            
        # 必定获得abc三样东西其中一个
        rand_abc = random.random()
        if rand_abc < 0.25:
            item_a += 5
        elif rand_abc < 0.5:
            item_b += 5
        else:
            item_c += 5

        # 必定获得de两样东西其中一个
        rand_de = random.random()
        if rand_de < 0.5:
            item_d += random.choice([100, 200, 500])
        #     item_d += 100
        # elif rand_de < 0.4:
        #     item_d += 200
        # elif rand_de < 0.5:
        #     item_d += 500
        else:
            item_e += random.choice([3, 5, 10])

        # 50%概率获得附加物品f
        if random.random() < 0.5:
            item_f += 1
    bola=False
    if item_a>0:
        strs=strs+'【魔罗】+'+str(item_a)+'\r'
        # strs[0]='【魔罗】+'+str(item_a)
        extract_and_combine("./src/plugins/DragonBall/image/path_to_symbols.png", "./src/plugins/DragonBall/image/s5006.png", "./src/plugins/DragonBall/image/pica.png", item_a)
        bola=True
    if item_b>0:
        strs=strs+'【大罗】+'+str(item_b)+'\r'
        # strs[1]='【大罗】+'+str(item_b)
        if bola==True:
            extract_and_combine("./src/plugins/DragonBall/image/path_to_symbols.png", "./src/plugins/DragonBall/image/s9001.png", "./src/plugins/DragonBall/image/picb.png", item_b)
            concatenate_images("./src/plugins/DragonBall/image/pica.png", "./src/plugins/DragonBall/image/picb.png", "./src/plugins/DragonBall/image/pica.png")
        else:
            extract_and_combine("./src/plugins/DragonBall/image/path_to_symbols.png", "./src/plugins/DragonBall/image/s9001.png", "./src/plugins/DragonBall/image/pica.png", item_b)
            bola=True
    if item_c>0:
        strs=strs+'【肥龙】+'+str(item_c)+'\r'
        # strs[2]='【肥龙】+'+str(item_c)
        if bola==True:
            extract_and_combine("./src/plugins/DragonBall/image/path_to_symbols.png", "./src/plugins/DragonBall/image/s9003.png", "./src/plugins/DragonBall/image/picb.png", item_c)
            concatenate_images("./src/plugins/DragonBall/image/pica.png", "./src/plugins/DragonBall/image/picb.png", "./src/plugins/DragonBall/image/pica.png")
        else:
            extract_and_combine("./src/plugins/DragonBall/image/path_to_symbols.png", "./src/plugins/DragonBall/image/s9003.png", "./src/plugins/DragonBall/image/pica.png", item_c)
    if item_d>0:
        strs=strs+'【石头券】+'+str(item_d)+'\r'
        # strs[3]='【石头券】+'+str(item_d)
        extract_and_combine("./src/plugins/DragonBall/image/path_to_symbols.png", "./src/plugins/DragonBall/image/shitouquan.jpg", "./src/plugins/DragonBall/image/picb.png", item_d)
        concatenate_images("./src/plugins/DragonBall/image/pica.png", "./src/plugins/DragonBall/image/picb.png", "./src/plugins/DragonBall/image/pica.png")
    if item_e>0:
        strs=strs+'【主角箱(金)】+'+str(item_e)+'\r'
        # strs[4]='【主角箱(金)】+'+str(item_e)
        extract_and_combine("./src/plugins/DragonBall/image/path_to_symbols.png", "./src/plugins/DragonBall/image/997_zhujuejin.jpg", "./src/plugins/DragonBall/image/picb.png", item_e)
        concatenate_images("./src/plugins/DragonBall/image/pica.png", "./src/plugins/DragonBall/image/picb.png", "./src/plugins/DragonBall/image/pica.png")
    
    if item_f>0:
        strs=strs+'【14级符石袋】+'+str(item_f)+'\r'
        # strs[5]='【14级符石袋】+'+str(item_f)
        extract_and_combine("./src/plugins/DragonBall/image/path_to_symbols.png", "./src/plugins/DragonBall/image/25.jpg", "./src/plugins/DragonBall/image/picb.png", item_f)
        concatenate_images("./src/plugins/DragonBall/image/pica.png", "./src/plugins/DragonBall/image/picb.png", "./src/plugins/DragonBall/image/pica.png")
    
    overlay_images('./src/plugins/DragonBall/image/a.png', './src/plugins/DragonBall/image/pica.png', f'./botweb/image/final_pic{ts}.jpg')
    file_path = './src/plugins/DragonBall/image/a.json'
    # 清除原来的图片
    # 打开文件并加载JSON数据
    with open(file_path, 'r') as file:
        data = json.load(file)

    # 从加载的JSON数据中获取'times'的值
    times_value = data['times']
    pic_path = f'./botweb/image/final_pic{times_value}.jpg'
    try:
        # 尝试删除文件
        os.remove(pic_path)
        print("旧图片已删除")
    except FileNotFoundError:
        print("文件不存在")
    except PermissionError:
        print("没有权限删除文件")
    except Exception as e:
        print(f"删除旧图片时发生错误: {e}")
        
    data['times'] = ts  # 更改为新的值
    # 将更新后的数据写回文件
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        
    return strs
    # 输出结果
    # print(f"魔罗: {item_a}")
    # print(f"大罗: {item_b}")
    # print(f"肥龙: {item_c}")
    # print(f"石头票: {item_d}")
    # print(f"8星主角箱子: {item_e}")
    # print(f"符石袋: {item_f}")
    

