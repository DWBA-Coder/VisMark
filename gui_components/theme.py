"""
GUI主题配置
专业、简洁的界面设计
"""

import tkinter as tk
from tkinter import ttk

# 颜色方案 - 桂电蓝色系，专业稳重
COLORS = {
    # 主色调 - 桂电蓝系列
    'primary': '#005FA5',        # 桂电蓝（主色调）
    'primary_light': '#2a7bb9',  # 稍亮的桂电蓝
    'primary_dark': '#00457a',   # 更深的桂电蓝
    
    # 辅助色 - 基于桂电蓝的渐变
    'secondary': '#0078c8',      # 辅助蓝
    'secondary_light': '#4a9ad4', # 浅辅助蓝
    'secondary_dark': '#005a9c',  # 深辅助蓝
    
    # 背景色 - 浅色系，专业舒适
    'background': '#f5f7fa',     # 极浅灰蓝
    'background_light': '#ffffff', # 纯白
    'background_dark': '#eef2f7',  # 浅灰蓝
    
    # 文字色 - 深色系，易读
    'text_primary': '#1e2a3a',   # 深蓝黑
    'text_secondary': '#5a6778', # 中灰蓝
    'text_light': '#8c98a8',     # 浅灰蓝
    'text_dark': '#1e2a3a',      # 深蓝黑
    
    # 边框和分隔线
    'border': '#d8e1ea',         # 浅蓝灰边框
    'border_light': '#f0f4f8',   # 极浅蓝灰边框
    'border_dark': '#c0cdd8',    # 中等蓝灰边框
    
    # 状态色 - 专业但不刺眼
    'success': '#2e7d32',        # 深绿色
    'warning': '#f57c00',        # 橙色
    'error': '#d32f2f',          # 红色
    'info': '#005FA5'            # 桂电蓝
}

# 字体配置
FONTS = {
    'title': ('黑体', 12, 'bold'),
    'subtitle': ('黑体', 10, 'bold'),
    'body': ('黑体', 9),
    'small': ('黑体', 8),
    'button': ('黑体', 9, 'bold')
}

# 间距和尺寸
SPACING = {
    'small': 2,
    'medium': 5,
    'large': 10,
    'xlarge': 15
}

# 边框圆角
BORDER_RADIUS = {
    'small': 2,
    'medium': 4,
    'large': 6
}

# 阴影效果
SHADOWS = {
    'light': '0 1px 3px rgba(0,0,0,0.1)',
    'medium': '0 2px 6px rgba(0,0,0,0.15)',
    'heavy': '0 4px 12px rgba(0,0,0,0.2)'
}

# 样式配置函数
def configure_styles():
    """配置tkinter样式"""
    style = ttk.Style()
    
    # 配置主题
    style.theme_use('clam')  # 使用clam主题作为基础
    
    # 配置按钮样式
    style.configure('Primary.TButton',
                   background=COLORS['primary'],
                   foreground=COLORS['background_light'],  # 白色文字在蓝色背景上
                   borderwidth=1,
                   focusthickness=3,
                   focuscolor=COLORS['primary_light'],
                   padding=(10, 5))
    
    # 配置Primary.TButton的悬停状态
    style.map('Primary.TButton',
              background=[('active', COLORS['primary_light']),  # 悬停时保持蓝色背景
                         ('pressed', COLORS['primary_dark'])])
    
    # 配置Secondary.TButton的悬停状态
    style.map('Secondary.TButton',
              background=[('active', COLORS['background_dark']),  # 悬停时变为浅灰色
                         ('pressed', COLORS['border_light'])])
    
    style.configure('Secondary.TButton',
                   background=COLORS['background_light'],
                   foreground=COLORS['text_primary'],  # 深色文字在白色背景上
                   borderwidth=1,
                   border=COLORS['border'],
                   focusthickness=3,
                   focuscolor=COLORS['border_light'])
    
    # 配置标签样式
    style.configure('Title.TLabel',
                   background=COLORS['background'],
                   foreground=COLORS['primary'],
                   font=FONTS['title'])
    
    style.configure('Subtitle.TLabel',
                   background=COLORS['background'],
                   foreground=COLORS['primary'],
                   font=FONTS['subtitle'])
    
    # 配置框架样式
    style.configure('Card.TFrame',
                   background=COLORS['background_light'],
                   borderwidth=1,
                   relief='solid')
    
    style.configure('Section.TFrame',
                   background=COLORS['background'])
    
    # 配置输入框样式
    style.configure('Modern.TEntry',
                   fieldbackground=COLORS['background_light'],
                   borderwidth=1,
                   relief='solid')
    
    # 配置组合框样式
    style.configure('Modern.TCombobox',
                   fieldbackground=COLORS['background_light'],
                   background=COLORS['background_light'])
    
    # 配置滚动条样式
    style.configure('Modern.Vertical.TScrollbar',
                   background=COLORS['border_light'],
                   troughcolor=COLORS['background'])

# 工具函数
def create_section_title(parent, text, bg_color=None):
    """创建分区标题"""
    if bg_color is None:
        bg_color = COLORS['background']
    
    title_frame = tk.Frame(parent, bg=bg_color, height=30)
    
    # 标题容器，带桂电蓝背景
    title_container = tk.Frame(title_frame, bg=COLORS['primary'], height=28)
    title_container.pack(fill='x', padx=0, pady=(0, SPACING['small']))
    
    title_label = tk.Label(title_container, 
                          text=text, 
                          bg=COLORS['primary'],
                          fg=COLORS['background_light'],
                          font=("黑体", 10, "bold"),
                          anchor='w')
    title_label.pack(fill='x', padx=SPACING['medium'], pady=SPACING['small'])
    
    return title_frame

def create_card_frame(parent, **kwargs):
    """创建卡片式框架"""
    return tk.Frame(parent, 
                   bg=COLORS['background_light'],
                   bd=1, 
                   relief='solid',
                   **kwargs)

def create_modern_button(parent, text, command, style='primary'):
    """创建现代风格按钮"""
    if style == 'primary':
        return ttk.Button(parent, text=text, command=command, style='Primary.TButton')
    else:
        return ttk.Button(parent, text=text, command=command, style='Secondary.TButton')