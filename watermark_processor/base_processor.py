"""
基础水印处理器类
提供通用的水印处理功能
"""

import os
import traceback
from PIL import Image, ImageDraw, ImageFont


class BaseWatermarkProcessor:
    """基础水印处理器"""
    
    def __init__(self):
        self.font_cache = {}
    
    def _get_font(self, font_size, font_family, bold=False, italic=False, underline=False):
        """获取字体对象"""
        # 根据字体家族和样式生成字体样式名称
        style_name = ""
        if bold:
            style_name += "bold"
        if italic:
            if style_name:
                style_name += " italic"
            else:
                style_name += "italic"
        if not style_name:
            style_name = "normal"
        
        # 尝试加载支持中文的字体
        font_path = None
        
        # 根据不同系统查找支持中文的字体
        if os.name == 'nt':  # Windows
            # 扩展字体映射，支持更多系统字体
            font_mapping = self._get_windows_font_mapping()
            
            # 检查选择的字体家族是否在映射中
            if font_family in font_mapping:
                # 根据样式选择字体文件
                if style_name in font_mapping[font_family]:
                    font_path = font_mapping[font_family][style_name]
                else:
                    # 默认使用正常样式
                    font_path = font_mapping[font_family]["normal"]
            else:
                # 尝试动态查找字体文件
                font_path = self._find_font_file(font_family, style_name)
                if not font_path:
                    # 默认使用黑体
                    font_path = font_mapping.get("黑体", font_mapping.get("宋体", {"normal": None}))["normal"]
            
            # 检查字体文件是否存在
            if font_path and os.path.exists(font_path):
                return ImageFont.truetype(font_path, font_size)
        elif os.name == 'posix':  # macOS/Linux
            # 尝试加载字体
            font_path = self._find_font_file(font_family, style_name)
            if font_path and os.path.exists(font_path):
                return ImageFont.truetype(font_path, font_size)
        
        # 如果找不到指定字体，使用默认字体
        return ImageFont.load_default()
    
    def _get_windows_font_mapping(self):
        """获取Windows系统字体映射"""
        return {
            "宋体": {
                "normal": r'C:\\Windows\\Fonts\\simsun.ttc', 
                "bold": r'C:\\Windows\\Fonts\\simsun.ttc', 
                "italic": r'C:\\Windows\\Fonts\\simsun.ttc',
                "bold italic": r'C:\\Windows\\Fonts\\simsun.ttc'
            },
            "黑体": {
                "normal": r'C:\\Windows\\Fonts\\simhei.ttf', 
                "bold": r'C:\\Windows\\Fonts\\simhei.ttf', 
                "italic": r'C:\\Windows\\Fonts\\simhei.ttf',
                "bold italic": r'C:\\Windows\\Fonts\\simhei.ttf'
            },
            "楷体": {
                "normal": r'C:\\Windows\\Fonts\\simkai.ttf', 
                "bold": r'C:\\Windows\\Fonts\\simkai.ttf', 
                "italic": r'C:\\Windows\\Fonts\\simkai.ttf',
                "bold italic": r'C:\\Windows\\Fonts\\simkai.ttf'
            },
            "仿宋": {
                "normal": r'C:\\Windows\\Fonts\\simfang.ttf', 
                "bold": r'C:\\Windows\\Fonts\\simfang.ttf', 
                "italic": r'C:\\Windows\\Fonts\\simfang.ttf',
                "bold italic": r'C:\\Windows\\Fonts\\simfang.ttf'
            },
            "微软雅黑": {
                "normal": r'C:\\Windows\\Fonts\\msyh.ttc', 
                "bold": r'C:\\Windows\\Fonts\\msyhbd.ttc', 
                "italic": r'C:\\Windows\\Fonts\\msyh.ttc',
                "bold italic": r'C:\\Windows\\Fonts\\msyhbd.ttc'
            },
            "Arial": {
                "normal": r'C:\\Windows\\Fonts\\arial.ttf', 
                "bold": r'C:\\Windows\\Fonts\\arialbd.ttf', 
                "italic": r'C:\\Windows\\Fonts\\ariali.ttf', 
                "bold italic": r'C:\\Windows\\Fonts\\arialbi.ttf'
            },
            "Times New Roman": {
                "normal": r'C:\\Windows\\Fonts\\times.ttf', 
                "bold": r'C:\\Windows\\Fonts\\timesbd.ttf', 
                "italic": r'C:\\Windows\\Fonts\\timesi.ttf', 
                "bold italic": r'C:\\Windows\\Fonts\\timesbi.ttf'
            },
            "Calibri": {
                "normal": r'C:\\Windows\\Fonts\\calibri.ttf', 
                "bold": r'C:\\Windows\\Fonts\\calibrib.ttf', 
                "italic": r'C:\\Windows\\Fonts\\calibrii.ttf', 
                "bold italic": r'C:\\Windows\\Fonts\\calibriz.ttf'
            },
            "Verdana": {
                "normal": r'C:\\Windows\\Fonts\\verdana.ttf', 
                "bold": r'C:\\Windows\\Fonts\\verdanab.ttf', 
                "italic": r'C:\\Windows\\Fonts\\verdanai.ttf', 
                "bold italic": r'C:\\Windows\\Fonts\\verdanaz.ttf'
            },
            "Tahoma": {
                "normal": r'C:\\Windows\\Fonts\\tahoma.ttf', 
                "bold": r'C:\\Windows\\Fonts\\tahomabd.ttf'
            }
        }
    
    def _find_font_file(self, font_family, style_name):
        """动态查找字体文件"""
        if os.name == 'nt':  # Windows
            font_dir = r'C:\\Windows\\Fonts'
            
            # 字体名称到文件名的映射
            font_name_mapping = {
                "宋体": ["simsun.ttc", "simsunb.ttf"],
                "黑体": ["simhei.ttf"],
                "楷体": ["simkai.ttf"],
                "仿宋": ["simfang.ttf"],
                "微软雅黑": ["msyh.ttc", "msyhbd.ttc"],
                "Arial": ["arial.ttf", "arialbd.ttf", "ariali.ttf", "arialbi.ttf"],
                "Times New Roman": ["times.ttf", "timesbd.ttf", "timesi.ttf", "timesbi.ttf"],
                "Calibri": ["calibri.ttf", "calibrib.ttf", "calibrii.ttf", "calibriz.ttf"],
                "Verdana": ["verdana.ttf", "verdanab.ttf", "verdanai.ttf", "verdanaz.ttf"],
                "Tahoma": ["tahoma.ttf", "tahomabd.ttf"]
            }
            
            # 尝试查找字体文件
            if font_family in font_name_mapping:
                for filename in font_name_mapping[font_family]:
                    font_path = os.path.join(font_dir, filename)
                    if os.path.exists(font_path):
                        return font_path
            
            # 尝试通过字体名称查找文件
            import glob
            possible_files = []
            
            # 根据字体家族名称生成可能的文件名
            if "黑体" in font_family:
                possible_files.extend(["*hei*", "*black*", "*bold*"])
            elif "宋体" in font_family or "Song" in font_family:
                possible_files.extend(["*song*", "*sun*"])
            elif "楷体" in font_family or "Kai" in font_family:
                possible_files.extend(["*kai*"])
            elif "仿宋" in font_family or "Fang" in font_family:
                possible_files.extend(["*fang*"])
            elif "雅黑" in font_family or "YaHei" in font_family:
                possible_files.extend(["*yahei*", "*msyh*"])
            
            # 搜索字体文件
            for pattern in possible_files:
                search_pattern = os.path.join(font_dir, f"*{pattern}*")
                for font_file in glob.glob(search_pattern):
                    if os.path.isfile(font_file):
                        return font_file
        
        return None
    
    def _get_watermark_position(self, image_size, watermark_size, position_name):
        """获取水印位置坐标"""
        # 如果position_name是一个元组或列表，表示自定义位置坐标
        if isinstance(position_name, (tuple, list)) and len(position_name) == 2:
            return position_name
        
        image_width, image_height = image_size
        watermark_width, watermark_height = watermark_size
        
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
    
    def _save_image(self, image, output_path):
        """保存图片，根据文件格式设置不同的保存参数"""
        try:
            ext = os.path.splitext(output_path)[1].lower()
            if ext in ['.jpg', '.jpeg']:
                # JPEG不支持透明通道，需要转换为RGB模式
                if image.mode in ["RGBA", "LA"]:
                    image = image.convert('RGB')
                image.save(output_path, 'JPEG', quality=95, optimize=False, progressive=False)
            elif ext == '.png':
                image.save(output_path, 'PNG', optimize=True, compress_level=9)
            else:
                image.save(output_path)
            return True
        except Exception as e:
            print(f"保存图片时出错: {str(e)}")
            traceback.print_exc()
            return False