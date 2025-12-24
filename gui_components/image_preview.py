import tkinter as tk
from PIL import Image, ImageTk
from gui_components.theme import COLORS, FONTS, SPACING, create_section_title, create_modern_button


class ImagePreview:
    """图片预览组件"""
    
    def __init__(self, parent, gui):
        self.parent = parent
        self.gui = gui
        self.create_image_preview()
    
    def create_image_preview(self):
        """创建图片预览区 - 只显示水印效果预览"""
        preview_frame = tk.Frame(self.parent, bg=COLORS['background'])
        preview_frame.grid(row=0, column=1, sticky="nsew")
        
        # 配置预览区网格布局
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
        
        # 水印效果预览（专业设计）
        watermarked_frame = tk.Frame(preview_frame, bg=COLORS['background_light'], relief=tk.FLAT, bd=1)
        watermarked_frame.grid(row=0, column=0, sticky="nsew", padx=SPACING['medium'], pady=SPACING['medium'])
        
        # 预览标题栏
        preview_header = create_section_title(watermarked_frame, "预览效果", COLORS['background_light'])
        preview_header.pack(fill="x", padx=SPACING['medium'], pady=SPACING['medium'])
        
        # 预览画布
        self.watermarked_canvas = tk.Canvas(watermarked_frame, bg=COLORS['background_dark'], relief=tk.SUNKEN, bd=1, highlightthickness=0)
        self.watermarked_canvas.pack(fill="both", expand=True, padx=SPACING['medium'], pady=SPACING['medium'])
        
        # 绑定窗口大小变化事件
        self.watermarked_canvas.bind("<Configure>", self._on_canvas_configure)
        
        # 批量预览控制按钮
        self.batch_nav_frame = tk.Frame(watermarked_frame, bg=COLORS['background_light'])
        # 初始时隐藏，批量处理完成后显示
        
        self.prev_button = create_modern_button(self.batch_nav_frame, "上一张", self.gui.previous_batch_image, style='secondary')
        self.prev_button.pack(side="left", padx=SPACING['medium'], pady=SPACING['medium'])
        
        self.batch_info_label = tk.Label(self.batch_nav_frame, text="", bg=COLORS['background_light'], 
                                        fg=COLORS['text_secondary'], font=FONTS['body'])
        self.batch_info_label.pack(side="left", padx=SPACING['medium'], pady=SPACING['medium'])
        
        self.next_button = create_modern_button(self.batch_nav_frame, "下一张", self.gui.next_batch_image, style='secondary')
        self.next_button.pack(side="left", padx=SPACING['medium'], pady=SPACING['medium'])
        
        # 初始化一个空白的预览图
        self.original_canvas = self.watermarked_canvas  # 保持与原有代码兼容
        blank_image = Image.new('RGB', (800, 600), color=COLORS['background_dark'])
        self.display_image(self.watermarked_canvas, blank_image)
    
    def display_original_image(self, image):
        """显示原始图片"""
        self.display_image(self.original_canvas, image)
    
    def display_watermarked_image(self, image):
        """显示水印图片"""
        self.display_image(self.watermarked_canvas, image)
    
    def display_image(self, canvas, image):
        """在Canvas上显示图片"""
        # 清除Canvas内容
        canvas.delete("all")
        
        # 获取Canvas大小
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        # 确保Canvas有有效的尺寸
        if canvas_width <= 0 or canvas_height <= 0:
            # 使用默认尺寸
            canvas_width = 800
            canvas_height = 600
        
        # 计算图片大小（保持宽高比）
        img_width, img_height = image.size
        
        if img_width <= canvas_width and img_height <= canvas_height:
            # 图片小于Canvas，直接显示
            display_image = image
        else:
            # 缩放图片以适应Canvas
            scale = min(canvas_width / img_width, canvas_height / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            # 确保新尺寸大于0
            new_width = max(1, new_width)
            new_height = max(1, new_height)
            display_image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # 计算图片位置（居中）
        x = (canvas_width - display_image.width) // 2
        y = (canvas_height - display_image.height) // 2
        
        # 转换为Tkinter兼容的图像
        tk_image = ImageTk.PhotoImage(display_image)
        
        # 保存图像引用（避免被垃圾回收）
        canvas.tk_image = tk_image
        
        # 显示图像
        canvas.create_image(x, y, anchor="nw", image=tk_image)
        
        # 保存图片相关信息到canvas
        # 如果图片小于Canvas，scale设为1
        scale = getattr(canvas.image_info, "scale", 1.0) if hasattr(canvas, "image_info") else 1.0
        if img_width > canvas_width or img_height > canvas_height:
            scale = min(canvas_width / img_width, canvas_height / img_height)
        
        canvas.image_info = {
            "original_size": (img_width, img_height),
            "display_size": (display_image.width, display_image.height),
            "position": (x, y),
            "scale": scale
        }
        
        # 添加鼠标事件监听器（仅当选择了自定义位置时）
        if hasattr(self.gui, 'watermark_position') and self.gui.watermark_position == "custom":
            # 移除旧的事件绑定
            canvas.unbind("<Button-1>")
            canvas.unbind("<B1-Motion>")
            canvas.unbind("<ButtonRelease-1>")
            
            # 绑定新的事件
            canvas.bind("<Button-1>", lambda e: self.on_mouse_press(e, canvas))
            canvas.bind("<B1-Motion>", lambda e: self.on_mouse_drag(e, canvas))
            canvas.bind("<ButtonRelease-1>", lambda e: self.on_mouse_release(e, canvas))
        else:
            # 移除事件绑定
            canvas.unbind("<Button-1>")
            canvas.unbind("<B1-Motion>")
            canvas.unbind("<ButtonRelease-1>")
    
    def on_mouse_press(self, event, canvas):
        """鼠标按下事件处理"""
        if not hasattr(canvas, 'image_info') or not self.gui.original_image:
            return
        
        # 检查鼠标是否在图片区域内
        image_info = canvas.image_info
        img_x, img_y = image_info["position"]
        img_width, img_height = image_info["display_size"]
        
        if (img_x <= event.x <= img_x + img_width and 
            img_y <= event.y <= img_y + img_height):
            # 记录按下时的位置信息
            canvas.dragging = True
            canvas.start_x = event.x
            canvas.start_y = event.y
            
            # 记录当前的自定义位置
            if hasattr(self.gui, 'custom_position'):
                canvas.current_custom_x = self.gui.custom_position[0]
                canvas.current_custom_y = self.gui.custom_position[1]
        else:
            canvas.dragging = False
    
    def on_mouse_drag(self, event, canvas):
        """鼠标拖拽事件处理"""
        if not hasattr(canvas, 'dragging') or not canvas.dragging:
            return
        
        if not hasattr(canvas, 'image_info') or not self.gui.original_image:
            return
        
        # 获取图片信息
        image_info = canvas.image_info
        original_width, original_height = image_info["original_size"]
        display_width, display_height = image_info["display_size"]
        img_x, img_y = image_info["position"]
        scale = image_info["scale"]
        
        # 计算鼠标在图片上的相对移动距离（基于显示尺寸）
        delta_x = event.x - canvas.start_x
        delta_y = event.y - canvas.start_y
        
        # 转换为原始图片上的移动距离
        original_delta_x = int(delta_x / scale)
        original_delta_y = int(delta_y / scale)
        
        # 计算新的自定义位置
        new_x = canvas.current_custom_x + original_delta_x
        new_y = canvas.current_custom_y + original_delta_y
        
        # 限制位置在图片范围内
        new_x = max(0, min(new_x, original_width))
        new_y = max(0, min(new_y, original_height))
        
        # 更新自定义位置
        self.gui.custom_position = (new_x, new_y)
        
        # 计算百分比值
        x_percent = int((new_x / original_width) * 100)
        y_percent = int((new_y / original_height) * 100)
        
        # 更新滑块值（不触发回调，避免重复更新）
        if hasattr(self.gui, 'custom_x_var'):
            self.gui.custom_x_var.set(x_percent)
        if hasattr(self.gui, 'custom_y_var'):
            self.gui.custom_y_var.set(y_percent)
        
        # 更新预览
        self.gui.update_preview()
    
    def on_mouse_release(self, event, canvas):
        """鼠标释放事件处理"""
        if hasattr(canvas, 'dragging'):
            canvas.dragging = False
    
    def show_batch_navigation(self):
        """显示批量导航控制"""
        self.batch_nav_frame.pack(fill="x", padx=5, pady=5)
    
    def update_batch_info(self, current_index, total_count):
        """更新批量图片信息"""
        self.batch_info_label.config(text=f"图片 {current_index}/{total_count}")
    
    def update_navigation_buttons(self, current_index, total_count):
        """更新导航按钮状态"""
        self.prev_button.config(state="disabled" if current_index == 0 else "normal")
        self.next_button.config(state="disabled" if current_index == total_count - 1 else "normal")
    
    def _on_canvas_configure(self, event):
        """Canvas大小变化时的回调函数"""
        # 如果当前有图片显示，重新显示以适应新的大小
        if hasattr(self.watermarked_canvas, 'tk_image'):
            # 获取当前显示的图片
            if hasattr(self.gui, 'watermarked_image') and self.gui.watermarked_image:
                self.display_watermarked_image(self.gui.watermarked_image)
            elif hasattr(self.gui, 'original_image') and self.gui.original_image:
                self.display_original_image(self.gui.original_image)