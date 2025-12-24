import tkinter as tk
from .theme import COLORS, FONTS


class MenuBar:
    """菜单栏组件"""
    
    def __init__(self, root, gui):
        self.root = root
        self.gui = gui
        self.create_menu_bar()
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = tk.Menu(self.root, bg=COLORS['background_light'], fg=COLORS['primary'], 
                          activebackground=COLORS['primary_light'], activeforeground=COLORS['background_light'])
        self.root.config(menu=menu_bar)
        
        # 文件菜单
        file_menu = tk.Menu(menu_bar, tearoff=0, 
                          bg=COLORS['background_light'], fg=COLORS['text_primary'],
                          activebackground=COLORS['primary_light'], activeforeground=COLORS['background_light'])
        menu_bar.add_cascade(label="文件(F)", menu=file_menu)
        file_menu.add_command(label="打开图片(O)... Ctrl+O", command=self.gui.load_image)
        file_menu.add_command(label="保存图片(S)... Ctrl+S", command=self.gui.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="批量处理(B)... Ctrl+B", command=self.gui.batch_process)
        file_menu.add_separator()
        file_menu.add_command(label="退出(X)", command=self.root.quit)
        
        # 添加快捷键绑定
        self.root.bind('<Control-o>', lambda event: self.gui.load_image())
        self.root.bind('<Control-O>', lambda event: self.gui.load_image())
        self.root.bind('<Control-s>', lambda event: self.gui.save_image())
        self.root.bind('<Control-S>', lambda event: self.gui.save_image())
        self.root.bind('<Control-b>', lambda event: self.gui.batch_process())
        self.root.bind('<Control-B>', lambda event: self.gui.batch_process())
        
        # 编辑菜单
        edit_menu = tk.Menu(menu_bar, tearoff=0,
                          bg=COLORS['background_light'], fg=COLORS['text_primary'],
                          activebackground=COLORS['primary_light'], activeforeground=COLORS['background_light'])
        menu_bar.add_cascade(label="编辑(E)", menu=edit_menu)
        edit_menu.add_separator()
        edit_menu.add_command(label="保存样式...", command=self.gui.save_style)
        edit_menu.add_command(label="加载样式...", command=self.gui.load_style)
        
        # 视图菜单
        view_menu = tk.Menu(menu_bar, tearoff=0,
                          bg=COLORS['background_light'], fg=COLORS['text_primary'],
                          activebackground=COLORS['primary_light'], activeforeground=COLORS['background_light'])
        menu_bar.add_cascade(label="视图(V)", menu=view_menu)
        view_menu.add_command(label="智能放置", command=self.gui.smart_watermark_position)
        view_menu.add_separator()
        view_menu.add_command(label="重置设置 Ctrl+R", command=self.reset_settings)
        
        # 工具菜单
        tools_menu = tk.Menu(menu_bar, tearoff=0,
                           bg=COLORS['background_light'], fg=COLORS['text_primary'],
                           activebackground=COLORS['primary_light'], activeforeground=COLORS['background_light'])
        menu_bar.add_cascade(label="工具(T)", menu=tools_menu)
        tools_menu.add_command(label="水印设置 F2", command=self.show_watermark_settings)
        tools_menu.add_command(label="批量处理向导 Ctrl+B", command=self.gui.batch_process)
        
        # 帮助菜单
        help_menu = tk.Menu(menu_bar, tearoff=0,
                          bg=COLORS['background_light'], fg=COLORS['text_primary'],
                          activebackground=COLORS['primary_light'], activeforeground=COLORS['background_light'])
        menu_bar.add_cascade(label="帮助(H)", menu=help_menu)
        help_menu.add_command(label="使用说明 F1", command=self.show_help)
        help_menu.add_separator()
        help_menu.add_command(label="关于", command=self.gui.show_about)
        
        # 添加快捷键绑定
        self.root.bind('<Control-o>', lambda event: self.gui.load_image())
        self.root.bind('<Control-O>', lambda event: self.gui.load_image())
        self.root.bind('<Control-s>', lambda event: self.gui.save_image())
        self.root.bind('<Control-S>', lambda event: self.gui.save_image())
        self.root.bind('<Control-b>', lambda event: self.gui.batch_process())
        self.root.bind('<Control-B>', lambda event: self.gui.batch_process())
        self.root.bind('<Control-r>', lambda event: self.reset_settings())
        self.root.bind('<Control-R>', lambda event: self.reset_settings())
        self.root.bind('<F1>', lambda event: self.show_help())
        self.root.bind('<F2>', lambda event: self.show_watermark_settings())
    
    def reset_settings(self):
        """重置设置"""
        from utils import DEFAULT_CONFIG
        import tkinter.messagebox as messagebox
        
        # 确认重置
        result = messagebox.askyesno("重置设置", "确定要重置所有设置到默认值吗？")
        if not result:
            return
        
        try:
            # 重置文字水印设置
            if hasattr(self.gui, 'text_entry') and self.gui.text_entry is not None:
                self.gui.text_entry.delete(0, tk.END)
                self.gui.text_entry.insert(0, DEFAULT_CONFIG["default_text"])
            
            # 重置颜色设置
            if hasattr(self.gui, 'font_color'):
                self.gui.font_color = DEFAULT_CONFIG["default_font_color"]
                if hasattr(self.gui, 'color_button'):
                    self.gui.color_button.config(bg=self.gui.font_color)
                if hasattr(self.gui, 'color_entry'):
                    self.gui.color_entry.delete(0, tk.END)
                    self.gui.color_entry.insert(0, self.gui.font_color)
            
            # 重置字体设置
            if hasattr(self.gui, 'font_family_var'):
                self.gui.font_family_var.set("黑体")
            if hasattr(self.gui, 'font_size_var'):
                self.gui.font_size_var.set(DEFAULT_CONFIG["default_font_size"])
            if hasattr(self.gui, 'bold_var'):
                self.gui.bold_var.set(False)
            if hasattr(self.gui, 'italic_var'):
                self.gui.italic_var.set(False)
            if hasattr(self.gui, 'underline_var'):
                self.gui.underline_var.set(False)
            
            # 重置位置设置
            if hasattr(self.gui, 'watermark_position'):
                self.gui.watermark_position = DEFAULT_CONFIG["default_position"]
            if hasattr(self.gui, 'position_var'):
                self.gui.position_var.set(DEFAULT_CONFIG["default_position"])
            
            # 重置透明度设置
            if hasattr(self.gui, 'opacity_var'):
                self.gui.opacity_var.set(DEFAULT_CONFIG["default_opacity"])
            
            # 重置旋转设置
            if hasattr(self.gui, 'rotation_var'):
                self.gui.rotation_var.set(DEFAULT_CONFIG["default_rotation"])
            
            # 重置翻转设置
            if hasattr(self.gui, 'flip_horizontal'):
                self.gui.flip_horizontal.set(False)
            if hasattr(self.gui, 'flip_vertical'):
                self.gui.flip_vertical.set(False)
            
            # 重置水印类型
            if hasattr(self.gui, 'watermark_type'):
                self.gui.watermark_type.set("text")
            
            # 重置水印功能
            if hasattr(self.gui, 'normal_watermark_var'):
                self.gui.normal_watermark_var.set(True)
            if hasattr(self.gui, 'scattered_watermark_var'):
                self.gui.scattered_watermark_var.set(False)
            if hasattr(self.gui, 'invisible_watermark_var'):
                self.gui.invisible_watermark_var.set(False)
            if hasattr(self.gui, 'texture_watermark_var'):
                self.gui.texture_watermark_var.set(False)
            if hasattr(self.gui, 'security_watermark_var'):
                self.gui.security_watermark_var.set(False)
            
            # 更新预览
            self.gui.update_preview()
            
            messagebox.showinfo("重置成功", "所有设置已重置为默认值")
            
        except Exception as e:
            messagebox.showerror("重置失败", f"重置设置时发生错误: {str(e)}")
    
    def show_watermark_settings(self):
        """显示水印设置"""
        import tkinter.messagebox as messagebox
        
        # 获取当前水印设置信息
        settings_info = "当前水印设置:\n\n"
        
        if hasattr(self.gui, 'watermark_type'):
            settings_info += f"水印类型: {self.gui.watermark_type.get()}\n"
        
        if hasattr(self.gui, 'watermark_position'):
            settings_info += f"水印位置: {self.gui.watermark_position}\n"
        
        if hasattr(self.gui, 'opacity_var'):
            settings_info += f"透明度: {self.gui.opacity_var.get()}%\n"
        
        if hasattr(self.gui, 'rotation_var'):
            settings_info += f"旋转角度: {self.gui.rotation_var.get()}°\n"
        
        if hasattr(self.gui, 'flip_horizontal') and self.gui.flip_horizontal.get():
            settings_info += "水平翻转: 是\n"
        else:
            settings_info += "水平翻转: 否\n"
            
        if hasattr(self.gui, 'flip_vertical') and self.gui.flip_vertical.get():
            settings_info += "垂直翻转: 是\n"
        else:
            settings_info += "垂直翻转: 否\n"
        
        # 水印功能状态
        settings_info += "\n水印功能状态:\n"
        if hasattr(self.gui, 'normal_watermark_var'):
            settings_info += f"普通水印: {'启用' if self.gui.normal_watermark_var.get() else '禁用'}\n"
        if hasattr(self.gui, 'scattered_watermark_var'):
            settings_info += f"分散水印: {'启用' if self.gui.scattered_watermark_var.get() else '禁用'}\n"
        if hasattr(self.gui, 'invisible_watermark_var'):
            settings_info += f"隐形水印: {'启用' if self.gui.invisible_watermark_var.get() else '禁用'}\n"
        if hasattr(self.gui, 'texture_watermark_var'):
            settings_info += f"纹理水印: {'启用' if self.gui.texture_watermark_var.get() else '禁用'}\n"
        if hasattr(self.gui, 'security_watermark_var'):
            settings_info += f"DCT安全水印: {'启用' if self.gui.security_watermark_var.get() else '禁用'}\n"
        
        messagebox.showinfo("水印设置", settings_info)
    
    def show_help(self):
        """显示使用说明"""
        import tkinter.messagebox as messagebox
        messagebox.showinfo("使用说明", 
                          "VisMark - 智能图像水印处理工具 使用说明\n\n"
                          "1. 打开图片：选择要添加水印的图片\n"
                          "2. 选择水印类型：文字水印或Logo水印\n"
                          "3. 设置水印参数：位置、透明度、旋转等\n"
                          "4. 实时预览效果\n"
                          "5. 保存处理后的图片\n\n"
                          "批量处理功能支持同时处理多张图片。")