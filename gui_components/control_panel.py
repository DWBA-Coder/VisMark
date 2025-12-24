import tkinter as tk
from tkinter import ttk, colorchooser
from utils import DEFAULT_CONFIG, validate_color

from .control_sections.watermark_type import WatermarkTypeSection
from .control_sections.watermark_feature import WatermarkFeatureSection
from .control_sections.operation_scope import OperationScopeSection
from .control_sections.text_settings import TextSettingsSection
from .control_sections.logo_settings import LogoSettingsSection
from .control_sections.position import PositionSection
from .control_sections.opacity import OpacitySection
from .control_sections.rotation import RotationSection
from .control_sections.flip import FlipSection
from .control_sections.smart_placement import SmartPlacementSection
from gui_components.theme import COLORS, FONTS, SPACING, create_section_title


class ControlPanel:
    """控制面板组件"""
    
    def __init__(self, parent, gui):
        self.parent = parent
        self.gui = gui
        self.create_control_panel()
    
    def create_control_panel(self):
        """创建左侧控制面板"""
        # 创建控制面板容器
        control_container = tk.Frame(self.parent, bg=COLORS['background'])
        control_container.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING['medium']))
        
        # 创建滚动条和Canvas
        scrollbar = ttk.Scrollbar(control_container, orient="vertical", style='Modern.Vertical.TScrollbar')
        scrollbar.pack(side="right", fill="y")
        
        canvas = tk.Canvas(control_container, yscrollcommand=scrollbar.set, bg=COLORS['background'], highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar.config(command=canvas.yview)
        
        # 创建控制面板内容
        self.control_content = tk.Frame(canvas, bg=COLORS['background'], relief=tk.FLAT, bd=0)
        
        # 将控制面板添加到Canvas
        canvas_window = canvas.create_window((0, 0), window=self.control_content, anchor="nw", width=340)
        
        # 确保Canvas窗口宽度与Canvas一致，并设置最小宽度
        def on_canvas_configure(event):
            # 设置最小宽度为300px，最大宽度为400px
            width = max(300, min(event.width, 400))
            canvas.itemconfig(canvas_window, width=width)
        
        canvas.bind("<Configure>", on_canvas_configure)
        
        # 绑定鼠标滚轮事件
        def on_mousewheel(event):
            # 检查事件源是否为Combobox，如果是则忽略
            if hasattr(event.widget, 'widgetName') and event.widget.widgetName == 'ttk::combobox':
                return "break"
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # 绑定到root窗口，这样菜单栏也能响应鼠标滚轮
        self.gui.root.bind("<MouseWheel>", on_mousewheel)
        # 同时保持对canvas的绑定
        canvas.bind("<MouseWheel>", on_mousewheel)
        
        # 当控制面板内容变化时更新Canvas滚动区域
        def update_scrollregion(event):
            # 添加一些边距，确保滚动区域正确
            bbox = canvas.bbox("all")
            if bbox:
                canvas.configure(scrollregion=(0, 0, bbox[2], bbox[3] + 20))
        
        self.control_content.bind("<Configure>", update_scrollregion)
        
        # 添加控制面板内容
        self.sections = {}
        
        # 添加标题
        title_frame = create_section_title(self.control_content, "水印设置", COLORS['primary'])
        title_frame.pack(fill="x", pady=(0, SPACING['medium']))
        
        self.sections['watermark_type'] = WatermarkTypeSection(self.control_content, self.gui)
        self.sections['watermark_feature'] = WatermarkFeatureSection(self.control_content, self.gui)
        self.sections['operation_scope'] = OperationScopeSection(self.control_content, self.gui)
        self.sections['text_settings'] = TextSettingsSection(self.control_content, self.gui)
        self.sections['logo_settings'] = LogoSettingsSection(self.control_content, self.gui)
        
        # 添加样式设置标题
        style_title_frame = create_section_title(self.control_content, "样式设置", COLORS['primary'])
        style_title_frame.pack(fill="x", pady=(SPACING['large'], SPACING['medium']))
        
        self.sections['position'] = PositionSection(self.control_content, self.gui)
        self.sections['opacity'] = OpacitySection(self.control_content, self.gui)
        self.sections['rotation'] = RotationSection(self.control_content, self.gui)
        self.sections['flip'] = FlipSection(self.control_content, self.gui)
        self.sections['smart_placement'] = SmartPlacementSection(self.control_content, self.gui)
        
        # 手动更新滚动区域
        canvas.after(100, lambda: canvas.configure(scrollregion=canvas.bbox("all")))
    
    def update_control_states(self, image_loaded, logo_selected):
        """根据当前状态更新控制面板组件的启用/禁用状态"""
        # 所有设置部分都始终启用，不依赖图片加载状态
        for section_name, section in self.sections.items():
            if hasattr(section, 'update_control_states'):
                section.update_control_states(True, logo_selected)  # 强制image_loaded为True
    
    def toggle_watermark_type(self):
        """切换水印类型（文字/Logo）"""
        if hasattr(self.gui, 'watermark_type') and self.gui.watermark_type.get() == "text":
            # 显示文字水印设置部分，隐藏Logo设置部分
            if 'text_settings' in self.sections:
                self.sections['text_settings'].main_frame.pack(fill=tk.X, padx=10, pady=5)
            if 'logo_settings' in self.sections:
                self.sections['logo_settings'].main_frame.pack_forget()
        elif hasattr(self.gui, 'watermark_type') and self.gui.watermark_type.get() == "logo":
            # 显示Logo设置部分，隐藏文字水印设置部分
            if 'logo_settings' in self.sections:
                self.sections['logo_settings'].main_frame.pack(fill=tk.X, padx=10, pady=5)
            if 'text_settings' in self.sections:
                self.sections['text_settings'].main_frame.pack_forget()
        
        self.gui.update_preview()
    
    def choose_color(self):
        """选择颜色（向后兼容方法）"""
        # 这个方法现在由TextSettingsSection组件处理
        # 保持向后兼容性，但实际功能在组件中实现
        pass
    
    def update_color(self, event):
        """更新颜色"""
        color = self.color_entry.get()
        if validate_color(color):
            self.font_color = color
            self.color_button.config(bg=self.font_color)
            self.gui.update_preview()
    
    def set_position(self, position):
        """设置水印位置"""
        # 直接调用GUI主类的set_position方法
        self.gui.set_position(position)
    
    def validate_opacity_input(self, new_value):
        """验证透明度输入"""
        if new_value == "":
            return True
        try:
            value = int(new_value)
            return 0 <= value <= 100
        except ValueError:
            return False
            
    def set_opacity_from_entry(self, event=None):
        """从输入框设置透明度"""
        try:
            value = int(self.opacity_entry.get())
            if 0 <= value <= 100:
                self.opacity_var.set(value)
                self.gui.update_preview()
            else:
                self.opacity_entry.delete(0, tk.END)
                self.opacity_entry.insert(0, str(self.opacity_var.get()))
        except ValueError:
            self.opacity_entry.delete(0, tk.END)
            self.opacity_entry.insert(0, str(self.opacity_var.get()))
            
    def reset_opacity(self):
        """重置透明度"""
        self.opacity_var.set(DEFAULT_CONFIG["default_opacity"])
        self.opacity_entry.delete(0, tk.END)
        self.opacity_entry.insert(0, str(self.opacity_var.get()))
        self.gui.update_preview()
        
    def validate_rotation_input(self, new_value):
        """验证旋转角度输入"""
        if new_value == "":
            return True
        try:
            value = int(new_value)
            return -180 <= value <= 180
        except ValueError:
            return False
            
    def set_rotation_from_entry(self, event=None):
        """从输入框设置旋转角度"""
        try:
            value = int(self.rotation_entry.get())
            if -180 <= value <= 180:
                self.rotation_var.set(value)
                self.gui.update_preview()
            else:
                self.rotation_entry.delete(0, tk.END)
                self.rotation_entry.insert(0, str(self.rotation_var.get()))
        except ValueError:
            self.rotation_entry.delete(0, tk.END)
            self.rotation_entry.insert(0, str(self.rotation_var.get()))
            
    def reset_rotation(self):
        """重置旋转角度"""
        self.rotation_var.set(DEFAULT_CONFIG["default_rotation"])
        self.rotation_entry.delete(0, tk.END)
        self.rotation_entry.insert(0, str(self.rotation_var.get()))
        self.gui.update_preview()
    
    def toggle_shadow_settings(self):
        """切换阴影设置的显示/隐藏"""
        if self.shadow_enable_var.get():
            self.shadow_settings_frame.pack(fill=tk.X, pady=2)
        else:
            self.shadow_settings_frame.pack_forget()
        self.gui.update_preview()

    def choose_shadow_color(self):
        """选择阴影颜色"""
        color = colorchooser.askcolor(color=self.shadow_color, title="选择阴影颜色")[1]
        if color:
            self.shadow_color = color
            self.shadow_color_button.config(bg=color)
            self.shadow_color_entry.delete(0, tk.END)
            self.shadow_color_entry.insert(0, color)
            self.gui.update_preview()

    def update_shadow_color(self, event=None):
        """更新阴影颜色"""
        color = self.shadow_color_entry.get()
        if validate_color(color):
            self.shadow_color = color
            self.shadow_color_button.config(bg=color)
            self.gui.update_preview()

    def toggle_normal_watermark(self):
        """切换普通水印时的回调函数"""
        if hasattr(self.gui, 'normal_watermark_var') and self.gui.normal_watermark_var.get():
            # 如果选择了普通水印，自动取消所有其他水印的勾选
            if hasattr(self.gui, 'scattered_watermark_var'):
                self.gui.scattered_watermark_var.set(False)
            if hasattr(self.gui, 'invisible_watermark_var'):
                self.gui.invisible_watermark_var.set(False)
            if hasattr(self.gui, 'texture_watermark_var'):
                self.gui.texture_watermark_var.set(False)
            if hasattr(self.gui, 'security_watermark_var'):
                self.gui.security_watermark_var.set(False)
            # DCT安全水印参数始终显示，不再隐藏
            # if hasattr(self, 'security_key_frame'):
            #     self.security_key_frame.pack_forget()
            # if hasattr(self, 'security_strength_frame'):
            #     self.security_strength_frame.pack_forget()
        
        self.gui.update_preview()

    def toggle_security_feature(self):
        """切换安全水印功能时的回调函数"""
        # 获取当前选中的安全水印
        scattered = hasattr(self.gui, 'scattered_watermark_var') and self.gui.scattered_watermark_var.get()
        invisible = hasattr(self.gui, 'invisible_watermark_var') and self.gui.invisible_watermark_var.get()
        texture = hasattr(self.gui, 'texture_watermark_var') and self.gui.texture_watermark_var.get()
        
        # 如果选择了任何一个安全水印，取消其他所有水印的勾选
        if scattered or invisible or texture:
            # 取消普通水印
            if hasattr(self.gui, 'normal_watermark_var'):
                self.gui.normal_watermark_var.set(False)
            # 取消DCT安全水印
            if hasattr(self.gui, 'security_watermark_var'):
                self.gui.security_watermark_var.set(False)
        
        # 确保分散水印、隐形水印、纹理水印之间互斥
        # 找出当前被选中的复选框
        widgets = []
        if hasattr(self.gui, 'scattered_watermark_var'):
            widgets.append((self.gui.scattered_watermark_var, "scattered"))
        if hasattr(self.gui, 'invisible_watermark_var'):
            widgets.append((self.gui.invisible_watermark_var, "invisible"))
        if hasattr(self.gui, 'texture_watermark_var'):
            widgets.append((self.gui.texture_watermark_var, "texture"))
        
        # 获取当前被勾选的数量
        checked_count = sum(1 for var, name in widgets if var.get())
        
        if checked_count > 1:
            # 找出最后被点击的那个（通过检查哪个是从未选中变为选中的）
            # 这里我们采用简单的策略：只保留当前被选中的，取消其他
            current_checked = None
            # 找出当前被点击的复选框
            for var, name in widgets:
                if var.get():
                    current_checked = name
                    break
            
            # 取消其他所有复选框
            for var, name in widgets:
                if name != current_checked:
                    var.set(False)
        
        self.gui.update_preview()

    def toggle_dct_security_watermark(self):
        """切换DCT安全水印时的回调函数"""
        if hasattr(self.gui, 'security_watermark_var') and self.gui.security_watermark_var.get():
            # 如果选择了DCT安全水印，自动取消所有其他水印的勾选
            if hasattr(self.gui, 'normal_watermark_var'):
                self.gui.normal_watermark_var.set(False)
            if hasattr(self.gui, 'scattered_watermark_var'):
                self.gui.scattered_watermark_var.set(False)
            if hasattr(self.gui, 'invisible_watermark_var'):
                self.gui.invisible_watermark_var.set(False)
            if hasattr(self.gui, 'texture_watermark_var'):
                self.gui.texture_watermark_var.set(False)
        else:
            # 如果取消DCT安全水印，自动选中普通水印
            if hasattr(self.gui, 'normal_watermark_var'):
                self.gui.normal_watermark_var.set(True)
        
        self.gui.update_preview()