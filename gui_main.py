import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
from PIL import Image
from watermark_processor.watermark_processor import WatermarkProcessor
from utils import DEFAULT_CONFIG, validate_color
import os

from gui_components.menu_bar import MenuBar
from gui_components.toolbar import Toolbar
from gui_components.control_panel import ControlPanel
from gui_components.image_preview import ImagePreview
from gui_components.theme import COLORS, SPACING, configure_styles


class WatermarkGUI:
    """水印添加器的GUI类"""
    
    def __init__(self, root):
        self.root = root
        self.watermark_processor = WatermarkProcessor()
        
        # 初始化变量
        self.original_image = None
        self.watermarked_image = None
        self.logo_path = None
        
        # 创建程序运行期间保持存在的临时目录
        import tempfile
        self.app_temp_dir = tempfile.mkdtemp(prefix="watermark_editor_")
        
        # 批量处理相关变量
        self.batch_images = []  # 存储批量处理的图片路径列表
        self.current_batch_index = 0  # 当前预览的图片索引
        self.batch_output_dir = None  # 批量处理输出目录
        
        # 初始化所有必要的变量，避免后续引用错误
        self._initialize_gui_variables()
        
        # 创建GUI界面
        self.create_widgets()
    
    def _initialize_gui_variables(self):
        """初始化所有GUI相关的变量"""
        from utils import DEFAULT_CONFIG
        
        # 水印类型相关
        self.watermark_type = tk.StringVar(value="text")
        
        # 文字水印相关
        self.text_entry = None  # 会在组件中初始化
        self.font_color = DEFAULT_CONFIG["default_font_color"]
        self.font_family_var = tk.StringVar(value="黑体")
        self.font_size_var = tk.IntVar(value=DEFAULT_CONFIG["default_font_size"])
        self.bold_var = tk.BooleanVar(value=False)
        self.italic_var = tk.BooleanVar(value=False)
        self.underline_var = tk.BooleanVar(value=False)
        
        # 颜色选择相关
        self.rgb_red_var = tk.IntVar(value=0)
        self.rgb_green_var = tk.IntVar(value=0)
        self.rgb_blue_var = tk.IntVar(value=0)
        
        # 阴影效果相关
        self.shadow_enable_var = tk.BooleanVar(value=False)
        self.shadow_color = "#000000"
        self.shadow_offset_x_var = tk.IntVar(value=2)
        self.shadow_offset_y_var = tk.IntVar(value=2)
        self.shadow_opacity_var = tk.IntVar(value=30)
        
        # 水印功能相关
        self.normal_watermark_var = tk.BooleanVar(value=True)
        self.scattered_watermark_var = tk.BooleanVar(value=False)
        self.invisible_watermark_var = tk.BooleanVar(value=False)
        self.texture_watermark_var = tk.BooleanVar(value=False)
        self.security_watermark_var = tk.BooleanVar(value=False)
        self.security_key_entry = None  # 会在组件中初始化
        self.security_strength_var = tk.DoubleVar(value=0.02)
        
        # Logo水印相关
        self.logo_path_var = tk.StringVar(value="未选择Logo")
        self.logo_size_var = tk.IntVar(value=100)
        self.logo_recolor_var = tk.StringVar(value="")  # 重着色颜色
        
        # 位置相关
        self.watermark_position = DEFAULT_CONFIG["default_position"]
        self.position_var = tk.StringVar(value=DEFAULT_CONFIG["default_position"])
        self.custom_position = (50, 50)
        self.custom_x_var = tk.IntVar(value=50)
        self.custom_y_var = tk.IntVar(value=50)
        
        # 透明度相关
        self.opacity_var = tk.IntVar(value=DEFAULT_CONFIG["default_opacity"])
        self.opacity_entry = None  # 会在组件中初始化
        
        # 旋转角度相关
        self.rotation_var = tk.IntVar(value=DEFAULT_CONFIG["default_rotation"])
        self.rotation_entry = None  # 会在组件中初始化
        
        # 翻转相关
        self.flip_horizontal = tk.BooleanVar(value=False)
        self.flip_vertical = tk.BooleanVar(value=False)
        
        # 操作范围相关
        self.operation_scope = tk.StringVar(value="single")
        
        # UI组件引用（避免hasattr检查）
        self.color_entry = None
        self.color_button = None
        self.shadow_color_button = None
        self.shadow_color_entry = None
        self.font_combobox = None
        self.text_settings_frame = None
        self.logo_settings_frame = None
        # 这些框架将由组件创建，不需要初始化为None
        # self.security_key_frame = None
        # self.security_strength_frame = None
    
    def create_widgets(self):
        """创建GUI控件"""
        # 配置样式
        configure_styles()
        
        # 设置窗口标题和大小
        self.root.title("VisMark - 智能图像水印处理工具")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        
        # 设置窗口背景色
        self.root.configure(bg=COLORS['background'])
        
        # 设置窗口图标（如果有）
        # self.root.iconbitmap("watermark.ico")
        
        # 配置网格布局
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # 创建菜单栏
        self.menu_bar = MenuBar(self.root, self)
        
        # 创建工具栏
        self.toolbar = Toolbar(self.root, self)
        
        # 创建主内容区
        self.main_frame = tk.Frame(self.root, bg=COLORS['background'])
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=SPACING['large'], pady=SPACING['medium'])
        
        # 配置主内容区网格
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=0)
        
        # 创建左侧控制面板
        self.control_panel = ControlPanel(self.main_frame, self)
        
        # 创建右侧图片预览区
        self.image_preview = ImagePreview(self.main_frame, self)
        
        # 初始状态：图片未加载时禁用相关控件
        self._update_control_states()
    
    def load_image(self):
        """加载图片"""
        file_path = filedialog.askopenfilename(
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.tif *.tiff")],
            title="选择图片"
        )
        
        if file_path:
            try:
                # 打开图片并确保转换为RGB模式
                image = Image.open(file_path)
                if image.mode not in ('RGB', 'RGBA'):
                    self.original_image = image.convert("RGB")
                else:
                    self.original_image = image.copy().convert("RGB")
                
                self.image_preview.display_original_image(self.original_image)
                self.update_preview()
                
                # 更新Logo大小滑块的范围
                self._update_logo_size_range()
                
                # 更新控件状态
                self._update_control_states()
                
                # 更新控件状态
                self._update_control_states()
            except Exception as e:
                messagebox.showerror("错误", f"加载图片失败: {str(e)}")
                print(f"加载图片失败: {str(e)}")
                import traceback
                traceback.print_exc()
    
    def load_logo(self):
        """加载Logo图片"""
        file_path = filedialog.askopenfilename(
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.tif *.tiff")],
            title="选择Logo图片"
        )
        
        if file_path:
            try:
                # 检查是否有图片被加载
                if not hasattr(self, 'original_image') or self.original_image is None:
                    messagebox.showerror("错误", "请先加载一张图片，然后再选择Logo")
                    return
                
                # 加载Logo并确保转换为RGBA模式
                logo = Image.open(file_path)
                if logo.mode not in ('RGBA'):
                    logo = logo.convert('RGBA')
                original_logo_width, original_logo_height = logo.size
                
                # 获取当前图片的尺寸
                image_width, image_height = self.original_image.size
                
                # 设置Logo大小限制为当前图片的50%
                max_logo_width = image_width * 0.5
                max_logo_height = image_height * 0.5
                
                # 检查Logo是否超过大小限制
                if original_logo_width > max_logo_width or original_logo_height > max_logo_height:
                    # 计算缩放比例
                    width_ratio = max_logo_width / original_logo_width
                    height_ratio = max_logo_height / original_logo_height
                    scale_ratio = min(width_ratio, height_ratio)
                    
                    # 计算新的Logo尺寸
                    new_logo_width = int(original_logo_width * scale_ratio)
                    new_logo_height = int(original_logo_height * scale_ratio)
                    
                    # 缩放Logo
                    logo = logo.resize((new_logo_width, new_logo_height), Image.LANCZOS)
                    
                    # 将缩放后的Logo保存到临时文件
                    import tempfile
                    temp_logo_path = os.path.join(self.app_temp_dir, f"scaled_{os.path.basename(file_path)}")
                    logo.save(temp_logo_path, format=logo.format if logo.format else 'PNG')
                    
                    # 更新Logo路径为临时文件
                    self.logo_path = temp_logo_path
                    self.logo_path_var.set(f"{os.path.basename(file_path)} (已缩放: {scale_ratio:.1%})")
                    
                    # 显示缩放信息
                    messagebox.showinfo("Logo自动缩放", f"Logo尺寸过大，已自动缩放以适应图片。\n\n原Logo尺寸: {original_logo_width}×{original_logo_height}\n当前图片尺寸: {image_width}×{image_height}\n缩放比例: {scale_ratio:.1%}\n新Logo尺寸: {new_logo_width}×{new_logo_height}")
                else:
                    # 正常加载Logo
                    self.logo_path = file_path
                    self.logo_path_var.set(os.path.basename(file_path))
                
                self.update_preview()
                
                # 更新Logo大小滑块的范围
                self._update_logo_size_range()
                
                # 更新控件状态
                self._update_control_states()
            except Exception as e:
                messagebox.showerror("错误", f"加载Logo失败: {str(e)}")
    
    def apply_watermark_to_selection(self):
        """根据用户选择的操作范围应用水印"""
        if not self.original_image:
            return
        
        # 应用水印到当前图片
        self.apply_watermark_to_current_image()
        
        # 如果用户选择了"所有图片"且有批量图片加载
        if hasattr(self, 'operation_scope') and self.operation_scope.get() == "all" and hasattr(self, 'batch_images') and self.batch_images:
            try:
                # 创建临时目录用于存储重新处理的结果
                import tempfile
                temp_dir = tempfile.mkdtemp()
                output_dir = temp_dir
                
                # 收集所有原始图片路径
                original_paths = [original_path for original_path, _ in self.batch_images]
                
                # 重新处理所有图片
                if self.watermark_type.get() == "text":
                    result = self.watermark_processor.batch_add_text_watermark(
                        original_paths,
                        self.text_entry.get(),
                        output_dir,
                        self.font_size_var.get(),
                        self.font_color,
                        self.font_family_var.get(),
                        self.bold_var.get(),
                        self.italic_var.get(),
                        self.underline_var.get(),
                        self.watermark_position,
                        self.opacity_var.get(),
                        self.rotation_var.get(),
                        self.flip_horizontal.get(),
                        self.flip_vertical.get(),
                        # 添加安全水印和阴影效果参数
                        scattered_watermark=self.scattered_watermark_var.get(),
                        invisible_watermark=self.invisible_watermark_var.get(),
                        texture_watermark=self.texture_watermark_var.get(),
                        enable_shadow=self.shadow_enable_var.get(),
                        shadow_color=self.shadow_color,
                        shadow_offset_x=self.shadow_offset_x_var.get(),
                        shadow_offset_y=self.shadow_offset_y_var.get(),
                        shadow_opacity=self.shadow_opacity_var.get(),
                        security_watermark=self.security_watermark_var.get(),
                        security_key=self.security_key_entry.get() if hasattr(self, 'security_key_entry') and self.security_key_entry is not None else "watermark123",
                        security_strength=self.security_strength_var.get()
                    )
                elif self.watermark_type.get() == "logo":
                    if not self.logo_path:
                        messagebox.showwarning("警告", "请先选择Logo图片")
                        return
                    
                    # 获取重着色颜色
                    recolor_color = self.logo_recolor_var.get() if hasattr(self, 'logo_recolor_var') else None
                    
                    result = self.watermark_processor.batch_add_logo_watermark(
                        original_paths,
                        self.logo_path,
                        output_dir,
                        self.logo_size_var.get(),
                        self.watermark_position,
                        self.control_panel.opacity_var.get(),
                        self.control_panel.rotation_var.get(),
                        self.control_panel.flip_horizontal.get(),
                        self.control_panel.flip_vertical.get(),
                        recolor_color
                    )

                
                # 更新批量图片列表
                self.batch_images = []
                for original_path, output_path, success in result:
                    if success:
                        self.batch_images.append((original_path, output_path))
                
            except Exception as e:
                messagebox.showerror("错误", f"批量应用水印失败: {str(e)}")
    
    def apply_watermark_to_current_image(self):
        """应用水印到当前图片"""
        if not self.original_image:
            return
        
        # 创建原始图片的副本（确保从干净的原始图片开始）
        preview_image = self.original_image.copy()
        
        # 获取水印位置
        position = self.watermark_position if hasattr(self, 'watermark_position') else "center"
        # 如果是自定义位置，传递坐标元组
        if position == "custom" and hasattr(self, 'custom_position'):
            position = self.custom_position
        
        # 添加水印
        watermarked_image = preview_image
        if hasattr(self, 'watermark_type') and self.watermark_type.get() == "text":
            # 安全地获取所有需要的参数，确保组件已经初始化
            text = "VisMark - 智能图像水印处理工具"  # 默认值
            if hasattr(self, 'text_entry') and self.text_entry is not None:
                text = self.text_entry.get()
            
            font_size = self.font_size_var.get() if hasattr(self, 'font_size_var') else 36
            font_color = self.font_color if hasattr(self, 'font_color') else "#000000"
            font_family = self.font_family_var.get() if hasattr(self, 'font_family_var') else "黑体"
            bold = self.bold_var.get() if hasattr(self, 'bold_var') else False
            italic = self.italic_var.get() if hasattr(self, 'italic_var') else False
            underline = self.underline_var.get() if hasattr(self, 'underline_var') else False
            opacity = self.opacity_var.get() if hasattr(self, 'opacity_var') else 50
            rotation = self.rotation_var.get() if hasattr(self, 'rotation_var') else 0
            flip_h = self.flip_horizontal.get() if hasattr(self, 'flip_horizontal') else False
            flip_v = self.flip_vertical.get() if hasattr(self, 'flip_vertical') else False
            
            # 阴影效果参数
            enable_shadow = self.shadow_enable_var.get() if hasattr(self, 'shadow_enable_var') else False
            shadow_color = self.shadow_color if hasattr(self, 'shadow_color') else "#000000"
            shadow_offset_x = self.shadow_offset_x_var.get() if hasattr(self, 'shadow_offset_x_var') else 2
            shadow_offset_y = self.shadow_offset_y_var.get() if hasattr(self, 'shadow_offset_y_var') else 2
            shadow_opacity = self.shadow_opacity_var.get() if hasattr(self, 'shadow_opacity_var') else 30
            
            # 水印功能参数
            normal_watermark = self.normal_watermark_var.get() if hasattr(self, 'normal_watermark_var') else True
            scattered_watermark = self.scattered_watermark_var.get() if hasattr(self, 'scattered_watermark_var') else False
            invisible_watermark = self.invisible_watermark_var.get() if hasattr(self, 'invisible_watermark_var') else False
            texture_watermark = self.texture_watermark_var.get() if hasattr(self, 'texture_watermark_var') else False
            
            watermarked_image = self.watermark_processor.add_text_watermark_to_image(
                preview_image,
                text,
                font_size,
                font_color,
                font_family,
                bold,
                italic,
                underline,
                position,
                opacity,
                rotation,
                flip_h,
                flip_v,
                # 添加阴影效果参数
                enable_shadow=enable_shadow,
                shadow_color=shadow_color,
                shadow_offset_x=shadow_offset_x,
                shadow_offset_y=shadow_offset_y,
                shadow_opacity=shadow_opacity,
                # 添加水印功能参数
                scattered_watermark=not normal_watermark and scattered_watermark,
                invisible_watermark=not normal_watermark and invisible_watermark,
                texture_watermark=not normal_watermark and texture_watermark
            )
        elif hasattr(self, 'watermark_type') and self.watermark_type.get() == "logo":
            if hasattr(self, 'logo_path') and self.logo_path:
                logo_size = self.logo_size_var.get() if hasattr(self, 'logo_size_var') else 100
                opacity = self.opacity_var.get() if hasattr(self, 'opacity_var') else 50
                rotation = self.rotation_var.get() if hasattr(self, 'rotation_var') else 0
                flip_h = self.flip_horizontal.get() if hasattr(self, 'flip_horizontal') else False
                flip_v = self.flip_vertical.get() if hasattr(self, 'flip_vertical') else False
                
                # 获取重着色颜色
                recolor_color = self.logo_recolor_var.get() if hasattr(self, 'logo_recolor_var') else None
                
                watermarked_image = self.watermark_processor.add_logo_watermark_to_image(
                    preview_image,
                    self.logo_path,
                    logo_size,
                    position,
                    opacity,
                    rotation,
                    flip_h,
                    flip_v,
                    recolor_color
                )

        
        # 应用DCT安全水印（如果启用）
        if hasattr(self, 'security_watermark_var') and self.security_watermark_var.get():
            key = "watermark123"  # 默认值
            if hasattr(self, 'security_key_entry') and self.security_key_entry is not None:
                key = self.security_key_entry.get()
            
            strength = self.security_strength_var.get() if hasattr(self, 'security_strength_var') else 0.02
            if key:
                # 安全地获取水印文本
                watermark_text = "LOGO_WATERMARK"
                if hasattr(self, 'text_entry') and self.text_entry is not None and hasattr(self, 'watermark_type') and self.watermark_type.get() == "text":
                    watermark_text = self.text_entry.get()
                
                # 应用DCT安全水印
                watermarked_image = self.watermark_processor.embed_security_watermark(
                    watermarked_image,
                    watermark_text,
                    key,
                    strength
                )
        
        # 显示水印图片
        self.image_preview.display_watermarked_image(watermarked_image)
        self.watermarked_image = watermarked_image
    
    def update_preview(self):
        """更新预览"""
        self.apply_watermark_to_selection()
    
    def toggle_watermark_type(self):
        """切换水印类型（文字/Logo）"""
        # 这个方法现在由各个组件自己处理，这里只需要更新预览
        self.update_preview()
    
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
            # 更新RGB滑块
            if hasattr(self, 'rgb_red_var') and hasattr(self, 'rgb_green_var') and hasattr(self, 'rgb_blue_var'):
                self._update_rgb_from_hex(self.font_color)
            self.update_preview()
    
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
                if hasattr(self, 'rgb_red_var'):
                    self.rgb_red_var.set(r)
                if hasattr(self, 'rgb_green_var'):
                    self.rgb_green_var.set(g)
                if hasattr(self, 'rgb_blue_var'):
                    self.rgb_blue_var.set(b)
        except (ValueError, IndexError):
            # 如果颜色格式无效，使用默认值
            if hasattr(self, 'rgb_red_var'):
                self.rgb_red_var.set(0)
            if hasattr(self, 'rgb_green_var'):
                self.rgb_green_var.set(0)
            if hasattr(self, 'rgb_blue_var'):
                self.rgb_blue_var.set(0)
    
    def choose_shadow_color(self):
        """选择阴影颜色"""
        color = colorchooser.askcolor(color=self.shadow_color)
        if color[1]:
            self.shadow_color = color[1]
            self.shadow_color_button.config(bg=self.shadow_color)
            self.shadow_color_entry.delete(0, tk.END)
            self.shadow_color_entry.insert(0, self.shadow_color)
            self.update_preview()
    
    def update_shadow_color(self, event):
        """更新阴影颜色"""
        color = self.shadow_color_entry.get()
        if validate_color(color):
            self.shadow_color = color
            self.shadow_color_button.config(bg=self.shadow_color)
            self.update_preview()
    
    def set_position(self, position):
        """设置水印位置"""
        self.watermark_position = position
        if position == "custom":
            self.custom_position = (self.custom_x_var.get(), self.custom_y_var.get())
        self.update_preview()
    
    def validate_opacity_input(self, value):
        """验证透明度输入"""
        if value == "":
            return True
        try:
            opacity = int(value)
            return 0 <= opacity <= 100
        except ValueError:
            return False
    
    def set_opacity_from_entry(self, event):
        """从输入框设置透明度"""
        try:
            opacity = int(self.opacity_entry.get())
            if 0 <= opacity <= 100:
                self.opacity_var.set(opacity)
                self.update_preview()
        except ValueError:
            pass
    
    def reset_opacity(self):
        """重置透明度"""
        self.opacity_var.set(DEFAULT_CONFIG["default_opacity"])
        self.opacity_entry.delete(0, tk.END)
        self.opacity_entry.insert(0, str(DEFAULT_CONFIG["default_opacity"]))
        self.update_preview()
    
    def validate_rotation_input(self, value):
        """验证旋转角度输入"""
        if value == "":
            return True
        try:
            rotation = int(value)
            return -180 <= rotation <= 180
        except ValueError:
            return False
    
    def set_rotation_from_entry(self, event):
        """从输入框设置旋转角度"""
        try:
            rotation = int(self.rotation_entry.get())
            if -180 <= rotation <= 180:
                self.rotation_var.set(rotation)
                self.update_preview()
        except ValueError:
            pass
    
    def reset_rotation(self):
        """重置旋转角度"""
        self.rotation_var.set(DEFAULT_CONFIG["default_rotation"])
        self.rotation_entry.delete(0, tk.END)
        self.rotation_entry.insert(0, str(DEFAULT_CONFIG["default_rotation"]))
        self.update_preview()
    
    def save_image(self):
        """保存水印图片"""
        if not self.watermarked_image:
            messagebox.showwarning("警告", "没有要保存的图片")
            return
        
        # 如果是批量处理的图片
        if hasattr(self, 'batch_images') and self.batch_images and hasattr(self, 'current_batch_index'):
            # 询问用户是保存当前图片还是全部图片
            save_option = messagebox.askyesnocancel(
                "保存选项",
                "选择保存方式:\n" \
                "是: 保存所有处理后的图片\n" \
                "否: 只保存当前查看的图片\n" \
                "取消: 取消保存"
            )
            
            if save_option is None:  # 用户点击了取消
                return
            elif save_option:  # 保存所有图片
                # 选择输出目录
                output_dir = filedialog.askdirectory(
                    parent=self.root,
                    title="选择输出目录",
                    initialdir=os.path.dirname(self.batch_images[0][0])
                )
                
                if not output_dir:
                    return
                
                # 保存所有图片
                import shutil
                success_count = 0
                saved_paths = []
                for original_path, temp_path in self.batch_images:
                    try:
                        # 获取原始文件名
                        filename = os.path.basename(original_path)
                        output_path = os.path.join(output_dir, filename)
                        
                        # 复制文件到目标目录
                        shutil.copy2(temp_path, output_path)
                        success_count += 1
                        saved_paths.append((original_path, output_path))
                    except Exception as e:
                        messagebox.showerror("错误", f"保存图片 {os.path.basename(original_path)} 失败: {str(e)}")
                        saved_paths.append((original_path, temp_path))  # 保存失败时保持原路径
                
                # 更新self.batch_images中的路径为实际保存路径
                self.batch_images = saved_paths
                self.batch_output_dir = output_dir
                
                messagebox.showinfo("成功", f"已成功保存 {success_count}/{len(self.batch_images)} 张图片到目录: {output_dir}")
            else:  # 只保存当前图片
                # 选择保存路径和格式
                file_path = filedialog.asksaveasfilename(
                    parent=self.root,
                    filetypes=[
                        ("JPEG 图片", "*.jpg *.jpeg"),
                        ("PNG 图片", "*.png"),
                        ("BMP 图片", "*.bmp"),
                        ("GIF 图片", "*.gif"),
                        ("TIFF 图片", "*.tif *.tiff"),
                        ("所有文件", "*.*")
                    ],
                    title="保存当前图片",
                    defaultextension=".jpg"
                )
                
                if not file_path:
                    return
                
                try:
                    # 获取文件扩展名
                    ext = os.path.splitext(file_path)[1].lower()
                    
                    # 根据扩展名选择保存格式
                    if ext in [".jpg", ".jpeg"]:
                        # JPEG格式不支持透明度，需要转换为RGB
                        if self.watermarked_image.mode in ["RGBA", "LA"]:
                            self.watermarked_image = self.watermarked_image.convert("RGB")
                        self.watermarked_image.save(file_path, "JPEG", quality=95)
                    elif ext == ".png":
                        self.watermarked_image.save(file_path, "PNG")
                    elif ext == ".bmp":
                        self.watermarked_image.save(file_path, "BMP")
                    elif ext in [".gif", ".tif", ".tiff"]:
                        self.watermarked_image.save(file_path)
                    else:
                        # 默认保存为JPEG
                        if self.watermarked_image.mode in ["RGBA", "LA"]:
                            self.watermarked_image = self.watermarked_image.convert("RGB")
                        self.watermarked_image.save(file_path, "JPEG", quality=95)
                    
                    messagebox.showinfo("成功", "图片保存成功")
                except Exception as e:
                    messagebox.showerror("错误", f"保存图片失败: {str(e)}")
        else:  # 单张图片保存
            # 选择保存路径和格式
            file_path = filedialog.asksaveasfilename(
                parent=self.root,
                filetypes=[
                    ("JPEG 图片", "*.jpg *.jpeg"),
                    ("PNG 图片", "*.png"),
                    ("BMP 图片", "*.bmp"),
                    ("GIF 图片", "*.gif"),
                    ("TIFF 图片", "*.tif *.tiff"),
                    ("所有文件", "*.*")
                ],
                title="保存图片",
                defaultextension=".jpg"
            )
            
            if not file_path:
                return
            
            try:
                # 获取文件扩展名
                ext = os.path.splitext(file_path)[1].lower()
                
                # 根据扩展名选择保存格式
                if ext in [".jpg", ".jpeg"]:
                    # JPEG格式不支持透明度，需要转换为RGB
                    if self.watermarked_image.mode in ["RGBA", "LA"]:
                        self.watermarked_image = self.watermarked_image.convert("RGB")
                    self.watermarked_image.save(file_path, "JPEG", quality=95)
                elif ext == ".png":
                    self.watermarked_image.save(file_path, "PNG")
                elif ext == ".bmp":
                    self.watermarked_image.save(file_path, "BMP")
                elif ext in [".gif", ".tif", ".tiff"]:
                    self.watermarked_image.save(file_path)
                else:
                    # 默认保存为JPEG
                    if self.watermarked_image.mode in ["RGBA", "LA"]:
                        self.watermarked_image = self.watermarked_image.convert("RGB")
                    self.watermarked_image.save(file_path, "JPEG", quality=95)
                
                messagebox.showinfo("成功", "图片保存成功")
            except Exception as e:
                messagebox.showerror("错误", f"保存图片失败: {str(e)}")
    
    def load_first_batch_image(self, result, output_dir):
        """加载批量处理后的第一张图片"""
        # 清空之前的批量图片列表
        self.batch_images = []
        
        # 收集成功处理的图片路径
        for original_path, output_path, success in result:
            if success:
                self.batch_images.append((original_path, output_path))
        
        if self.batch_images:
            self.batch_output_dir = output_dir
            self.current_batch_index = 0
            
            # 显示导航控制按钮
            self.image_preview.show_batch_navigation()
            
            # 加载并显示第一张图片
            self.display_batch_image(self.current_batch_index)
    
    def display_batch_image(self, index):
        """显示指定索引的批量图片"""
        if not self.batch_images or index < 0 or index >= len(self.batch_images):
            return
        
        original_path, output_path = self.batch_images[index]
        
        try:
            # 加载原始图片和处理后的图片
            self.original_image = Image.open(original_path)
            self.watermarked_image = Image.open(output_path)
            
            # 显示原始图片和处理后的图片
            self.image_preview.display_original_image(self.original_image)
            self.image_preview.display_watermarked_image(self.watermarked_image)
            
            # 更新图片信息
            self.image_preview.update_batch_info(index + 1, len(self.batch_images))
            
            # 更新导航按钮状态
            self.image_preview.update_navigation_buttons(index, len(self.batch_images))
        except Exception as e:
            messagebox.showerror("错误", f"加载图片失败: {str(e)}")
    
    def previous_batch_image(self):
        """显示上一张批量处理的图片"""
        if self.current_batch_index > 0:
            self.current_batch_index -= 1
            self.display_batch_image(self.current_batch_index)
    
    def next_batch_image(self):
        """显示下一张批量处理的图片"""
        if self.current_batch_index < len(self.batch_images) - 1:
            self.current_batch_index += 1
            self.display_batch_image(self.current_batch_index)
    
    def batch_process(self):
        """批量处理图片"""
        # 确保根窗口是活动窗口
        self.root.lift()
        self.root.focus_force()
        
        # 创建进度条窗口
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title("批量处理进度")
        self.progress_window.geometry("300x100")
        self.progress_window.resizable(False, False)
        self.progress_window.transient(self.root)  # 使进度条窗口随主窗口移动
        self.progress_window.grab_set()  # 模态窗口
        
        # 添加进度条
        self.progress_label = tk.Label(self.progress_window, text="准备处理...")
        self.progress_label.pack(pady=10)
        
        self.progress_bar = tk.ttk.Progressbar(self.progress_window, orient="horizontal", length=250, mode="determinate")
        self.progress_bar.pack(pady=10)
        
        # 选择图片文件
        try:
            # 为了确保文件选择对话框正常工作，我们可以尝试使用不同的方式调用
            file_paths = filedialog.askopenfilenames(
                parent=self.root,
                filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.tif *.tiff")],
                title="选择要处理的图片"
            )
        except Exception as e:
            messagebox.showerror("错误", f"文件选择失败: {str(e)}")
            return
        
        if not file_paths:
            print("没有选择任何文件")
            self.progress_window.destroy()  # 关闭进度条窗口
            return
        
        # 使用应用程序级别的临时目录存储处理结果
        import os
        # 在应用程序临时目录内创建一个唯一的子目录
        import uuid
        batch_temp_dir = os.path.join(self.app_temp_dir, str(uuid.uuid4()))
        os.makedirs(batch_temp_dir, exist_ok=True)
        output_dir = batch_temp_dir
        
        # 进度回调函数
        def update_progress(completed, total):
            progress = int((completed / total) * 100)
            self.progress_bar['value'] = progress
            self.progress_label.config(text=f"处理中... {completed}/{total} ({progress}%)")
            # 确保GUI刷新
            self.progress_window.update_idletasks()
            self.progress_window.update()
        
        # 开始批量处理
        if hasattr(self, 'watermark_type') and self.watermark_type.get() == "text":
            # 构建字体样式字符串
            font_style = ""
            if hasattr(self, 'bold_var') and self.bold_var.get():
                font_style += "bold "
            if hasattr(self, 'italic_var') and self.italic_var.get():
                font_style += "italic "
            if hasattr(self, 'underline_var') and self.underline_var.get():
                font_style += "underline "
            font_style = font_style.strip() or "normal"
            
            result = self.watermark_processor.batch_add_text_watermark(
                file_paths,
                self.text_entry.get() if hasattr(self, 'text_entry') and self.text_entry is not None else DEFAULT_CONFIG["default_text"],
                output_dir,
                self.font_size_var.get() if hasattr(self, 'font_size_var') else 24,
                self.font_color if hasattr(self, 'font_color') else "#000000",
                self.font_family_var.get() if hasattr(self, 'font_family_var') else "Arial",
                self.bold_var.get() if hasattr(self, 'bold_var') else False,
                self.italic_var.get() if hasattr(self, 'italic_var') else False,
                self.underline_var.get() if hasattr(self, 'underline_var') else False,
                self.watermark_position if hasattr(self, 'watermark_position') else "center",
                self.opacity_var.get() if hasattr(self, 'opacity_var') else 50,
                self.rotation_var.get() if hasattr(self, 'rotation_var') else 0,
                self.flip_horizontal.get() if hasattr(self, 'flip_horizontal') else False,
                self.flip_vertical.get() if hasattr(self, 'flip_vertical') else False,
                progress_callback=update_progress,
                scattered_watermark=self.scattered_watermark_var.get() if hasattr(self, 'scattered_watermark_var') else False,
                invisible_watermark=self.invisible_watermark_var.get() if hasattr(self, 'invisible_watermark_var') else False,
                texture_watermark=self.texture_watermark_var.get() if hasattr(self, 'texture_watermark_var') else False,
                enable_shadow=self.shadow_enable_var.get() if hasattr(self, 'shadow_enable_var') else False,
                shadow_color=self.shadow_color if hasattr(self, 'shadow_color') else "#000000",
                shadow_offset_x=self.shadow_offset_x_var.get() if hasattr(self, 'shadow_offset_x_var') else 2,
                shadow_offset_y=self.shadow_offset_y_var.get() if hasattr(self, 'shadow_offset_y_var') else 2,
                shadow_opacity=self.shadow_opacity_var.get() if hasattr(self, 'shadow_opacity_var') else 30,
                security_watermark=self.security_watermark_var.get() if hasattr(self, 'security_watermark_var') else False,
                security_key=self.security_key_entry.get() if hasattr(self, 'security_key_entry') and self.security_key_entry is not None else "watermark123",
                security_strength=self.security_strength_var.get() if hasattr(self, 'security_strength_var') else 0.02
            )
        else:
            if not self.logo_path:
                messagebox.showwarning("警告", "请先选择Logo图片")
                return
            
            # 获取重着色颜色
            recolor_color = self.logo_recolor_var.get() if hasattr(self, 'logo_recolor_var') else None
            
            result = self.watermark_processor.batch_add_logo_watermark(
                file_paths,
                self.logo_path,
                output_dir,
                self.logo_size_var.get() if hasattr(self, 'logo_size_var') else 100,
                self.watermark_position if hasattr(self, 'watermark_position') else "center",
                self.opacity_var.get() if hasattr(self, 'opacity_var') else 50,
                self.rotation_var.get() if hasattr(self, 'rotation_var') else 0,
                self.flip_horizontal.get() if hasattr(self, 'flip_horizontal') else False,
                self.flip_vertical.get() if hasattr(self, 'flip_vertical') else False,
                recolor_color,
                progress_callback=update_progress
            )
        
        # 统计结果
        success_count = sum(1 for _, _, success in result if success)
        total_count = len(result)
        
        # 关闭进度条窗口
        if hasattr(self, 'progress_window') and self.progress_window.winfo_exists():
            self.progress_window.destroy()
        
        # 加载并显示第一张成功处理的图片
        self.load_first_batch_image(result, output_dir)
        
        # 更新控件状态，确保按钮可用
        self._update_control_states()
        
        messagebox.showinfo(
            "批量处理完成",
            f"已处理 {total_count} 张图片，成功 {success_count} 张，失败 {total_count - success_count} 张\n\n" \
            f"您可以在预览界面查看处理结果，点击'保存'按钮选择输出目录保存图片"
        )
    
    def _update_logo_size_range(self):
        """更新Logo大小滑块的范围"""
        if hasattr(self, 'control_panel') and hasattr(self.control_panel, 'sections'):
            logo_section = self.control_panel.sections.get('logo_settings')
            if logo_section and hasattr(logo_section, '_update_logo_size_range'):
                logo_section._update_logo_size_range()
    
    def _update_control_states(self):
        """根据当前状态更新控件启用/禁用状态"""
        # 图片是否已加载
        image_loaded = self.original_image is not None
        # Logo是否已选择
        logo_selected = self.logo_path is not None
        
        # 更新工具栏按钮状态
        if hasattr(self, 'toolbar'):
            self.toolbar.update_control_states(image_loaded, logo_selected)
        
        # 更新控制面板状态
        if hasattr(self, 'control_panel'):
            self.control_panel.update_control_states(image_loaded, logo_selected)
    
    def clear_watermark(self):
        """清除水印"""
        if self.original_image:
            self.image_preview.display_original_image(self.original_image)
            self.image_preview.display_watermarked_image(self.original_image)
            self.watermarked_image = self.original_image.copy()
    
    def smart_watermark_position(self):
        """智能选择水印位置"""
        if not self.original_image:
            messagebox.showwarning("警告", "请先加载图片")
            return
        
        # 简单的智能水印位置算法：选择图片中最不复杂的区域
        img = self.original_image.convert("L")  # 转换为灰度图
        width, height = img.size
        
        # 定义四个角落的区域大小
        corner_size = 50
        
        # 计算四个角落的平均亮度
        corners = [
            ("top-left", img.crop((0, 0, corner_size, corner_size))),
            ("top-right", img.crop((width - corner_size, 0, width, corner_size))),
            ("bottom-left", img.crop((0, height - corner_size, corner_size, height))),
            ("bottom-right", img.crop((width - corner_size, height - corner_size, width, height)))
        ]
        
        corner_brightness = {}
        for corner_name, corner_img in corners:
            # 计算平均亮度
            pixels = list(corner_img.getdata())
            avg_brightness = sum(pixels) / len(pixels)
            corner_brightness[corner_name] = avg_brightness
        
        # 选择最亮的角落（最不复杂的区域）
        best_corner = max(corner_brightness, key=corner_brightness.get)
        
        # 应用最佳位置
        self.control_panel.set_position(best_corner)
        self.update_preview()
        
        messagebox.showinfo("智能位置选择", f"已自动选择最佳水印位置：{best_corner}\n\n系统根据图片内容复杂度选择了最不显眼的区域。")
    
    def save_style(self):
        """保存样式"""
        style_name = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json")],
            title="保存样式"
        )
        
        if style_name:
            import json
            
            # 构建字体样式字符串
            font_style = ""
            if self.bold_var.get():
                font_style += "bold "
            if self.italic_var.get():
                font_style += "italic "
            if self.underline_var.get():
                font_style += "underline "
            font_style = font_style.strip() or "normal"
            
            style = {
                "text": self.text_entry.get() if hasattr(self, 'text_entry') and self.text_entry is not None else DEFAULT_CONFIG["default_text"],
                "font_size": self.font_size_var.get(),
                "font_color": self.font_color,
                "font_style": font_style,
                "position": self.watermark_position,
                "opacity": self.opacity_var.get(),
                "rotation": self.rotation_var.get(),
                "flip_horizontal": self.flip_horizontal.get(),
                "flip_vertical": self.flip_vertical.get(),
                "watermark_type": self.watermark_type.get(),
                "logo_path": self.logo_path,
                "logo_size": self.logo_size_var.get()
            }
            
            try:
                with open(style_name, "w") as f:
                    json.dump(style, f, indent=4)
                messagebox.showinfo("成功", "样式保存成功")
            except Exception as e:
                messagebox.showerror("错误", f"保存样式失败: {str(e)}")
    
    def load_style(self):
        """加载样式"""
        style_name = filedialog.askopenfilename(
            filetypes=[("JSON文件", "*.json")],
            title="加载样式"
        )
        
        if style_name:
            import json
            try:
                with open(style_name, "r") as f:
                    style = json.load(f)
                
                # 应用样式
                if hasattr(self, 'text_entry') and self.text_entry is not None:
                    self.text_entry.delete(0, tk.END)
                    self.text_entry.insert(0, style.get("text", ""))
                self.font_size_var.set(style.get("font_size", DEFAULT_CONFIG["default_font_size"]))
                self.font_color = style.get("font_color", DEFAULT_CONFIG["default_font_color"])
                if hasattr(self, 'color_button'):
                    self.color_button.config(bg=self.font_color)
                if hasattr(self, 'color_entry'):
                    self.color_entry.delete(0, tk.END)
                    self.color_entry.insert(0, self.font_color)
                
                # 设置字体样式
                font_style = style.get("font_style", DEFAULT_CONFIG["default_font_style"])
                self.bold_var.set("bold" in font_style)
                self.italic_var.set("italic" in font_style)
                self.underline_var.set("underline" in font_style)
                
                self.set_position(style.get("position", DEFAULT_CONFIG["default_position"]))
                self.opacity_var.set(style.get("opacity", DEFAULT_CONFIG["default_opacity"]))
                self.rotation_var.set(style.get("rotation", DEFAULT_CONFIG["default_rotation"]))
                
                # 设置翻转
                self.flip_horizontal.set(style.get("flip_horizontal", False))
                self.flip_vertical.set(style.get("flip_vertical", False))
                
                # 设置水印类型
                watermark_type = style.get("watermark_type", "text")
                self.watermark_type.set(watermark_type)
                self.control_panel.toggle_watermark_type()
                
                # 设置Logo相关参数
                self.logo_path = style.get("logo_path", "")
                self.logo_path_var.set(os.path.basename(self.logo_path) if self.logo_path else "未选择Logo")
                self.logo_size_var.set(style.get("logo_size", 100))
                
                self.update_preview()
                messagebox.showinfo("成功", "样式加载成功")
                
            except Exception as e:
                messagebox.showerror("错误", f"加载样式失败: {str(e)}")
    
    def show_about(self):
        """显示关于信息"""
        messagebox.showinfo(
            "关于",
            "VisMark - 智能图像水印处理工具 v1.0\n\n"
            "基于Python和Pillow开发的水印添加工具\n\n"
            "功能特点：\n"
            "- 支持文字水印和图片Logo水印\n"
            "- 提供丰富的水印自定义选项\n"
            "- 支持批量处理多张图片\n"
            "- 实时预览水印效果\n"
            "- 支持水印翻转和旋转\n"
            "- 智能水印位置检测\n"
            "- 支持保存和加载水印样式"
        )


def main():
    """主函数"""
    root = tk.Tk()
    app = WatermarkGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()