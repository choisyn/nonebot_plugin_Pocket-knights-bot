import requests
import json
import os
import re
import time
import glob
from PIL import Image
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.adapters.onebot.v11 import MessageSegment
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import calendar

hxyxdate = on_command("幻想日历",aliases={"档期","活动","活动日历"}, priority=1, block=True)

@hxyxdate.handle()
async def readrank_function(event: GroupMessageEvent, args: Message = CommandArg()):
    filename=generate_calendar_image()
    
    await hxyxdate.finish(MessageSegment.image("http://bot.ddata.top/image/pic/"+filename)+"\n【说明】:同名活动所使用的[S]道具是一样的，而小活动不能使用[SS]和[SSS]道具，以及氪金的活动卡目前每期都不通用")
    
    
def generate_calendar_image(json_path='d:/nbbot2/nb2/botweb/date/calendar.json', output_dir='d:/nbbot2/nb2/botweb/image/pic'):
    """
    从 JSON 文件加载事件数据，生成带时间戳的日历图片，并删除旧图片。
    """
    # --- 确保输出目录存在 ---
    # 123
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已创建目录: {output_dir}")

    # --- 清理旧图片 ---
    try:
        old_images = glob.glob(os.path.join(output_dir, 'image_*.jpg'))
        for old_image in old_images:
            os.remove(old_image)
            print(f"已删除旧图片: {old_image}")
    except OSError as e:
        print(f"删除旧图片时出错: {e}")

    # --- 生成新文件名 ---
    timestamp = int(time.time())
    new_filename = f"image_{timestamp}.jpg"
    output_path = os.path.join(output_dir, new_filename)

    # --- 加载数据 ---
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            events_data = json.load(f)
    except FileNotFoundError:
        print(f"错误: JSON 文件未找到于 {json_path}")
        return
    except json.JSONDecodeError:
        print(f"错误: JSON 文件格式不正确: {json_path}")
        return

    if not events_data:
        print("JSON 文件中没有事件数据。")
        return

    events = []
    for item in events_data:
        try:
            start_date = datetime.strptime(item['time'], '%Y-%m-%d')
            duration = int(item.get('day', 1))
            if duration < 1: duration = 1
            end_date = start_date + timedelta(days=duration - 1)
            events.append({
                'start_date': start_date,
                'end_date': end_date,
                'title': item['title'],
            })
        except (ValueError, TypeError, KeyError) as e:
            print(f"警告: 忽略格式错误的事件: {item}, 错误: {e}")
            continue
    
    events.sort(key=lambda e: (e['start_date'], e['end_date']))

    # --- 准备绘图 ---
    event_colors = ['#FFADAD', '#FFD6A5', '#FDFFB6', '#CAFFBF', '#9BF6FF', '#A0C4FF', '#BDB2FF', '#FFC6FF', '#D4FFAD', '#A0DDFF', '#D1B2FF', '#A0FFEE', '#E4D4B9', '#CCCCCC', '#FFB4A2', '#E0BBE4']
    lanes_occupied_until = []
    color_idx = 0
    today = datetime.now()
    
    # 寻找可用的泳道
    for event in events:
        assigned_lane = None
        for i, end_date in enumerate(lanes_occupied_until):
            if event['start_date'] > end_date:
                assigned_lane = i
                lanes_occupied_until[i] = event['end_date']
                break
        # 如果没有找到可用泳道，创建新泳道
        if assigned_lane is None:
            assigned_lane = len(lanes_occupied_until)
            lanes_occupied_until.append(event['end_date'])
        
        event['lane'] = assigned_lane
        event['color'] = event_colors[color_idx % len(event_colors)]
        color_idx += 1
    # --- 确定要显示的月份 (根据当天日期) ---
    current_month_start = today.replace(day=1)
    # previous_month_end = current_month_start - timedelta(days=1)
    # previous_month_start = previous_month_end.replace(day=1)
    
    # latest_months = sorted([current_month_start, previous_month_start])
    if today.day < 15:
        # 1-14号：显示当月与上个月
        previous_month_end = current_month_start - timedelta(days=1)
        previous_month_start = previous_month_end.replace(day=1)
        latest_months = sorted([current_month_start, previous_month_start])
    else:
        # >=15号：显示当月与下个月
        next_month_start = (current_month_start + timedelta(days=32)).replace(day=1)
        latest_months = [current_month_start, next_month_start]
    
    # --- 绘图设置 ---
    cell_width, base_cell_height = 180, 150
    header_height = 75
    month_header_height = 85
    padding = 35
    bar_y_start_offset, bar_height, bar_padding = 65, 32, 5
    lanes_area_height_in_cell = base_cell_height - bar_y_start_offset
    img_width = 7 * cell_width + 2 * padding

    # --- 字体加载 ---
    try:
        font_path = "./src/plugins/date/SmileySans-Oblique.ttf"
        if not os.path.exists(font_path):
             raise IOError(f"指定的字体文件未找到: {font_path}")

        font_main = ImageFont.truetype(font_path, 36)
        font_month = ImageFont.truetype(font_path, 54)
        font_day_header = ImageFont.truetype(font_path, 38)
        font_event = ImageFont.truetype(font_path, 35)
        font_today = ImageFont.truetype(font_path, 40)
        font_hint = ImageFont.truetype(font_path, 50)
    except IOError as e:
        print(f"警告: {e}。将使用 PIL 默认字体（中文可能无法显示）。")
        font_main, font_month, font_day_header, font_event, font_today, font_hint = [ImageFont.load_default()] * 6

    # --- 高度预计算 ---
    week_extra_heights = {}
    total_calculated_extra_height = 0
    base_months_height = 0

    for month_date_calc in latest_months:
        year_calc, month_calc = month_date_calc.year, month_date_calc.month
        month_calendar_calc = calendar.monthcalendar(year_calc, month_calc)
        base_months_height += month_header_height + header_height + (len(month_calendar_calc) * base_cell_height)

        for week_index_calc, week_calc in enumerate(month_calendar_calc):
            week_start_date_calc = datetime(year_calc, month_calc, week_calc[0]) if week_calc[0] != 0 else (datetime(year_calc, month_calc, week_calc[6]) - timedelta(days=6))
            week_end_date_calc = week_start_date_calc + timedelta(days=6)
            
            events_in_week_calc = [e for e in events if e['start_date'] <= week_end_date_calc and e['end_date'] >= week_start_date_calc]
            
            max_lane = -1
            if events_in_week_calc:
                max_lane = max(e.get('lane', -1) for e in events_in_week_calc)
            
            # 当泳道数达到3条或以上时 (lane索引为2或以上)
            if max_lane >= 2:
                required_height_for_lanes = (max_lane + 1) * (bar_height + bar_padding)
                extra_height = max(0, required_height_for_lanes - lanes_area_height_in_cell)
                if extra_height > 0:
                    week_extra_heights[(year_calc, month_calc, week_index_calc)] = extra_height
                    total_calculated_extra_height += extra_height
                    
    # 计算提示文字所需的总高度
    hint_text1 = "提示1：空白日期未必没有活动，可能只是暂未安排活动！"
    hint_text2 = "提示2：国服更新时间为凌晨0点，国际服为早上8点"
    line_spacing = 8
    try:
        _l, _t, _r, hint_text_height = font_hint.getbbox(hint_text1)
    except AttributeError:
        _w, hint_text_height = font_hint.getmask(hint_text1).size
    total_hint_height = hint_text_height * 2 + line_spacing + 15 
    
    # 计算最终图片总高度
    total_height = base_months_height + total_calculated_extra_height + (len(latest_months) + 1) * padding + total_hint_height

    img = Image.new('RGB', (img_width, total_height), 'white')
    draw = ImageDraw.Draw(img)

    current_y = padding
    
    # --- 开始绘图 ---
    for month_date in latest_months:
        year, month = month_date.year, month_date.month
        month_calendar = calendar.monthcalendar(year, month)

        # 绘制月份和星期标题
        draw.text((padding, current_y), f"{year}年 {month}月", fill='black', font=font_month)
        current_y += month_header_height
        
        days_of_week = ["一", "二", "三", "四", "五", "六", "日"]
        for i, day in enumerate(days_of_week):
            draw.text((padding + i * cell_width + cell_width/2 - 19, current_y), day, fill='gray', font=font_day_header)
        current_y += header_height

        # 动态绘制网格和日期
        grid_top_y = current_y
        week_start_y_main = grid_top_y
        for week_index, week in enumerate(month_calendar):
            current_week_height = base_cell_height + week_extra_heights.get((year, month, week_index), 0)
            for day_index, day in enumerate(week):
                x0, y0 = padding + day_index * cell_width, week_start_y_main
                draw.rectangle([x0, y0, x0 + cell_width, y0 + current_week_height], outline='lightgray')
                if day != 0:
                    draw.text((x0 + 5, y0 + 5), str(day), fill='black', font=font_main)
                    if year == today.year and month == today.month and day == today.day:
                        today_text = "今日"
                        text_width = font_today.getlength(today_text)
                        tx = x0 + (cell_width - text_width) / 2
                        ty = y0 + 5
                        draw.text((tx, ty), today_text, fill='red', font=font_today)
            week_start_y_main += current_week_height
        
        
        # 动态绘制事件条背景
        week_start_y_main = grid_top_y
        for week_index, week in enumerate(month_calendar):
            current_week_height = base_cell_height + week_extra_heights.get((year, month, week_index), 0)
            week_start_date = datetime(year, month, week[0]) if week[0] != 0 else (datetime(year, month, week[6]) - timedelta(days=6))
            week_end_date = week_start_date + timedelta(days=6)
            
            events_in_week = [e for e in events if e['start_date'] <= week_end_date and e['end_date'] >= week_start_date]
            for event in events_in_week:
                start_col = max(event['start_date'], week_start_date).weekday()
                end_col = min(event['end_date'], week_end_date).weekday()
                
                bar_y = week_start_y_main + bar_y_start_offset + event.get('lane', 0) * (bar_height + bar_padding)
                x0_bar = padding + start_col * cell_width
                x1_bar = padding + (end_col + 1) * cell_width
                draw.rectangle([x0_bar + 2, bar_y, x1_bar - 2, bar_y + bar_height], fill=event['color'])
            week_start_y_main += current_week_height

        # 动态绘制事件条标题
        week_start_y_main = grid_top_y
        for week_index, week in enumerate(month_calendar):
            current_week_height = base_cell_height + week_extra_heights.get((year, month, week_index), 0)
            week_start_date = datetime(year, month, week[0]) if week[0] != 0 else (datetime(year, month, week[6]) - timedelta(days=6))
            week_end_date = week_start_date + timedelta(days=6)

            events_in_week = [e for e in events if e['start_date'] <= week_end_date and e['end_date'] >= week_start_date]
            for event in events_in_week:
                event_start_this_week = max(event['start_date'], week_start_date)
                event_end_this_week = min(event['end_date'], week_end_date)
                start_col = event_start_this_week.weekday()
                title_x = padding + start_col * cell_width + 5
                bar_y = week_start_y_main + bar_y_start_offset + event.get('lane', 0) * (bar_height + bar_padding)
                
                end_col = event_end_this_week.weekday()
                available_width = (end_col - start_col + 1) * cell_width - 10
                
                title = event['title']
                if font_event.getlength(title) > available_width:
                    for i in range(len(title), 0, -1):
                        if font_event.getlength(title[:i] + '...') <= available_width:
                            title = title[:i] + '...'
                            break
                    else:
                        title = ''
                if title:
                    draw.text((title_x, bar_y), title, fill='black', font=font_event)
            week_start_y_main += current_week_height

        current_y = week_start_y_main + padding
        
   # --- 添加提示文字 ---
    hint2_y = total_height - hint_text_height - 15
    hint2_x = padding
    hint1_y = hint2_y - hint_text_height - line_spacing
    hint1_x = padding
    draw.text((hint1_x, hint1_y), hint_text1, fill='gray', font=font_hint)
    draw.text((hint2_x, hint2_y), hint_text2, fill='gray', font=font_hint)
    # --- 保存图片 ---
    img.save(output_path)
    print(f"日历图片已保存至 {output_path}")
    return new_filename

