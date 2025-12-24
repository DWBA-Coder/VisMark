"""
Logo水印处理器类
提供Logo水印的添加功能
"""

import os
import traceback
import concurrent.futures
from PIL import Image
from .base_processor import BaseWatermarkProcessor


class LogoWatermarkProcessor(BaseWatermarkProcessor):
    """Logo水印处理器"""
    
    def add_logo_watermark(self, image_path, logo_path, output_path,
                         logo_size=100, position="center", opacity=50, rotation=0,
                         flip_horizontal=False, flip_vertical=False, recolor_color=None):
        """
        添加Logo水印到图片
        
        参数:
            image_path: 原始图片路径
            logo_path: Logo图片路径
            output_path: 输出图片路径
            logo_size: Logo大小
            position: 水印位置
            opacity: 透明度 (0-100)
            rotation: 旋转角度 (-180到180)
            flip_horizontal: 是否水平翻转
            flip_vertical: 是否垂直翻转
            
        返回:
            bool: 是否成功添加水印
        """
        try:
            # 打开原始图片
            image = Image.open(image_path).convert("RGBA")
            
            # 添加水印
            watermarked_image = self.add_logo_watermark_to_image(
                image, logo_path, logo_size, position, opacity, rotation, flip_horizontal, flip_vertical
            )
            
            # 保存图片
            return self._save_image(watermarked_image, output_path)
        except Exception as e:
            print(f"添加Logo水印时出错: {str(e)}")
            traceback.print_exc()
            return False
    
    def add_logo_watermark_to_image(self, image, logo_path, logo_size=100,
                                    position="center", opacity=50, rotation=0,
                                    flip_horizontal=False, flip_vertical=False,
                                    recolor_color=None):
        """
        向Image对象添加Logo水印
        
        参数:
            recolor_color: 重着色颜色，格式为 "#RRGGBB" 或 "#RRGGBBAA"
        """
        # 打开Logo图片并确保转换为RGBA模式
        try:
            logo = Image.open(logo_path)
            # 统一转换为RGBA模式以确保alpha通道存在
            logo = logo.convert("RGBA")
            
            # 应用重着色
            if recolor_color:
                logo = self._recolor_logo(logo, recolor_color)
                
        except Exception as e:
            print(f"处理Logo时出错: {str(e)}")
            traceback.print_exc()
            return image
        
        # 调整Logo大小 - 始终锁定宽高比
        original_width, original_height = logo.size
        
        if original_width > original_height:
            new_width = logo_size
            new_height = int(original_height * (logo_size / original_width))
        else:
            new_height = logo_size
            new_width = int(original_width * (logo_size / original_height))
        
        logo = logo.resize((new_width, new_height), Image.LANCZOS)
        
        # 旋转Logo
        if rotation != 0:
            logo = logo.rotate(rotation, expand=True)
        
        # 翻转Logo
        if flip_horizontal:
            logo = logo.transpose(Image.FLIP_LEFT_RIGHT)
        if flip_vertical:
            logo = logo.transpose(Image.FLIP_TOP_BOTTOM)
        
        # 调整透明度
        alpha = logo.split()[3]
        alpha = alpha.point(lambda p: p * (opacity / 100))
        logo.putalpha(alpha)
        
        # 创建一个新图像用于合并
        watermarked_image = image.copy()
        
        # 处理全图覆盖模式
        if position == "full_cover":
            # 计算水印间距（水印大小的1.5倍）
            spacing_x = int(logo.width * 1.5)
            spacing_y = int(logo.height * 1.5)
            
            # 在整个图片上以网格形式重复添加水印
            for x in range(-logo.width, watermarked_image.width + logo.width, spacing_x):
                for y in range(-logo.height, watermarked_image.height + logo.height, spacing_y):
                    watermarked_image.paste(logo, (x, y), logo)
        else:
            # 常规位置模式
            # 获取水印位置
            x, y = self._get_watermark_position(image.size, logo.size, position)
            
            # 确保水印在图像范围内
            x_offset = max(0, min(x - logo.width // 2, watermarked_image.width - logo.width))
            y_offset = max(0, min(y - logo.height // 2, watermarked_image.height - logo.height))
            
            # 合并图像
            watermarked_image.paste(logo, (x_offset, y_offset), logo)
        
        return watermarked_image
    
    def _recolor_logo(self, logo_image, color):
        """
        对Logo图片进行重着色
        
        参数:
            logo_image: PIL Image对象 (RGBA模式)
            color: 颜色字符串，格式为 "#RRGGBB" 或 "#RRGGBBAA"
            
        返回:
            重着色后的PIL Image对象
        """
        # 解析颜色值
        if color.startswith('#'):
            color = color[1:]
        
        if len(color) == 6:  # #RRGGBB
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            a = 255  # 默认不透明
        elif len(color) == 8:  # #RRGGBBAA
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            a = int(color[6:8], 16)
        else:
            # 无效颜色格式，返回原图
            return logo_image
        
        # 创建重着色后的图像
        recolored = Image.new("RGBA", logo_image.size, (r, g, b, a))
        
        # 使用原图的alpha通道作为蒙版
        if logo_image.mode == "RGBA":
            alpha = logo_image.split()[3]
            recolored.putalpha(alpha)
        
        return recolored
    
    def _process_single_logo_watermark(self, image_path, logo_path, output_path,
                                      logo_size=100, position="center", opacity=50, rotation=0,
                                      flip_horizontal=False, flip_vertical=False, recolor_color=None):
        """
        处理单张图片的Logo水印
        """
        # 添加水印
        success = self.add_logo_watermark(
            image_path, logo_path, output_path,
            logo_size, position, opacity, rotation,
            flip_horizontal, flip_vertical, recolor_color
        )
        return (image_path, output_path, success)
    
    def batch_add_logo_watermark(self, image_paths, logo_path, output_dir,
                                logo_size=100, position="center", opacity=50, rotation=0,
                                flip_horizontal=False, flip_vertical=False, 
                                recolor_color=None, progress_callback=None):
        """
        批量添加Logo水印（多线程优化版）
        
        Args:
            image_paths: 图片路径列表
            logo_path: Logo图片路径
            output_dir: 输出目录
            logo_size: Logo大小
            position: 水印位置
            opacity: 透明度
            rotation: 旋转角度
            flip_horizontal: 是否水平翻转
            flip_vertical: 是否垂直翻转
            progress_callback: 进度回调函数，接收已完成数量和总数
        """
        results = []
        print(f"开始批量添加Logo水印，共处理 {len(image_paths)} 张图片")
        
        # 准备参数列表
        params = []
        for image_path in image_paths:
            # 获取输出文件名
            filename = os.path.basename(image_path)
            output_path = os.path.join(output_dir, filename)
            params.append((image_path, logo_path, output_path, logo_size, 
                          position, opacity, rotation, flip_horizontal, flip_vertical, recolor_color))
        
        # 使用多线程并行处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            # 提交所有任务
            futures = [executor.submit(self._process_single_logo_watermark, *param) for param in params]
            
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
        
        print(f"批量添加Logo水印完成，成功 {sum(1 for _, _, s in results if s)} 张，失败 {sum(1 for _, _, s in results if not s)} 张")
        return results