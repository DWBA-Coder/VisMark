"""
主水印处理器类
整合文字水印、Logo水印和安全水印功能，保持向后兼容性
"""

from .text_watermark import TextWatermarkProcessor
from .logo_watermark import LogoWatermarkProcessor
from .security_watermark import SecurityWatermarkProcessor


class WatermarkProcessor(TextWatermarkProcessor, LogoWatermarkProcessor, SecurityWatermarkProcessor):
    """
    水印处理器类，负责添加文字水印和Logo水印
    继承自各个功能模块，提供统一的接口
    """
    
    def __init__(self):
        # 调用各个父类的初始化方法
        TextWatermarkProcessor.__init__(self)
        LogoWatermarkProcessor.__init__(self)
        SecurityWatermarkProcessor.__init__(self)