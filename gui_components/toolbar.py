import tkinter as tk
from tkinter import ttk
from gui_components.theme import COLORS, FONTS, SPACING, create_modern_button


class Toolbar:
    """工具栏组件"""
    
    def __init__(self, root, gui):
        self.root = root
        self.gui = gui
        self.create_toolbar()
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = tk.Frame(self.root, bg=COLORS['background'], bd=0, relief=tk.FLAT, height=50)
        toolbar.grid(row=0, column=0, sticky="ew", padx=SPACING['large'], pady=SPACING['medium'])
        
        # 工具栏容器
        toolbar_container = tk.Frame(toolbar, bg=COLORS['background_light'], bd=1, relief=tk.SOLID)
        toolbar_container.pack(fill="x", padx=0, pady=0)
        
        # 按钮容器
        button_frame = tk.Frame(toolbar_container, bg=COLORS['background_light'])
        button_frame.pack(fill="x", padx=SPACING['medium'], pady=SPACING['medium'])
        
        # 打开图片按钮
        open_button = create_modern_button(button_frame, "打开图片", self.gui.load_image, style='primary')
        open_button.pack(side="left", padx=SPACING['small'])
        
        # 保存图片按钮
        save_button = create_modern_button(button_frame, "保存图片", self.gui.save_image, style='primary')
        save_button.pack(side="left", padx=SPACING['small'])
        
        # 批量处理按钮
        batch_button = create_modern_button(button_frame, "批量处理", self.gui.batch_process, style='secondary')
        batch_button.pack(side="left", padx=SPACING['small'])
        
        # 清除水印按钮
        clear_button = create_modern_button(button_frame, "清除水印", self.gui.clear_watermark, style='secondary')
        clear_button.pack(side="left", padx=SPACING['small'])
        
        # 添加分隔符
        separator = ttk.Separator(button_frame, orient='vertical')
        separator.pack(side="left", padx=SPACING['medium'], fill="y", pady=SPACING['small'])
        
        # 智能放置按钮
        smart_button = create_modern_button(button_frame, "智能放置", self.gui.smart_watermark_position, style='secondary')
        smart_button.pack(side="left", padx=SPACING['small'])
        
        # 保存样式按钮
        save_style_button = create_modern_button(button_frame, "保存样式", self.gui.save_style, style='secondary')
        save_style_button.pack(side="left", padx=SPACING['small'])
        
        # 加载样式按钮
        load_style_button = create_modern_button(button_frame, "加载样式", self.gui.load_style, style='secondary')
        load_style_button.pack(side="left", padx=SPACING['small'])
        
        # 保存按钮引用，用于状态管理
        self.save_button = save_button
        self.batch_button = batch_button
        self.clear_button = clear_button
        self.smart_button = smart_button
        self.save_style_button = save_style_button
        self.load_style_button = load_style_button
        
        # 初始状态：图片未加载时禁用相关按钮
        self.update_control_states(False, False)
    
    def update_control_states(self, image_loaded, logo_selected):
        """根据当前状态更新按钮启用/禁用状态"""
        # 保存按钮：图片已加载且有水印时才启用
        save_enabled = image_loaded and self.gui.watermarked_image is not None
        self.save_button.config(state=tk.NORMAL if save_enabled else tk.DISABLED)
        
        # 批量处理按钮：图片已加载且Logo已选择（如果是Logo水印）
        batch_enabled = image_loaded
        if hasattr(self.gui, 'watermark_type') and self.gui.watermark_type.get() == "logo":
            batch_enabled = batch_enabled and logo_selected
        self.batch_button.config(state=tk.NORMAL if batch_enabled else tk.DISABLED)
        
        # 清除水印按钮：图片已加载且有水印时才启用
        clear_enabled = image_loaded and self.gui.watermarked_image is not None and self.gui.watermarked_image != self.gui.original_image
        self.clear_button.config(state=tk.NORMAL if clear_enabled else tk.DISABLED)
        
        # 智能放置按钮：图片已加载时即可启用（文字和图片水印都可用）
        smart_enabled = image_loaded
        self.smart_button.config(state=tk.NORMAL if smart_enabled else tk.DISABLED)
        
        # 样式按钮：始终启用
        self.save_style_button.config(state=tk.NORMAL)
        self.load_style_button.config(state=tk.NORMAL)