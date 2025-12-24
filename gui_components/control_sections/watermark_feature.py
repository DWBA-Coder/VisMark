import tkinter as tk
from gui_components.theme import COLORS, SPACING, create_card_frame


class WatermarkFeatureSection:
    """水印功能选择部分"""
    
    def __init__(self, parent, gui):
        self.parent = parent
        self.gui = gui
        self.create_section()
    
    def create_section(self):
        """创建水印功能选择部分"""
        # 创建卡片式容器
        card_frame = create_card_frame(self.parent)
        card_frame.pack(pady=SPACING['small'], padx=SPACING['medium'], fill=tk.X)
        
        # 标题标签 - 使用黑体并靠左显示
        title_label = tk.Label(card_frame, text="水印功能", 
                              bg=COLORS['background_light'], 
                              fg=COLORS['text_primary'],
                              font=("黑体", 12, "bold"),
                              anchor='w')
        title_label.pack(pady=(SPACING['medium'], SPACING['small']), padx=SPACING['medium'], fill=tk.X)
        
        feature_frame = tk.Frame(card_frame, bg=COLORS['background_light'])
        feature_frame.pack(pady=SPACING['small'], padx=SPACING['medium'], fill=tk.X)
        
        # 初始化变量（如果不存在）
        if not hasattr(self.gui, 'normal_watermark_var'):
            self.gui.normal_watermark_var = tk.BooleanVar(value=True)
        if not hasattr(self.gui, 'scattered_watermark_var'):
            self.gui.scattered_watermark_var = tk.BooleanVar(value=False)
        if not hasattr(self.gui, 'invisible_watermark_var'):
            self.gui.invisible_watermark_var = tk.BooleanVar(value=False)
        if not hasattr(self.gui, 'texture_watermark_var'):
            self.gui.texture_watermark_var = tk.BooleanVar(value=False)
        if not hasattr(self.gui, 'security_watermark_var'):
            self.gui.security_watermark_var = tk.BooleanVar(value=False)
        if not hasattr(self.gui, 'security_strength_var'):
            self.gui.security_strength_var = tk.DoubleVar(value=0.02)
        
        # 创建水印功能单选按钮组
        self.watermark_feature_var = tk.StringVar(value="normal")
        
        # 普通水印选项 - 改为圆形单选框
        tk.Radiobutton(feature_frame, text="普通水印", variable=self.watermark_feature_var, 
                      value="normal", bg=COLORS['background_light'],
                      fg=COLORS['text_primary'],
                      activebackground=COLORS['background_light'],
                      activeforeground=COLORS['secondary'],
                      selectcolor=COLORS['background_light'],
                      font=("黑体", 9),
                      command=self._on_feature_change).pack(anchor="w", padx=5, pady=2)
        
        # 安全增强选项标题
        tk.Label(feature_frame, text="安全增强", bg=COLORS['background_light'], 
                font=("黑体", 10, "bold"), anchor='w').pack(anchor="w", padx=5, pady=(5, 2))
        
        # 分散水印 - 改为圆形单选框
        tk.Radiobutton(feature_frame, text="分散水印", variable=self.watermark_feature_var, 
                      value="scattered", bg=COLORS['background_light'],
                      fg=COLORS['text_primary'],
                      activebackground=COLORS['background_light'],
                      activeforeground=COLORS['secondary'],
                      selectcolor=COLORS['background_light'],
                      font=("黑体", 9),
                      command=self._on_feature_change).pack(anchor="w", padx=20, pady=2)
        
        # 隐形水印 - 改为圆形单选框
        tk.Radiobutton(feature_frame, text="隐形水印", variable=self.watermark_feature_var, 
                      value="invisible", bg=COLORS['background_light'],
                      fg=COLORS['text_primary'],
                      activebackground=COLORS['background_light'],
                      activeforeground=COLORS['secondary'],
                      selectcolor=COLORS['background_light'],
                      font=("黑体", 9),
                      command=self._on_feature_change).pack(anchor="w", padx=20, pady=2)
        
        # 纹理水印 - 改为圆形单选框
        tk.Radiobutton(feature_frame, text="纹理水印", variable=self.watermark_feature_var, 
                      value="texture", bg=COLORS['background_light'],
                      fg=COLORS['text_primary'],
                      activebackground=COLORS['background_light'],
                      activeforeground=COLORS['secondary'],
                      selectcolor=COLORS['background_light'],
                      font=("黑体", 9),
                      command=self._on_feature_change).pack(anchor="w", padx=20, pady=2)
        
        # DCT安全水印（频域加密） - 改为圆形单选框
        tk.Radiobutton(feature_frame, text="DCT安全水印", variable=self.watermark_feature_var, 
                      value="security", bg=COLORS['background_light'],
                      fg=COLORS['text_primary'],
                      activebackground=COLORS['background_light'],
                      activeforeground=COLORS['secondary'],
                      selectcolor=COLORS['background_light'],
                      font=("黑体", 9),
                      command=self._on_feature_change).pack(anchor="w", padx=20, pady=2)
        
        # 安全水印密钥输入 - 始终显示
        if not hasattr(self.gui, 'security_key_frame'):
            self.gui.security_key_frame = tk.Frame(feature_frame, bg=COLORS['background_light'])
        self.gui.security_key_frame.pack(anchor="w", padx=30, pady=2)
        
        tk.Label(self.gui.security_key_frame, text="密钥", bg=COLORS['background_light'], 
                width=8, font=("黑体", 9)).pack(side="left", pady=2)
        if not hasattr(self.gui, 'security_key_entry') or self.gui.security_key_entry is None:
            self.gui.security_key_entry = tk.Entry(self.gui.security_key_frame, width=20, show="*")
        self.gui.security_key_entry.pack(side="left", pady=2)
        self.gui.security_key_entry.delete(0, tk.END)
        self.gui.security_key_entry.insert(0, "watermark123")
        
        # 水印强度（仅安全水印） - 始终显示
        if not hasattr(self.gui, 'security_strength_frame'):
            self.gui.security_strength_frame = tk.Frame(feature_frame, bg=COLORS['background_light'])
        self.gui.security_strength_frame.pack(anchor="w", padx=30, pady=2)
        
        tk.Label(self.gui.security_strength_frame, text="水印强度", bg=COLORS['background_light'], 
                width=8, font=("黑体", 9)).pack(side="left", pady=2)
        tk.Scale(self.gui.security_strength_frame, from_=0.01, to=0.1, resolution=0.01, 
                 orient="horizontal", variable=self.gui.security_strength_var, length=150, 
                 bg=COLORS['background_light']).pack(side="left", pady=2)
        
        # 添加分隔线
        separator = tk.Frame(card_frame, bg=COLORS['border'], height=1)
        separator.pack(fill="x", padx=SPACING['medium'], pady=(SPACING['small'], 0))
    
    def _on_feature_change(self):
        """水印功能选项改变时的回调函数"""
        selected_feature = self.watermark_feature_var.get()
        
        # 更新对应的布尔变量
        if hasattr(self.gui, 'normal_watermark_var'):
            self.gui.normal_watermark_var.set(selected_feature == "normal")
        if hasattr(self.gui, 'scattered_watermark_var'):
            self.gui.scattered_watermark_var.set(selected_feature == "scattered")
        if hasattr(self.gui, 'invisible_watermark_var'):
            self.gui.invisible_watermark_var.set(selected_feature == "invisible")
        if hasattr(self.gui, 'texture_watermark_var'):
            self.gui.texture_watermark_var.set(selected_feature == "texture")
        if hasattr(self.gui, 'security_watermark_var'):
            self.gui.security_watermark_var.set(selected_feature == "security")
        
        # 调用控制面板的相应方法
        if hasattr(self.gui, 'control_panel'):
            if selected_feature == "normal":
                self.gui.control_panel.toggle_normal_watermark()
            elif selected_feature in ["scattered", "invisible", "texture"]:
                self.gui.control_panel.toggle_security_feature()
            elif selected_feature == "security":
                self.gui.control_panel.toggle_dct_security_watermark()