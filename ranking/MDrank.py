
import json
import base64

async def rank_button():
  str="直接点击下面按钮可快捷使用指令！\r-【绑定游戏id】:指令+游戏id即可绑定，用于个人查询中快捷查询(再次使用指令可换绑)\r-【个人查询】:查询已绑定的id数据,或加上其他id\r-【国服/国际服查询】:在指令后面加上区号可查询指定区排行\r提示：复制的@不生效!"
  data={
        "markdown":{
            "custom_template_id": " ",
            "params":[
                {
                    "key":"imgsize",
                    "values":["[img#224px #64px]"]
                },
                {
                    "key":"image",
                    "values":["https://127.0.0.1/QQ%E6%88%AA%E5%9B%BE20231218002839.png"]
                },
                {
                    "key":"title",
                    "values":["幻想排行榜"]
                },
                {
                    "key":"cite",
                    "values":[str]
                }
            ]
        },
        "rows": [
    {
      "buttons": [
        {
          "id": "1",
          "render_data": {
            "label": "绑定游戏id",
            "visited_label": "绑定游戏id",
            "style":2
          },
          "action": {
            "type": 2,
            "enter":False,
            "permission": {
              "type": 2
            },
            "unsupport_tips": "兼容文本",
            "data": "/幻想绑定"
          }
        },
        {
          "id": "2",
          "render_data": {
            "label": "个人查询",
            "visited_label": "个人查询",
            "style":2
          },
          "action": {
            "type": 2,
            "enter":False,
            "permission": {
              "type": 2
            },
            "unsupport_tips": "兼容文本",
            "data": "/战力查询"
          }
        },
      ]
    },
    {
      "buttons": [
        {
          "id": "3",
          "render_data": {
            "label": "排行榜国服",
            "visited_label": "排行榜国服",
            "style":2
          },
          "action": {
            "type": 2,
            "enter":False,
            "permission": {
              "type": 2
            },
            "unsupport_tips": "兼容文本",
            "data": "排行榜国服"
          }
        },
      ]
    },
    {
      "buttons": [
        {
          "id": "4",
          "render_data": {
            "label": "排行榜国际服",
            "visited_label": "排行榜国际服",
            "style":2
          },
          "action": {
            "type": 2,
            "enter":False,
            "permission": {
              "type": 2
            },
            "unsupport_tips": "兼容文本",
            "data": "排行榜国际服"
          }
        },
      ]
    },
    {
      "buttons": [
        {
          "id": "5",
          "render_data": {
            "label": "📘排行榜在线查询",
            "visited_label": "📘排行榜在线查询",
            "style":2
          },
          "action": {
            "type": 0,
            "permission": {
              "type": 2
            },
            "unsupport_tips": "兼容文本",
            "data": "http://127.0.0.1/show/index.php?zone=1&server=&show_server=1&abbreviate=1&power_sort=1"
          }
        },
      ]
    }
  ]
}
  # 将字典转换为 JSON 字符串
  json_str = json.dumps(data)
  data_bytes = json_str.encode('utf-8')
  encoded_data = base64.b64encode(data_bytes).decode('utf-8')
  return encoded_data