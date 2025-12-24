import os
import random
from tkinter import messagebox

# 默认配置
DEFAULT_CONFIG = {
    "default_text": "VisMark - 智能图像水印处理工具",
    "default_font_size": 36,
    "default_opacity": 70,
    "default_rotation": 0,
    "default_position": "center",
    "default_font_color": "#FFFFFF",
    "default_font_style": "normal"
}

# 预设样式
PRESETS = {
    "版权信息": {
        "text": "© 2023 版权所有",
        "font_size": 16,
        "font_color": "#FFFFFF",
        "font_style": "normal",
        "position": "bottom-right",
        "opacity": 80
    },
    "品牌标识": {
        "text": "My Brand",
        "font_size": 32,
        "font_color": "#FF0000",
        "font_style": "bold",
        "position": "top-left",
        "opacity": 100
    },
    "日期标记": {
        "text": "2023-01-01",
        "font_size": 14,
        "font_color": "#888888",
        "font_style": "normal",
        "position": "bottom-left",
        "opacity": 60
    }
}


def get_watermark_position(position_name, image_width, image_height, watermark_width, watermark_height):
    """根据位置名称获取水印在图片上的坐标"""
    positions = {
        "top-left": (watermark_width // 2, watermark_height // 2),
        "top": (image_width // 2, watermark_height // 2),
        "top-right": (image_width - watermark_width // 2, watermark_height // 2),
        "left": (watermark_width // 2, image_height // 2),
        "center": (image_width // 2, image_height // 2),
        "right": (image_width - watermark_width // 2, image_height // 2),
        "bottom-left": (watermark_width // 2, image_height - watermark_height // 2),
        "bottom": (image_width // 2, image_height - watermark_height // 2),
        "bottom-right": (image_width - watermark_width // 2, image_height - watermark_height // 2)
    }
    
    return positions.get(position_name, positions["center"])


def validate_color(color_str):
    """验证颜色字符串是否有效"""
    if not color_str.startswith("#"):
        return False
    if len(color_str) != 7:
        return False
    try:
        int(color_str[1:], 16)
        return True
    except ValueError:
        return False


def get_unique_filename(directory, filename):
    """生成唯一的文件名，避免覆盖"""
    base_name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base_name}_{counter}{ext}"
        counter += 1
    
    return new_filename


def show_error(message):
    """显示错误消息"""
    messagebox.showerror("错误", message)


def show_info(message):
    """显示信息消息"""
    messagebox.showinfo("提示", message)


def show_warning(message):
    """显示警告消息"""
    messagebox.showwarning("警告", message)