import os
import json
import base64

# from flask import Flask, send_from_directory

# app = Flask(__name__)

# @app.route('/images/<filename>')
# def serve_image(filename):
#     # 存放图片路径
#     return send_from_directory('./src/plugins/DragonBall/image', 'final_pic.jpg')

# if __name__ == '__main__':
    # 运行服务器，host='0.0.0.0'使得服务器对外部可访问
    # app.run(host='127.0.0.1', port=8543)

async def db_button(s,w,h,ts,am):
  str1=s
  str2=f"[img#{int(w/3)}px #{int(h/3)}px]"
  # current_directory = os.path.dirname(__file__)
  # img_path = os.path.join(current_directory, './src/plugins/DragonBall/image/final_pic.jpg')
  # picurl=f"[CQ:image,file=file:///{img_path}]"
  
  
  picurl=f'http://bot.ddata.top/image/final_pic{ts}.jpg'
  endstr="背包剩余:"+str(am)+"\r结果仅供娱乐！"
  data={
        "markdown":{
            "custom_template_id": "custom_template_id",
            "params":[
                {
                    "key":"imgsize",
                    "values":[str2]
                },
                {
                    "key":"image",
                    "values":[picurl]
                },
                {
                    "key":"title",
                    "values":[str1]
                },
                {
                    "key":"cite",
                    "values":[endstr]
                }
            ]
        },
        "rows": [
    {
      "buttons": [
        {
          "id": "1",
          "render_data": {
            "label": "开5个",
            "visited_label": "开5个",
            "style":2
          },
          "action": {
            "type": 2,
            "enter":False,
            "permission": {
              "type": 2
            },
            "unsupport_tips": "兼容文本",
            "data": "/龙珠"
          }
        },
        {
          "id": "1",
          "render_data": {
            "label": "开10个",
            "visited_label": "开10个",
            "style":2
          },
          "action": {
            "type": 2,
            "enter":False,
            "permission": {
              "type": 2
            },
            "unsupport_tips": "兼容文本",
            "data": "/龙珠10"
          }
        },
        {
          "id": "1",
          "render_data": {
            "label": "开30个",
            "visited_label": "开30个",
            "style":2
          },
          "action": {
            "type": 2,
            "enter":False,
            "permission": {
              "type": 2
            },
            "unsupport_tips": "兼容文本",
            "data": "/龙珠30"
          }
        },
      ]
    },
  ]
}
  # 将字典转换为 JSON 字符串
  json_str = json.dumps(data)
  data_bytes = json_str.encode('utf-8')
  encoded_data = base64.b64encode(data_bytes).decode('utf-8')

  return encoded_data
