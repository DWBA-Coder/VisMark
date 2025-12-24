"""
文字水印处理器类
提供文字水印的添加功能
"""

import os
import traceback
import concurrent.futures
import random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from .base_processor import BaseWatermarkProcessor


class TextWatermarkProcessor(BaseWatermarkProcessor):
    """文字水印处理器"""
    
    def add_text_watermark(self, image_path, watermark_text, output_path, 
                          font_size=24, font_color="#000000", font_family="宋体",
                          bold=False, italic=False, underline=False,
                          position="center", opacity=50, rotation=0,
                          flip_horizontal=False, flip_vertical=False,
                          scattered_watermark=False, invisible_watermark=False, texture_watermark=False,
                          enable_shadow=False, shadow_color="#000000", shadow_offset_x=2, shadow_offset_y=2, shadow_opacity=30,
                          security_watermark=False, security_key="", security_strength=0.02):
        """
        添加文字水印到图片
        
        参数:
            image_path: 原始图片路径
            watermark_text: 水印文字
            output_path: 输出图片路径
            font_size: 字体大小
            font_color: 字体颜色
            font_style: 字体样式 (normal, bold, italic, bold italic)
            position: 水印位置
            opacity: 透明度 (0-100)
            rotation: 旋转角度 (-180到180)
            flip_horizontal: 是否水平翻转
            flip_vertical: 是否垂直翻转
            scattered_watermark: 是否使用分散水印
            invisible_watermark: 是否使用隐形水印
            texture_watermark: 是否使用纹理水印
            enable_shadow: 是否启用文字阴影
            shadow_color: 阴影颜色
            shadow_offset_x: 阴影水平偏移量
            shadow_offset_y: 阴影垂直偏移量
            shadow_opacity: 阴影透明度 (0-100)
            
        返回:
            bool: 是否成功添加水印
        """
        try:
            # 打开原始图片
            image = Image.open(image_path).convert("RGBA")
            
            # 添加水印
            watermarked_image = self.add_text_watermark_to_image(
                image, watermark_text, font_size, font_color, font_family,
                bold, italic, underline,
                position, opacity, rotation, flip_horizontal, flip_vertical,
                scattered_watermark, invisible_watermark, texture_watermark,
                enable_shadow, shadow_color, shadow_offset_x, shadow_offset_y, shadow_opacity
            )
            
            # 保存图片
            return self._save_image(watermarked_image, output_path)
        except Exception as e:
            print(f"添加文字水印时出错: {str(e)}")
            traceback.print_exc()
            return False
    
    def add_text_watermark_to_image(self, image, watermark_text, font_size=24, 
                                   font_color="#000000", font_family="宋体",
                                   bold=False, italic=False, underline=False,
                                   position="center", opacity=50, rotation=0,
                                   flip_horizontal=False, flip_vertical=False,
                                   scattered_watermark=False, invisible_watermark=False, texture_watermark=False,
                                   enable_shadow=False, shadow_color="#000000", shadow_offset_x=2, shadow_offset_y=2, shadow_opacity=30):
        """
        向Image对象添加文字水印
        """
        try:
            # 确保图片是RGB模式
            if image.mode != 'RGB':
                result = image.copy().convert('RGB')
            else:
                result = image.copy()
            
            # 应用特殊水印功能
            if scattered_watermark:
                result = self.add_scattered_watermark(
                    result, watermark_text, font_size, font_color, font_family,
                    bold, italic, underline, opacity, rotation
                )
            elif invisible_watermark:
                result = self.add_invisible_watermark(
                    result, watermark_text, font_size, font_color, font_family,
                    position
                )
            elif texture_watermark:
                result = self.add_texture_watermark(
                    result, watermark_text, font_size, font_color, font_family,
                    opacity, rotation
                )
            else:
                # 继续普通水印的处理
                # 创建文字图层
                font = self._get_font(font_size, font_family, bold, italic, underline)
                draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # 为加粗效果增加额外空间
                bold_padding = 2 if bold else 0
                text_width += bold_padding  # 为左右偏移各增加1像素
                text_height += bold_padding  # 为上下偏移各增加1像素
                
                # 为斜体效果增加额外宽度，特别是针对中文
                italic_padding = int((text_height + bold_padding) * 0.8) if italic else 0  # 增加80%的宽度用于斜体
                text_width += italic_padding
                
                # 为下划线增加额外高度
                underline_padding = int(font_size * 0.3) if underline else 0  # 增加更多空间用于下划线
                text_height += underline_padding  # 增加30%的高度用于下划线
                
                # 额外增加更多安全空间，确保中文文本完整显示
                text_width += 20  # 额外增加20像素宽度
                text_height += 15  # 额外增加15像素高度
                
                # 对微软雅黑字体进行特殊处理，增加更多空间
                if font_family == "微软雅黑":
                    text_width += 10  # 微软雅黑字体额外增加10像素宽度
                    text_height += 10  # 微软雅黑字体额外增加10像素高度
                
                # 计算文本在text_layer中的绘制位置
                # 为斜体文本预留左侧空间
                base_x = (bold_padding) + italic_padding // 2
                base_y = (bold_padding + underline_padding // 2)  # 为加粗和下划线效果预留空间
                
                # 创建与原图相同大小的透明图层
                watermark_layer = Image.new('RGBA', result.size, (0, 0, 0, 0))
                
                # 处理阴影效果（如果需要）
                if enable_shadow:
                    # 创建阴影图层
                    shadow_layer = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
                    shadow_draw = ImageDraw.Draw(shadow_layer)
                    
                    # 绘制阴影文本
                    shadow_draw.text((base_x, base_y), watermark_text, font=font, fill=shadow_color)
                    
                    # 应用阴影的加粗效果（如果需要）
                    if bold:
                        for dx in [-1, 1]:
                            for dy in [-1, 1]:
                                shadow_draw.text((base_x + dx, base_y + dy), watermark_text, font=font, fill=shadow_color)
                    
                    # 绘制阴影的下划线（如果需要）
                    if underline:
                        underline_thickness = max(2, int(font_size * 0.07))
                        underline_spacing = int(font_size * 0.08)
                        if font_family == "微软雅黑":
                            underline_spacing += int(font_size * 0.12)
                        baseline_y = base_y + bbox[3] + underline_spacing
                        baseline_y = max(base_y + bbox[3], baseline_y)
                        start_x = base_x + bbox[0]
                        end_x = base_x + bbox[2]
                        layer_width = shadow_layer.width
                        layer_height = shadow_layer.height
                        start_x = max(0, start_x)
                        end_x = min(layer_width, end_x)
                        baseline_y = max(underline_thickness, baseline_y)
                        baseline_y = min(layer_height - 1, baseline_y)
                        if end_x - start_x > 0:
                            shadow_draw.rectangle([(start_x, baseline_y), (end_x, baseline_y + underline_thickness - 1)], 
                                                 fill=shadow_color)
                    
                    # 处理阴影的斜体效果（如果需要）
                    if italic:
                        # 应用斜切变换 - 使用负的斜切因子实现正确的意大利斜体方向
                        skew_factor = -0.3
                        width, height = shadow_layer.size
                        new_width = width + int(height * abs(skew_factor))
                        
                        # 创建一个更大的图像来容纳斜切后的阴影
                        skew_shadow_layer = Image.new('RGBA', (new_width, height), (0, 0, 0, 0))
                        
                        # 逐像素应用斜切变换
                        for y in range(height):
                            for x in range(width):
                                pixel = shadow_layer.getpixel((x, y))
                                if pixel[3] > 0:  # 如果像素不透明
                                    new_x = x + int(y * skew_factor) + italic_padding // 2
                                    skew_shadow_layer.putpixel((new_x, y), pixel)
                        
                        # 更新shadow_layer为斜切后的图层
                        shadow_layer = skew_shadow_layer
                    
                    # 应用阴影的旋转
                    if rotation != 0:
                        shadow_layer = shadow_layer.rotate(rotation, expand=True)
                    
                    # 应用阴影的翻转
                    if flip_horizontal:
                        shadow_layer = shadow_layer.transpose(Image.FLIP_LEFT_RIGHT)
                    if flip_vertical:
                        shadow_layer = shadow_layer.transpose(Image.FLIP_TOP_BOTTOM)
                    
                    # 调整阴影透明度
                    shadow_alpha = shadow_layer.split()[3]
                    shadow_alpha = shadow_alpha.point(lambda p: p * (shadow_opacity / 100))
                    shadow_layer.putalpha(shadow_alpha)
                    
                    # 处理阴影的全图覆盖模式
                    if position == "full_cover":
                        # 计算水印间距（水印大小的1.5倍）
                        spacing_x = int(shadow_layer.width * 1.5)
                        spacing_y = int(shadow_layer.height * 1.5)
                        
                        # 在整个图片上以网格形式重复添加阴影
                        for x in range(-shadow_layer.width, watermark_layer.width + shadow_layer.width, spacing_x):
                            for y in range(-shadow_layer.height, watermark_layer.height + shadow_layer.height, spacing_y):
                                watermark_layer.paste(shadow_layer, (x + shadow_offset_x, y + shadow_offset_y), shadow_layer)
                    else:
                        # 常规位置模式
                        # 计算阴影位置
                        x, y = self._get_watermark_position(result.size, shadow_layer.size, position)
                        
                        # 确保阴影在图像范围内
                        x_offset = max(0, min(x - shadow_layer.width // 2, watermark_layer.width - shadow_layer.width))
                        y_offset = max(0, min(y - shadow_layer.height // 2, watermark_layer.height - shadow_layer.height))
                        
                        # 将阴影图层粘贴到透明图层
                        watermark_layer.paste(shadow_layer, (x_offset + shadow_offset_x, y_offset + shadow_offset_y), shadow_layer)
                
                # 创建主文字图层
                text_layer = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
                draw = ImageDraw.Draw(text_layer)
                
                # 绘制主文字
                draw.text((base_x, base_y), watermark_text, font=font, fill=font_color)
                
                # 应用主文字的加粗效果（如果需要）
                if bold:
                    for dx in [-1, 1]:
                        for dy in [-1, 1]:
                            draw.text((base_x + dx, base_y + dy), watermark_text, font=font, fill=font_color)
                
                # 绘制主文字的下划线（如果需要）
                if underline:
                    underline_thickness = max(2, int(font_size * 0.07))
                    underline_spacing = int(font_size * 0.08)
                    if font_family == "微软雅黑":
                        underline_spacing += int(font_size * 0.12)
                    baseline_y = base_y + bbox[3] + underline_spacing
                    baseline_y = max(base_y + bbox[3], baseline_y)
                    start_x = base_x + bbox[0]
                    end_x = base_x + bbox[2]
                    layer_width = text_layer.width
                    layer_height = text_layer.height
                    start_x = max(0, start_x)
                    end_x = min(layer_width, end_x)
                    baseline_y = max(underline_thickness, baseline_y)
                    baseline_y = min(layer_height - 1, baseline_y)
                    if end_x - start_x > 0:
                        draw.rectangle([(start_x, baseline_y), (end_x, baseline_y + underline_thickness - 1)], 
                                     fill=font_color)
                
                # 处理主文字的斜体效果（如果需要）
                if italic:
                    skew_factor = -0.3
                    width, height = text_layer.size
                    new_width = width + int(height * abs(skew_factor))
                    
                    skew_text_layer = Image.new('RGBA', (new_width, height), (0, 0, 0, 0))
                    
                    for y in range(height):
                        for x in range(width):
                            pixel = text_layer.getpixel((x, y))
                            if pixel[3] > 0:
                                new_x = x + int(y * skew_factor) + italic_padding // 2
                                skew_text_layer.putpixel((new_x, y), pixel)
                        
                    text_layer = skew_text_layer
                    draw = ImageDraw.Draw(text_layer)
                
                # 应用主文字的旋转
                if rotation != 0:
                    text_layer = text_layer.rotate(rotation, expand=True)
                
                # 应用主文字的翻转
                if flip_horizontal:
                    text_layer = text_layer.transpose(Image.FLIP_LEFT_RIGHT)
                if flip_vertical:
                    text_layer = text_layer.transpose(Image.FLIP_TOP_BOTTOM)
                
                # 调整主文字透明度
                alpha = text_layer.split()[3]
                alpha = alpha.point(lambda p: p * (opacity / 100))
                text_layer.putalpha(alpha)
                
                # 处理主文字的全图覆盖模式
                if position == "full_cover":
                    spacing_x = int(text_layer.width * 1.5)
                    spacing_y = int(text_layer.height * 1.5)
                    
                    for x in range(-text_layer.width, watermark_layer.width + text_layer.width, spacing_x):
                        for y in range(-text_layer.height, watermark_layer.height + text_layer.height, spacing_y):
                            watermark_layer.paste(text_layer, (x, y), text_layer)
                else:
                    # 常规位置模式
                    x, y = self._get_watermark_position(result.size, text_layer.size, position)
                    
                    x_offset = max(0, min(x - text_layer.width // 2, watermark_layer.width - text_layer.width))
                    y_offset = max(0, min(y - text_layer.height // 2, watermark_layer.height - text_layer.height))
                    
                    # 将主文字图层粘贴到透明图层
                    watermark_layer.paste(text_layer, (x_offset, y_offset), text_layer)
                
                # 合并图片
                result = Image.alpha_composite(result.convert('RGBA'), watermark_layer)
                result = result.convert('RGB')
            
            return result
        except Exception as e:
            print(f"添加文字水印时出错: {str(e)}")
            traceback.print_exc()
            return image
    
    def add_scattered_watermark(self, image, watermark_text, font_size=12, 
                               font_color="#000000", font_family="宋体",
                               bold=False, italic=False, underline=False,
                               opacity=20, rotation=0):
        """
        向Image对象添加分散水印
        将水印文字分散到图像的多个位置
        """
        try:
            if image.mode != 'RGB':
                image = image.copy().convert('RGB')
            else:
                image = image.copy()
            
            # 创建文字图层
            font = self._get_font(font_size, font_family, bold, italic, underline)
            draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # 计算水印间距
            spacing_x = int(image.width * 0.2)
            spacing_y = int(image.height * 0.2)
            
            # 创建透明图层
            watermark_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark_layer)
            
            # 在多个位置添加水印
            for x in range(0, image.width, spacing_x):
                for y in range(0, image.height, spacing_y):
                    # 随机旋转角度
                    random_rotation = rotation + (random.randint(-15, 15) if rotation == 0 else 0)
                    
                    # 创建旋转后的文字图层
                    text_layer = Image.new('RGBA', (text_width + 20, text_height + 20), (0, 0, 0, 0))
                    text_draw = ImageDraw.Draw(text_layer)
                    text_draw.text((10, 10), watermark_text, font=font, fill=font_color)
                    
                    # 旋转文字图层
                    if random_rotation != 0:
                        text_layer = text_layer.rotate(random_rotation, expand=True)
                    
                    # 调整透明度
                    alpha = text_layer.split()[3]
                    alpha = alpha.point(lambda p: p * (opacity / 100))
                    text_layer.putalpha(alpha)
                    
                    # 计算位置
                    pos_x = x - text_layer.width // 2
                    pos_y = y - text_layer.height // 2
                    
                    # 确保水印在图像范围内
                    pos_x = max(0, min(pos_x, image.width - text_layer.width))
                    pos_y = max(0, min(pos_y, image.height - text_layer.height))
                    
                    # 粘贴文字图层
                    watermark_layer.paste(text_layer, (pos_x, pos_y), text_layer)
            
            # 合并图片
            result = Image.alpha_composite(image.convert('RGBA'), watermark_layer)
            return result.convert('RGB')
        except Exception as e:
            print(f"添加分散水印时出错: {str(e)}")
            traceback.print_exc()
            return image
    
    def add_invisible_watermark(self, image, watermark_text, font_size=16, 
                               font_color="#000000", font_family="宋体",
                               position="center"):
        """
        向Image对象添加隐形水印
        使用极低的透明度或颜色差异
        """
        try:
            if image.mode != 'RGB':
                image = image.copy().convert('RGB')
            else:
                image = image.copy()
            
            # 创建文字图层
            font = self._get_font(font_size, font_family, False, False, False)
            draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # 创建透明图层
            watermark_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark_layer)
            
            # 计算位置
            x, y = self._get_watermark_position(image.size, (text_width, text_height), position)
            
            # 使用极低的透明度
            rgba_color = tuple(int(font_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (5,)  # 5%透明度
            
            # 绘制隐形文字
            draw.text((x - text_width // 2, y - text_height // 2), watermark_text, font=font, fill=rgba_color)
            
            # 合并图片
            result = Image.alpha_composite(image.convert('RGBA'), watermark_layer)
            return result.convert('RGB')
        except Exception as e:
            print(f"添加隐形水印时出错: {str(e)}")
            traceback.print_exc()
            return image
    
    def add_texture_watermark(self, image, watermark_text, font_size=24, 
                             font_color="#000000", font_family="宋体",
                             opacity=30, rotation=0):
        """
        向Image对象添加纹理水印
        将水印嵌入到图像纹理中，实现更自然的融合效果
        """
        try:
            if image.mode != 'RGB':
                image = image.copy().convert('RGB')
            else:
                image = image.copy()
            
            # 创建文字图层
            font = self._get_font(font_size, font_family, True, False, False)
            draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # 创建文字图像（使用更高的分辨率）
            text_layer = Image.new('RGBA', (text_width + 100, text_height + 100), (0, 0, 0, 0))
            text_draw = ImageDraw.Draw(text_layer)
            text_draw.text((50, 50), watermark_text, font=font, fill=font_color)
            
            # 旋转文字图层
            if rotation != 0:
                text_layer = text_layer.rotate(rotation, expand=True)
            
            # 调整透明度（使用更低的透明度实现纹理效果）
            alpha = text_layer.split()[3]
            alpha = alpha.point(lambda p: p * (opacity / 200))  # 降低透明度，实现更自然的纹理
            text_layer.putalpha(alpha)
            
            # 计算位置（使用平铺模式而不是单一位置）
            result = image.copy()
            
            # 平铺水印，创建纹理效果
            tile_width, tile_height = text_layer.size
            
            # 计算平铺的行数和列数
            cols = max(2, image.width // (tile_width // 2))
            rows = max(2, image.height // (tile_height // 2))
            
            # 在图像上平铺水印
            for i in range(rows):
                for j in range(cols):
                    # 计算位置（交错排列，避免过于规律）
                    x_offset = j * tile_width // 2 + (i % 2) * tile_width // 4
                    y_offset = i * tile_height // 2
                    
                    # 确保在图像范围内
                    if x_offset < image.width and y_offset < image.height:
                        # 创建水印副本，避免修改原始水印
                        watermark_tile = text_layer.copy()
                        
                        # 随机轻微旋转每个水印（±5度），增加自然感
                        random_rotation = random.uniform(-5, 5)
                        watermark_tile = watermark_tile.rotate(random_rotation, expand=True)
                        
                        # 随机轻微缩放（±10%），增加变化
                        scale_factor = random.uniform(0.9, 1.1)
                        new_width = int(watermark_tile.width * scale_factor)
                        new_height = int(watermark_tile.height * scale_factor)
                        watermark_tile = watermark_tile.resize((new_width, new_height), Image.LANCZOS)
                        
                        # 粘贴水印
                        try:
                            result.paste(watermark_tile, (x_offset, y_offset), watermark_tile)
                        except:
                            # 如果粘贴失败（例如超出边界），跳过
                            pass
            
            # 应用轻微的模糊效果，使水印更自然地融入纹理
            result = result.filter(ImageFilter.GaussianBlur(radius=0.5))
            
            # 调整整体对比度，使水印与图像更融合
            enhancer = ImageEnhance.Contrast(result)
            result = enhancer.enhance(1.02)
            
            return result.convert('RGB')
        except Exception as e:
            print(f"添加纹理水印时出错: {str(e)}")
            traceback.print_exc()
            return image
    
    def _process_single_text_watermark(self, image_path, watermark_text, output_path,
                                      font_size=24, font_color="#000000", font_family="宋体",
                                      bold=False, italic=False, underline=False,
                                      position="center", opacity=50, rotation=0,
                                      flip_horizontal=False, flip_vertical=False,
                                      scattered_watermark=False, invisible_watermark=False, texture_watermark=False,
                                      enable_shadow=False, shadow_color="#000000", shadow_offset_x=2, shadow_offset_y=2, shadow_opacity=30):
        """
        处理单张图片的文字水印
        """
        # 添加水印
        success = self.add_text_watermark(
            image_path, watermark_text, output_path,
            font_size, font_color, font_family, bold, italic, underline,
            position, opacity, rotation,
            flip_horizontal, flip_vertical, scattered_watermark, invisible_watermark, texture_watermark,
            enable_shadow, shadow_color, shadow_offset_x, shadow_offset_y, shadow_opacity
        )
        return (image_path, output_path, success)
    
    def batch_add_text_watermark(self, image_paths, watermark_text, output_dir,
                                font_size=24, font_color="#000000", font_family="宋体",
                                bold=False, italic=False, underline=False,
                                position="center", opacity=50, rotation=0,
                                flip_horizontal=False, flip_vertical=False, progress_callback=None,
                                scattered_watermark=False, invisible_watermark=False, texture_watermark=False,
                                enable_shadow=False, shadow_color="#000000", shadow_offset_x=2, shadow_offset_y=2, shadow_opacity=30,
                                security_watermark=False, security_key="", security_strength=0.02):
        """
        批量添加文字水印（多线程优化版）
        
        Args:
            image_paths: 图片路径列表
            watermark_text: 水印文字
            output_dir: 输出目录
            font_size: 字体大小
            font_color: 字体颜色
            font_family: 字体族
            bold: 是否粗体
            italic: 是否斜体
            underline: 是否下划线
            position: 水印位置
            opacity: 透明度
            rotation: 旋转角度
            flip_horizontal: 是否水平翻转
            flip_vertical: 是否垂直翻转
            progress_callback: 进度回调函数，接收已完成数量和总数
        """
        results = []
        print(f"开始批量添加文字水印，共处理 {len(image_paths)} 张图片")
        
        # 准备参数列表
        params = []
        for image_path in image_paths:
            # 获取输出文件名
            filename = os.path.basename(image_path)
            output_path = os.path.join(output_dir, filename)
            params.append((image_path, watermark_text, output_path, font_size, font_color, font_family, 
                          bold, italic, underline, position, opacity, rotation, 
                          flip_horizontal, flip_vertical, scattered_watermark, invisible_watermark, texture_watermark, 
                          enable_shadow, shadow_color, shadow_offset_x, shadow_offset_y, shadow_opacity))
        
        # 使用多线程并行处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            # 提交所有任务
            futures = [executor.submit(self._process_single_text_watermark, *param) for param in params]
            
            # 收集结果
            completed_count = 0
            for future in concurrent.futures.as_completed(futures):
                image_path, output_path, success = future.result()
                results.append((image_path, output_path, success))
                completed_count += 1
                print(f"处理第 {completed_count}/{len(image_paths)} 张图片: {image_path} {'成功' if success else '失败'}")
                
                # 调用进度回调
                if progress_callback:
                    progress_callback(completed_count, len(image_paths))
        
        print(f"批量添加文字水印完成，成功 {sum(1 for _, _, s in results if s)} 张，失败 {sum(1 for _, _, s in results if not s)} 张")
        return results