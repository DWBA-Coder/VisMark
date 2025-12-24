import tkinter as tk


class LogoSettingsSection:
    """Logo水印设置部分"""
    
    def __init__(self, parent, gui):
        self.parent = parent
        self.gui = gui
        self.create_section()
    
    def _get_max_logo_size(self):
        """根据原图片尺寸计算最大Logo大小"""
        if not hasattr(self.gui, 'original_image') or self.gui.original_image is None:
            return 300  # 默认最大值
        
        # 获取原图片尺寸
        image_width, image_height = self.gui.original_image.size
        
        # 计算最大Logo尺寸（原图片较小尺寸的50%）
        max_size = int(min(image_width, image_height) * 0.8)
        
        # 确保最小值为50，最大值为1000
        return max(50, min(max_size, 1000))
    
    def _get_size_hint_text(self):
        """获取大小提示文本"""
        if not hasattr(self.gui, 'original_image') or self.gui.original_image is None:
            return "请先加载图片以获取智能大小限制"
        
        max_size = self._get_max_logo_size()
        image_width, image_height = self.gui.original_image.size
        return f"智能限制: 最大 {max_size}px (基于图片尺寸 {image_width}×{image_height})"
    
    def _update_logo_size_range(self):
        """更新Logo大小滑块的范围"""
        if hasattr(self, 'logo_size_slider'):
            max_size = self._get_max_logo_size()
            self.logo_size_slider.configure(to=max_size)
            
            # 如果当前值超过新范围，则调整为最大值
            current_value = self.gui.logo_size_var.get()
            if current_value > max_size:
                self.gui.logo_size_var.set(max_size)
            
            # 更新提示文本
            if hasattr(self, 'size_hint_label'):
                self.size_hint_label.configure(text=self._get_size_hint_text())
    
    def create_section(self):
        """创建Logo水印设置部分"""
        # 创建主框架
        self.main_frame = tk.Frame(self.parent, bg="#f5f5f5")
        # 默认隐藏，由toggle_watermark_type方法控制显示/隐藏
        self.main_frame.pack_forget()
        
        # 初始化变量（如果不存在）
        if not hasattr(self.gui, 'logo_path_var'):
            self.gui.logo_path_var = tk.StringVar(value="未选择Logo")
        if not hasattr(self.gui, 'logo_size_var'):
            self.gui.logo_size_var = tk.IntVar(value=100)
        if not hasattr(self.gui, 'logo_recolor_var'):
            self.gui.logo_recolor_var = tk.StringVar(value="")  # 重着色颜色
        
        # 图片水印选择
        tk.Label(self.main_frame, text="图片水印", bg="#f5f5f5", font=("黑体", 10, "bold")).pack(anchor="w", pady=(8, 4))
        logo_button = tk.Button(self.main_frame, text="选择图片", command=self.gui.load_logo, width=20)
        logo_button.pack(pady=(0, 8))
        
        tk.Label(self.main_frame, textvariable=self.gui.logo_path_var, bg="#f5f5f5", 
                wraplength=250).pack(pady=(0, 8))
        
        # 大小
        tk.Label(self.main_frame, text="大小", bg="#f5f5f5", font=("黑体", 10, "bold")).pack(anchor="w", pady=(8, 4))
        
        # 创建Logo大小滑块，根据原图片尺寸动态调整范围
        self.logo_size_slider = tk.Scale(self.main_frame, 
                                        from_=10, 
                                        to=self._get_max_logo_size(), 
                                        variable=self.gui.logo_size_var, 
                                        orient="horizontal", 
                                        bg="#f5f5f5", 
                                        command=lambda x: self.gui.update_preview())
        self.logo_size_slider.pack(fill=tk.X, pady=(0, 4))
        
        # 大小提示标签
        self.size_hint_label = tk.Label(self.main_frame, 
                                       text=self._get_size_hint_text(), 
                                       bg="#f5f5f5", 
                                       fg="#666666",
                                       font=("黑体", 7))
        self.size_hint_label.pack(anchor="w", pady=(0, 8))
        
        # Logo重着色
        recolor_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        recolor_frame.pack(fill=tk.X, pady=(8, 0))
        
        tk.Label(recolor_frame, text="重着色", bg="#f5f5f5", font=("黑体", 10, "bold")).pack(anchor="w", pady=(8, 4))
        
        recolor_control_frame = tk.Frame(recolor_frame, bg="#f5f5f5")
        recolor_control_frame.pack(fill=tk.X)
        
        # 颜色选择按钮
        self.recolor_button = tk.Button(recolor_control_frame, 
                                       text="选择颜色", 
                                       command=self._choose_recolor_color,
                                       width=8)
        self.recolor_button.pack(side=tk.LEFT, padx=(0, 8))
        
        # 颜色预览
        self.recolor_preview = tk.Label(recolor_control_frame, 
                                       text="", 
                                       bg="white", 
                                       width=3,
                                       relief="solid",
                                       bd=1)
        self.recolor_preview.pack(side=tk.LEFT, padx=(0, 8))
        
        # 清除颜色按钮
        clear_button = tk.Button(recolor_control_frame, 
                                text="清除", 
                                command=self._clear_recolor_color,
                                width=8)
        clear_button.pack(side=tk.LEFT)
        
        # 提示文字
        tk.Label(recolor_frame, 
                text="选择颜色后，Logo将重新着色为该颜色", 
                bg="#f5f5f5", 
                fg="#666666",
                font=("黑体", 7)).pack(anchor="w", pady=(4, 0))
        
        # 保存组件引用用于状态管理
        self.main_frame_widget = self.main_frame
        
        # 初始状态
        self.update_control_states(False, False)
    
    def update_control_states(self, image_loaded, logo_selected):
        """根据当前状态更新控件启用/禁用状态"""
        # Logo水印设置始终启用，不依赖图片加载状态
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
    
    def _choose_recolor_color(self):
        """选择重着色颜色"""
        color = tk.colorchooser.askcolor(title="选择Logo重着色颜色", 
                                        initialcolor=self.gui.logo_recolor_var.get() or "#FFFFFF")
        if color[1]:  # 用户选择了颜色
            self.gui.logo_recolor_var.set(color[1])
            self.recolor_preview.configure(bg=color[1])
            self.gui.update_preview()
    
    def _clear_recolor_color(self):
        """清除重着色颜色"""
        self.gui.logo_recolor_var.set("")
        self.recolor_preview.configure(bg="white")
        self.gui.update_preview()