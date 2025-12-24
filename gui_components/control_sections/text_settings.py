import tkinter as tk
from tkinter import ttk
from utils import DEFAULT_CONFIG


class TextSettingsSection:
    """文字水印设置部分"""
    
    def __init__(self, parent, gui):
        self.parent = parent
        self.gui = gui
        self.create_section()
    
    def create_section(self):
        """创建文字水印设置部分"""
        # 创建主框架
        self.main_frame = tk.Frame(self.parent, bg="#f5f5f5")
        self.main_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 初始化变量（如果不存在）
        if not hasattr(self.gui, 'text_entry'):
            self.gui.text_entry = tk.Entry(self.main_frame, width=30)
        if not hasattr(self.gui, 'font_color'):
            self.gui.font_color = DEFAULT_CONFIG["default_font_color"]
        if not hasattr(self.gui, 'rgb_red_var'):
            self.gui.rgb_red_var = tk.IntVar(value=0)
        if not hasattr(self.gui, 'rgb_green_var'):
            self.gui.rgb_green_var = tk.IntVar(value=0)
        if not hasattr(self.gui, 'rgb_blue_var'):
            self.gui.rgb_blue_var = tk.IntVar(value=0)
        if not hasattr(self.gui, 'font_family_var'):
            self.gui.font_family_var = tk.StringVar(value="黑体")
        if not hasattr(self.gui, 'font_size_var'):
            self.gui.font_size_var = tk.IntVar(value=DEFAULT_CONFIG["default_font_size"])
        if not hasattr(self.gui, 'bold_var'):
            self.gui.bold_var = tk.BooleanVar(value=False)
        if not hasattr(self.gui, 'italic_var'):
            self.gui.italic_var = tk.BooleanVar(value=False)
        if not hasattr(self.gui, 'underline_var'):
            self.gui.underline_var = tk.BooleanVar(value=False)
        if not hasattr(self.gui, 'shadow_enable_var'):
            self.gui.shadow_enable_var = tk.BooleanVar(value=False)
        if not hasattr(self.gui, 'shadow_color'):
            self.gui.shadow_color = "#000000"
        if not hasattr(self.gui, 'shadow_offset_x_var'):
            self.gui.shadow_offset_x_var = tk.IntVar(value=2)
        if not hasattr(self.gui, 'shadow_offset_y_var'):
            self.gui.shadow_offset_y_var = tk.IntVar(value=2)
        if not hasattr(self.gui, 'shadow_opacity_var'):
            self.gui.shadow_opacity_var = tk.IntVar(value=30)
        
        # 水印文字
        tk.Label(self.main_frame, text="水印文字", bg="#f5f5f5", font=("黑体", 10, "bold")).pack(anchor="w", pady=(8, 4))
        
        # 创建text_entry组件（如果不存在）
        if not hasattr(self.gui, 'text_entry') or self.gui.text_entry is None:
            self.gui.text_entry = tk.Entry(self.main_frame, width=30)
        
        self.gui.text_entry.pack(fill=tk.X, pady=(0, 8))
        self.gui.text_entry.delete(0, tk.END)
        self.gui.text_entry.insert(0, DEFAULT_CONFIG["default_text"])
        self.gui.text_entry.bind("<KeyRelease>", lambda e: self.gui.update_preview())
        
        # 颜色
        tk.Label(self.main_frame, text="颜色", bg="#f5f5f5", font=("黑体", 10, "bold")).pack(anchor="w", pady=(8, 4))
        color_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        color_frame.pack(fill=tk.X, pady=(0, 8))
        
        # 颜色选择控制框架
        color_control_frame = tk.Frame(color_frame, bg="#f5f5f5")
        color_control_frame.pack(fill=tk.X)
        
        # 颜色选择按钮（不带颜色，保持统一风格）
        if not hasattr(self.gui, 'color_button') or self.gui.color_button is None:
            self.gui.color_button = tk.Button(color_control_frame, 
                                           text="选择颜色", 
                                           command=self._choose_color,
                                           width=8,
                                           bg="#e0e0e0",
                                           fg="black",
                                           activebackground="#d0d0d0",
                                           activeforeground="black")
        self.gui.color_button.pack(side=tk.LEFT, padx=(0, 8))
        
        # 颜色预览
        self.color_preview = tk.Label(color_control_frame, 
                                     text="", 
                                     bg=self.gui.font_color, 
                                     width=3,
                                     relief="solid",
                                     bd=1)
        self.color_preview.pack(side=tk.LEFT, padx=(0, 8))
        
        # 清除颜色按钮
        clear_button = tk.Button(color_control_frame, 
                                text="清除", 
                                command=self._clear_color,
                                width=8)
        clear_button.pack(side=tk.LEFT)
        
        # 颜色值输入框
        if not hasattr(self.gui, 'color_entry') or self.gui.color_entry is None:
            self.gui.color_entry = tk.Entry(color_frame, width=15)
        self.gui.color_entry.pack(fill=tk.X, pady=(8, 0))
        self.gui.color_entry.delete(0, tk.END)
        self.gui.color_entry.insert(0, self.gui.font_color)
        self.gui.color_entry.bind("<KeyRelease>", self._update_color_from_entry)
        
        # RGB值设置
        rgb_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        rgb_frame.pack(fill=tk.X, pady=(8, 0))
        
        # 设置初始RGB值
        self._update_rgb_from_hex(self.gui.font_color)
        
        # R滑块
        r_frame = tk.Frame(rgb_frame, bg="#f5f5f5")
        r_frame.pack(fill=tk.X, pady=2)
        tk.Label(r_frame, text="R:", bg="#f5f5f5", width=3).pack(side="left")
        r_slider = tk.Scale(r_frame, from_=0, to=255, variable=self.gui.rgb_red_var, 
                           orient="horizontal", bg="#f5f5f5", showvalue=True, 
                           command=lambda x: self._update_color_from_rgb())
        r_slider.pack(side="left", fill=tk.X, expand=True)
        
        # G滑块
        g_frame = tk.Frame(rgb_frame, bg="#f5f5f5")
        g_frame.pack(fill=tk.X, pady=2)
        tk.Label(g_frame, text="G:", bg="#f5f5f5", width=3).pack(side="left")
        g_slider = tk.Scale(g_frame, from_=0, to=255, variable=self.gui.rgb_green_var, 
                           orient="horizontal", bg="#f5f5f5", showvalue=True,
                           command=lambda x: self._update_color_from_rgb())
        g_slider.pack(side="left", fill=tk.X, expand=True)
        
        # B滑块
        b_frame = tk.Frame(rgb_frame, bg="#f5f5f5")
        b_frame.pack(fill=tk.X, pady=2)
        tk.Label(b_frame, text="B:", bg="#f5f5f5", width=3).pack(side="left")
        b_slider = tk.Scale(b_frame, from_=0, to=255, variable=self.gui.rgb_blue_var, 
                           orient="horizontal", bg="#f5f5f5", showvalue=True,
                           command=lambda x: self._update_color_from_rgb())
        b_slider.pack(side="left", fill=tk.X, expand=True)
        
        # 字体选择
        tk.Label(self.main_frame, text="字体", bg="#f5f5f5", font=("黑体", 10, "bold")).pack(anchor="w", pady=(8, 4))
        font_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        font_frame.pack(fill=tk.X, pady=(0, 8))
        
        # 动态获取系统可用字体
        available_fonts = self._get_available_fonts()
        
        # 添加中文字体选项
        if not hasattr(self.gui, 'font_combobox') or self.gui.font_combobox is None:
            self.gui.font_combobox = ttk.Combobox(font_frame, textvariable=self.gui.font_family_var, 
                                         values=available_fonts)
        self.gui.font_combobox.pack(fill=tk.X)
        self.gui.font_combobox.bind("<<ComboboxSelected>>", lambda e: self.gui.update_preview())
        # 禁用鼠标滚轮操作
        self.gui.font_combobox.bind("<MouseWheel>", lambda e: "break")
        
        # 字体大小
        tk.Label(self.main_frame, text="大小", bg="#f5f5f5", font=("黑体", 10, "bold")).pack(anchor="w", pady=(8, 4))
        font_size_slider = tk.Scale(self.main_frame, from_=8, to=300, variable=self.gui.font_size_var, 
                                   orient="horizontal", bg="#f5f5f5", command=lambda x: self.gui.update_preview())
        font_size_slider.pack(fill=tk.X, pady=(0, 8))
        
        # 字体样式 - 改为按钮形式
        tk.Label(self.main_frame, text="样式", bg="#f5f5f5", font=("黑体", 10, "bold")).pack(anchor="w", pady=(8, 4))
        style_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        style_frame.pack(fill=tk.X, pady=(0, 8))
        
        # 加粗按钮
        self.bold_button = tk.Button(style_frame, 
                                   text="加粗", 
                                   width=6,
                                   bg="#e0e0e0",
                                   fg="black",
                                   activebackground="#d0d0d0",
                                   activeforeground="black",
                                   command=self._toggle_bold)
        self.bold_button.pack(side="left", padx=8)
        
        # 斜体按钮
        self.italic_button = tk.Button(style_frame, 
                                     text="斜体", 
                                     width=6,
                                     bg="#e0e0e0",
                                     fg="black",
                                     activebackground="#d0d0d0",
                                     activeforeground="black",
                                     command=self._toggle_italic)
        self.italic_button.pack(side="left", padx=8)
        
        # 下划线按钮
        self.underline_button = tk.Button(style_frame, 
                                        text="下划线", 
                                        width=8,
                                        bg="#e0e0e0",
                                        fg="black",
                                        activebackground="#d0d0d0",
                                        activeforeground="black",
                                        command=self._toggle_underline)
        self.underline_button.pack(side="left", padx=8)
        
        # 文字阴影效果
        tk.Label(self.main_frame, text="阴影", bg="#f5f5f5", font=("黑体", 10, "bold")).pack(anchor="w", pady=(12, 6))
        
        # 启用阴影按钮
        shadow_enable_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        shadow_enable_frame.pack(fill=tk.X, pady=(0, 8))
        
        self.shadow_button = tk.Button(shadow_enable_frame, 
                                     text="启用阴影", 
                                     width=8,
                                     bg="#e0e0e0",
                                     fg="black",
                                     activebackground="#d0d0d0",
                                     activeforeground="black",
                                     command=self._toggle_shadow)
        self.shadow_button.pack(side="left", padx=8)
        
        # 阴影设置框架
        self.shadow_settings_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        
        # 阴影颜色
        tk.Label(self.shadow_settings_frame, text="颜色", bg="#f5f5f5").pack(anchor="w", pady=(8, 4), padx=20)
        shadow_color_frame = tk.Frame(self.shadow_settings_frame, bg="#f5f5f5")
        shadow_color_frame.pack(fill=tk.X, pady=(0, 8), padx=20)
        
        if not hasattr(self.gui, 'shadow_color_button') or self.gui.shadow_color_button is None:
            self.gui.shadow_color_button = tk.Button(shadow_color_frame, bg=self.gui.shadow_color, width=5, command=self.gui.choose_shadow_color)
        self.gui.shadow_color_button.pack(side="left", padx=8)
        
        if not hasattr(self.gui, 'shadow_color_entry') or self.gui.shadow_color_entry is None:
            self.gui.shadow_color_entry = tk.Entry(shadow_color_frame, width=15)
        self.gui.shadow_color_entry.pack(side="left", fill=tk.X, expand=True, padx=8)
        self.gui.shadow_color_entry.delete(0, tk.END)
        self.gui.shadow_color_entry.insert(0, self.gui.shadow_color)
        self.gui.shadow_color_entry.bind("<KeyRelease>", self.gui.update_shadow_color)
        
        # 阴影水平偏移
        tk.Label(self.shadow_settings_frame, text="水平偏移", bg="#f5f5f5").pack(anchor="w", pady=(8, 4), padx=20)
        shadow_offset_x_slider = tk.Scale(self.shadow_settings_frame, from_=-10, to=10, variable=self.gui.shadow_offset_x_var,
                                         orient="horizontal", bg="#f5f5f5", command=lambda x: self.gui.update_preview(),
                                         length=180)
        shadow_offset_x_slider.pack(fill=tk.X, pady=(0, 8), padx=20)
        
        # 阴影垂直偏移
        tk.Label(self.shadow_settings_frame, text="垂直偏移", bg="#f5f5f5").pack(anchor="w", pady=(8, 4), padx=20)
        shadow_offset_y_slider = tk.Scale(self.shadow_settings_frame, from_=-10, to=10, variable=self.gui.shadow_offset_y_var,
                                         orient="horizontal", bg="#f5f5f5", command=lambda x: self.gui.update_preview(),
                                         length=180)
        shadow_offset_y_slider.pack(fill=tk.X, pady=(0, 8), padx=20)
        
        # 阴影透明度
        tk.Label(self.shadow_settings_frame, text="透明度", bg="#f5f5f5").pack(anchor="w", pady=(8, 4), padx=20)
        shadow_opacity_slider = tk.Scale(self.shadow_settings_frame, from_=0, to=100, variable=self.gui.shadow_opacity_var,
                                        orient="horizontal", bg="#f5f5f5", command=lambda x: self.gui.update_preview(),
                                        length=180)
        shadow_opacity_slider.pack(fill=tk.X, pady=(0, 8), padx=20)
        
        # 默认隐藏阴影设置
        self.shadow_settings_frame.pack_forget()
        
        # 保存组件引用用于状态管理
        self.main_frame_widget = self.main_frame
        
        # 初始状态
        self.update_control_states(False, False)
        
        # 更新按钮初始状态
        self._update_style_button_states()
    
    def update_control_states(self, image_loaded, logo_selected):
        """根据当前状态更新控件启用/禁用状态"""
        # 文字水印设置始终启用，不依赖图片加载状态
        state = tk.NORMAL
        
        # 更新所有控件状态
        if hasattr(self, 'main_frame_widget'):
            self._update_widget_state(self.main_frame_widget, state)
    
    def _update_widget_state(self, widget, state):
        """递归更新控件状态"""
        try:
            # 更新当前控件状态（如果控件支持state属性）
            if hasattr(widget, 'config') and 'state' in widget.config():
                widget.config(state=state)
            
            # 递归更新子控件
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    self._update_widget_state(child, state)
        except:
            # 忽略可能的异常
            pass
        if hasattr(self, 'font_combobox_widget'):
            self.font_combobox_widget.config(state=state)
        if hasattr(self, 'font_size_slider_widget'):
            self.font_size_slider_widget.config(state=state)
        if hasattr(self, 'style_frame_widget'):
            for widget in self.style_frame_widget.winfo_children():
                widget.config(state=state)
        if hasattr(self, 'shadow_enable_frame_widget'):
            for widget in self.shadow_enable_frame_widget.winfo_children():
                widget.config(state=state)
        if hasattr(self, 'shadow_settings_frame_widget'):
            for widget in self.shadow_settings_frame_widget.winfo_children():
                widget.config(state=state)
    
    def _choose_color(self):
        """选择文字颜色"""
        color = tk.colorchooser.askcolor(title="选择文字颜色", 
                                        initialcolor=self.gui.font_color)
        if color[1]:  # 用户选择了颜色
            self.gui.font_color = color[1]
            self.color_preview.configure(bg=color[1])
            
            # 更新颜色输入框
            if hasattr(self.gui, 'color_entry'):
                self.gui.color_entry.delete(0, tk.END)
                self.gui.color_entry.insert(0, color[1])
            
            # 更新RGB值
            self._update_rgb_from_hex(color[1])
            
            # 更新预览
            self.gui.update_preview()
    
    def _clear_color(self):
        """清除颜色，恢复默认"""
        default_color = DEFAULT_CONFIG["default_font_color"]
        self.gui.font_color = default_color
        self.color_preview.configure(bg=default_color)
        
        # 更新颜色输入框
        if hasattr(self.gui, 'color_entry'):
            self.gui.color_entry.delete(0, tk.END)
            self.gui.color_entry.insert(0, default_color)
        
        # 更新RGB值
        self._update_rgb_from_hex(default_color)
        
        # 更新预览
        self.gui.update_preview()
    
    def _update_color_from_entry(self, event=None):
        """从输入框更新颜色"""
        color_text = self.gui.color_entry.get()
        
        # 验证颜色格式
        if color_text.startswith('#') and len(color_text) in [4, 7, 9]:
            # 简化格式转换（如 #RGB 转 #RRGGBB）
            if len(color_text) == 4:  # #RGB
                color_text = f"#{color_text[1]}{color_text[1]}{color_text[2]}{color_text[2]}{color_text[3]}{color_text[3]}"
            
            self.gui.font_color = color_text
            # 只更新颜色预览，不改变按钮背景色
            self.color_preview.configure(bg=color_text)
            
            # 更新RGB值
            self._update_rgb_from_hex(color_text)
            
            # 更新预览
            self.gui.update_preview()
    
    def _update_rgb_from_hex(self, hex_color):
        """从十六进制颜色更新RGB值"""
        try:
            # 移除#号并转换为RGB
            hex_color = hex_color.lstrip('#')
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                
                # 更新RGB变量
                if hasattr(self.gui, 'rgb_red_var'):
                    self.gui.rgb_red_var.set(r)
                if hasattr(self.gui, 'rgb_green_var'):
                    self.gui.rgb_green_var.set(g)
                if hasattr(self.gui, 'rgb_blue_var'):
                    self.gui.rgb_blue_var.set(b)
        except (ValueError, IndexError):
            # 如果颜色格式无效，使用默认值
            if hasattr(self.gui, 'rgb_red_var'):
                self.gui.rgb_red_var.set(0)
            if hasattr(self.gui, 'rgb_green_var'):
                self.gui.rgb_green_var.set(0)
            if hasattr(self.gui, 'rgb_blue_var'):
                self.gui.rgb_blue_var.set(0)
    
    def _update_color_from_rgb(self):
        """从RGB值更新颜色"""
        if not (hasattr(self.gui, 'rgb_red_var') and hasattr(self.gui, 'rgb_green_var') and hasattr(self.gui, 'rgb_blue_var')):
            return
        
        # 获取RGB值
        r = self.gui.rgb_red_var.get()
        g = self.gui.rgb_green_var.get()
        b = self.gui.rgb_blue_var.get()
        
        # 转换为十六进制
        hex_color = f"#{r:02x}{g:02x}{b:02x}".upper()
        
        # 更新颜色
        self.gui.font_color = hex_color
        
        # 更新UI组件
        if hasattr(self.gui, 'color_entry'):
            # 避免循环更新
            current_text = self.gui.color_entry.get()
            if current_text != hex_color:
                self.gui.color_entry.delete(0, tk.END)
                self.gui.color_entry.insert(0, hex_color)
        
        # 更新颜色预览
        if hasattr(self, 'color_preview'):
            self.color_preview.configure(bg=hex_color)
        
        # 更新预览
        self.gui.update_preview()
    
    def _get_available_fonts(self):
        """获取系统可用字体列表"""
        import tkinter.font
        
        # 获取系统所有字体
        all_fonts = list(tkinter.font.families())
        
        # 优先显示常用中文字体
        preferred_fonts = ["黑体", "宋体", "楷体", "仿宋", "微软雅黑", "Arial", "Times New Roman"]
        
        # 过滤出实际存在的字体
        available_fonts = []
        
        # 先添加常用字体
        for font in preferred_fonts:
            if font in all_fonts:
                available_fonts.append(font)
        
        # 添加其他中英文字体
        for font in all_fonts:
            # 跳过已添加的字体
            if font in available_fonts:
                continue
            
            # 添加中文字体和常见英文字体
            if (font.startswith('@') or  # 跳过垂直字体
                font.lower() in ['system', 'fixedsys', 'terminal', 'modern', 'roman', 'script', 'courier'] or
                len(font) > 30):  # 跳过过长的字体名
                continue
            
            # 检查是否是中文字体（包含中文字符或常见中文字体名）
            chinese_keywords = ['黑体', '宋体', '楷体', '仿宋', '雅黑', '细黑', '圆体', '隶书', '幼圆']
            is_chinese_font = any(keyword in font for keyword in chinese_keywords)
            
            # 检查是否是常见英文字体
            english_fonts = ['Arial', 'Times', 'Helvetica', 'Verdana', 'Georgia', 'Tahoma', 'Courier', 'Impact']
            is_english_font = any(eng_font in font for eng_font in english_fonts)
            
            if is_chinese_font or is_english_font:
                available_fonts.append(font)
        
        # 按字母顺序排序
        available_fonts.sort()
        
        # 确保黑体在首位（作为默认字体）
        if "黑体" in available_fonts:
            available_fonts.remove("黑体")
            available_fonts.insert(0, "黑体")
        
        return available_fonts
    
    def _toggle_bold(self):
        """切换加粗状态"""
        self.gui.bold_var.set(not self.gui.bold_var.get())
        self._update_style_button_states()
        self.gui.update_preview()
    
    def _toggle_italic(self):
        """切换斜体状态"""
        self.gui.italic_var.set(not self.gui.italic_var.get())
        self._update_style_button_states()
        self.gui.update_preview()
    
    def _toggle_underline(self):
        """切换下划线状态"""
        self.gui.underline_var.set(not self.gui.underline_var.get())
        self._update_style_button_states()
        self.gui.update_preview()
    
    def _toggle_shadow(self):
        """切换阴影状态"""
        self.gui.shadow_enable_var.set(not self.gui.shadow_enable_var.get())
        self._update_style_button_states()
        
        # 显示或隐藏阴影设置
        if self.gui.shadow_enable_var.get():
            self.shadow_settings_frame.pack(fill=tk.X, pady=(0, 8))
        else:
            self.shadow_settings_frame.pack_forget()
        
        self.gui.update_preview()
    
    def _update_style_button_states(self):
        """更新样式按钮状态显示"""
        # 加粗按钮状态
        if self.gui.bold_var.get():
            self.bold_button.config(bg="#005FA5", fg="white")
        else:
            self.bold_button.config(bg="#e0e0e0", fg="black")
        
        # 斜体按钮状态
        if self.gui.italic_var.get():
            self.italic_button.config(bg="#005FA5", fg="white")
        else:
            self.italic_button.config(bg="#e0e0e0", fg="black")
        
        # 下划线按钮状态
        if self.gui.underline_var.get():
            self.underline_button.config(bg="#005FA5", fg="white")
        else:
            self.underline_button.config(bg="#e0e0e0", fg="black")
        
        # 阴影按钮状态
        if self.gui.shadow_enable_var.get():
            self.shadow_button.config(bg="#005FA5", fg="white")
        else:
            self.shadow_button.config(bg="#e0e0e0", fg="black")