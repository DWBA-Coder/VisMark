"""
水印处理模块包
提供文字水印、Logo水印和安全水印功能
"""

from .base_processor import BaseWatermarkProcessor
from .text_watermark import TextWatermarkProcessor
from .logo_watermark import LogoWatermarkProcessor
from .security_watermark import SecurityWatermarkProcessor
from .watermark_processor import WatermarkProcessor

# 保持向后兼容性
__all__ = ['WatermarkProcessor', 'BaseWatermarkProcessor', 'TextWatermarkProcessor', 'LogoWatermarkProcessor', 'SecurityWatermarkProcessor']