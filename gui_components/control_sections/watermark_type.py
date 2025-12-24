import tkinter as tk
from gui_components.theme import COLORS, SPACING, create_card_frame


class WatermarkTypeSection:
    """水印类型选择部分"""
    
    def __init__(self, parent, gui):
        self.parent = parent
        self.gui = gui
        self.create_section()
    
    def create_section(self):
        """创建水印类型选择部分"""
        # 创建卡片式容器
        card_frame = create_card_frame(self.parent)
        card_frame.pack(pady=SPACING['small'], padx=SPACING['medium'], fill=tk.X)
        
        # 标题标签 - 使用黑体
        title_label = tk.Label(card_frame, text="水印类型", 
                              bg=COLORS['background_light'], 
                              fg=COLORS['text_primary'],
                              font=("黑体", 12, "bold"),
                              anchor='w')
        title_label.pack(pady=(SPACING['medium'], SPACING['small']), padx=SPACING['medium'], fill=tk.X)
        
        # 按钮容器
        button_frame = tk.Frame(card_frame, bg=COLORS['background_light'])
        button_frame.pack(pady=SPACING['small'], padx=SPACING['medium'], fill=tk.X)
        
        # 初始化变量（如果不存在）
        if not hasattr(self.gui, 'watermark_type'):
            self.gui.watermark_type = tk.StringVar(value="text")
        
        # 文字水印按钮
        self.text_button = tk.Button(button_frame, 
                                   text="文字水印", 
                                   bg=COLORS['primary'],
                                   fg=COLORS['background_light'],
                                   font=("黑体", 10, "bold"),
                                   relief="raised",
                                   bd=2,
                                   padx=20,
                                   pady=8,
                                   command=lambda: self._set_watermark_type("text"))
        self.text_button.pack(side="left", padx=(0, SPACING['large']))
        
        # 图片水印按钮
        self.logo_button = tk.Button(button_frame, 
                                   text="图片水印", 
                                   bg=COLORS['background_light'],
                                   fg=COLORS['text_primary'],
                                   font=("黑体", 10, "bold"),
                                   relief="raised",
                                   bd=2,
                                   padx=20,
                                   pady=8,
                                   command=lambda: self._set_watermark_type("logo"))
        self.logo_button.pack(side="left")
        
        # 创建按钮样式（必须在按钮创建后调用）
        self._create_button_style()
        
        # 初始化按钮状态
        self._update_button_states()
        
        # 添加分隔线
        separator = tk.Frame(card_frame, bg=COLORS['border'], height=1)
        separator.pack(fill="x", padx=SPACING['medium'], pady=(SPACING['small'], 0))
    
    def _create_button_style(self):
        """创建按钮样式"""
        # 定义按钮悬停效果
        def on_enter(event, button, is_selected=False):
            if not is_selected:
                button.config(bg=COLORS['primary_light'] if button == self.text_button else COLORS['background_dark'])
        
        def on_leave(event, button, is_selected=False):
            if not is_selected:
                button.config(bg=COLORS['primary'] if button == self.text_button and self.gui.watermark_type.get() == "text" 
                             else COLORS['background_light'] if button == self.logo_button and self.gui.watermark_type.get() == "logo" 
                             else COLORS['background_light'])
        
        # 绑定事件到按钮
        self.text_button.bind("<Enter>", lambda e: on_enter(e, self.text_button, self.gui.watermark_type.get() == "text"))
        self.text_button.bind("<Leave>", lambda e: on_leave(e, self.text_button, self.gui.watermark_type.get() == "text"))
        
        self.logo_button.bind("<Enter>", lambda e: on_enter(e, self.logo_button, self.gui.watermark_type.get() == "logo"))
        self.logo_button.bind("<Leave>", lambda e: on_leave(e, self.logo_button, self.gui.watermark_type.get() == "logo"))
    
    def _set_watermark_type(self, watermark_type):
        """设置水印类型"""
        self.gui.watermark_type.set(watermark_type)
        self._update_button_states()
        
        # 通过ControlPanel的toggle_watermark_type方法来处理组件显示/隐藏
        if hasattr(self.gui, 'control_panel') and hasattr(self.gui.control_panel, 'toggle_watermark_type'):
            self.gui.control_panel.toggle_watermark_type()
    
    def _update_button_states(self):
        """更新按钮状态"""
        current_type = self.gui.watermark_type.get()
        
        # 文字水印按钮状态
        if current_type == "text":
            self.text_button.config(bg=COLORS['primary'], 
                                  fg=COLORS['background_light'],
                                  relief="sunken")
            self.logo_button.config(bg=COLORS['background_light'], 
                                  fg=COLORS['text_primary'],
                                  relief="raised")
        else:
            self.text_button.config(bg=COLORS['background_light'], 
                                  fg=COLORS['text_primary'],
                                  relief="raised")
            self.logo_button.config(bg=COLORS['primary'], 
                                  fg=COLORS['background_light'],
                                  relief="sunken")