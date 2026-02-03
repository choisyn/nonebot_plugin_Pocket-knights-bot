import json
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment

tjfind = on_command("图鉴", aliases={"tj"}, priority=1, block=True)

@tjfind.handle()
async def tjfind_f(args: Message = CommandArg()):
    if locstr := args.extract_plain_text():
        # 加载数据
        data = load_data('./src/plugins/tj/tjdata.json')
        result = get_data(data, locstr)
        if result == False:
            await tjfind.finish(f"\n未查到相关信息！")

        outtext = ''
        if isinstance(result, dict):
            if "别名" in result:
                result = get_data(data, result["别名"])  # 通过引用获取别名数据

            if "图片url" in result:
                imageur = result['图片url']
                # outtext += imageur
            for key, value in result.items():
                if key != "图片url":  # 排除图片url
                    outtext += f"\n【{key}】: {value}"

        await tjfind.finish(MessageSegment.image(imageur)+outtext)
    else:
        await tjfind.finish(f"\n指令使用方法：\n图鉴+名称\n如：@机器人 图鉴钻石")


# 从 data.json 文件中读取数据
def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# 创建一个函数来获取数据
def get_data(data, key):
    return data.get(key, False)  # 如果找不到，返回提示信息
