from PIL import Image
# 生成图片(素材图，物品图标，生成图，数字)
def extract_and_combine(base_image_path, target_image_path, output_path, number):
    # 打开基础图片，即包含所有符号的图片
    base_image = Image.open(base_image_path)
    # 打开目标图片，即需要添加符号的图片
    target_image = Image.open(target_image_path)

    # 设置每个符号的宽度和高度
    symbol_width, symbol_height = 36, 40
    # 确定需要提取的符号
    symbols = []
    if number < 0:
        symbols.append(1)  # "-" 的索引位置
        number = -number
    elif number == 0:
        symbols.append(2)  # "0" 的索引位置
    else:
        digits = []
        while number > 0:
            digit = number % 10
            digits.append(digit + 2)  # 数字的索引位置，加2是因为 "+" 和 "-" 在前两位
            number //= 10
        symbols.extend(reversed(digits))  # 反转列表以正确顺序处理数字
        symbols.insert(0, 0)  # 在数字前插入 "+" 的索引位置

    # 提取符号
    extracted_symbols = []
    for index in symbols:
        left = index * symbol_width
        box = (left, 0, left + symbol_width, symbol_height)
        symbol = base_image.crop(box)
        extracted_symbols.append(symbol)

    # 拼接符号到目标图片上
    # 计算新图片的宽度和高度
    new_width = target_image.width + symbol_width * len(extracted_symbols)
    new_height = max(target_image.height, symbol_height)

    # 创建一个新的空白图片
    new_image = Image.new('RGBA', (new_width, new_height))
    # 先粘贴目标图片
    new_image.paste(target_image, (0, 0))

    # 粘贴符号，确保垂直对齐
    offset = target_image.width
    for symbol in extracted_symbols:
        vertical_position = new_height - symbol_height  # 计算垂直位置
        new_image.paste(symbol, (offset, vertical_position))
        offset += symbol_width

    # 保存新图片
    new_image.save(output_path, overwrite=True)

# 使用函数
# extract_and_combine('path_to_symbols.png', '001.jpg', 'output.png', 999)  # 示例使用数字 10


# 将两张图竖着拼接(上图，下图，生成图)
def concatenate_images(top_image_path, bottom_image_path, output_path):
    # 打开顶部图片（output.png）
    top_image = Image.open(top_image_path)
    # 打开底部图片（output2.png）
    bottom_image = Image.open(bottom_image_path)

    # 获取两张图片的宽度和高度
    top_width, top_height = top_image.size
    bottom_width, bottom_height = bottom_image.size

    # 确定新图片的宽度和高度
    new_width = max(top_width, bottom_width)
    new_height = top_height + bottom_height

    # 创建一个新的空白图片，尺寸足以容纳两张图片
    new_image = Image.new('RGBA', (new_width, new_height))

    # 将顶部图片粘贴到新图片的顶部
    new_image.paste(top_image, (0, 0))

    # 将底部图片粘贴到新图片的底部
    new_image.paste(bottom_image, (0, top_height))

    # 保存最终的合成图片
    new_image.save(output_path, overwrite=True)

# 使用函数
# concatenate_images('output.png', 'output2.png', 'final_output.png')



# 添加背景(背景素材，原图，生成图)
from PIL import Image

def overlay_images(background_path, overlay_path, output_path):
    # 打开背景图片（a.png）
    background = Image.open(background_path)
    # 打开需要保持原样的图片（output.png）
    overlay = Image.open(overlay_path)

    # 获取overlay图片的尺寸
    overlay_width, overlay_height = overlay.size
    # 获取background图片的尺寸
    background_width, background_height = background.size
    # 计算新的背景宽度，宽度为overlay宽度加5
    # background_width = overlay_width + 5
    # 计算裁剪区域，使其居中
    left = (background_width - overlay_width) / 2
    top = (background_height - overlay_height) / 2
    right = (background_width + overlay_width) / 2
    bottom = (background_height + overlay_height) / 2

    # 调整background图片的大小以匹配overlay图片的尺寸
    # background = background.resize((overlay_width, overlay_height), Image.Resampling.LANCZOS)
    # 如果背景比覆盖图大，则裁剪背景图
    if background_width > overlay_width or background_height > overlay_height:
        background = background.crop((left, top, right, bottom))
        
    # 确保overlay是RGBA模式，以便处理透明度
    if overlay.mode != 'RGBA':
        overlay = overlay.convert('RGBA')

    # 创建一个新的空白图片，尺寸与overlay图片相同，模式为RGBA
    new_image = Image.new('RGB', (overlay_width, overlay_height))

    # 首先将调整大小后的背景图片放置在新图片上
    new_image.paste(background, (0, 0))

    # 然后将overlay图片放置在背景图片上
    new_image.paste(overlay, (0, 0), overlay)

    # 计算新的尺寸，等比压缩到原来的0.6
    new_width = int(overlay_width * 0.65)
    new_height = int(overlay_height * 0.65)

    # 调整图片大小
    new_image = new_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # 保存最终的合成图片
    new_image.save(output_path, overwrite=True)

# 使用函数
# overlay_images('a.png', '05.png', 'final_output.png')
