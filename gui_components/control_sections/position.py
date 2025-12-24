import tkinter as tk
from utils import DEFAULT_CONFIG


class PositionSection:
    """水印位置设置部分"""
    
    def __init__(self, parent, gui):
        self.parent = parent
        self.gui = gui
        self.create_section()
    
    def create_section(self):
        """创建水印位置设置部分"""
        tk.Label(self.parent, text="水印位置", bg="#f5f5f5", font=("黑体", 12, "bold")).pack(pady=(10, 5), anchor="w", padx=10)
        
        position_frame = tk.Frame(self.parent, bg="#f5f5f5")
        position_frame.pack(pady=5, padx=10, fill=tk.X)
        
        # 初始化位置变量
        if not hasattr(self.gui, 'position_var'):
            self.gui.position_var = tk.StringVar(value=DEFAULT_CONFIG["default_position"])
        
        # 位置映射
        position_mapping = {
            "top-left": "↖",
            "top": "↑",
            "top-right": "↗",
            "left": "←",
            "center": "●",
            "right": "→",
            "bottom-left": "↙",
            "bottom": "↓",
            "bottom-right": "↘",
            "full_cover": "全",
            "custom": "自"
        }
        
        position_names = {
            "top-left": "左上角",
            "top": "顶部居中",
            "top-right": "右上角",
            "left": "左侧居中",
            "center": "居中",
            "right": "右侧居中",
            "bottom-left": "左下角",
            "bottom": "底部居中",
            "bottom-right": "右下角",
            "full_cover": "覆盖全图",
            "custom": "自定义位置"
        }
        
        # 创建9宫格按钮布局
        grid_frame = tk.Frame(position_frame, bg="#f5f5f5")
        grid_frame.pack(pady=10)
        
        # 9宫格位置定义
        grid_positions = [
            (0, 0, "top-left"), (0, 1, "top"), (0, 2, "top-right"),
            (1, 0, "left"), (1, 1, "center"), (1, 2, "right"),
            (2, 0, "bottom-left"), (2, 1, "bottom"), (2, 2, "bottom-right")
        ]
        
        # 创建位置按钮 - 改为正方形样式
        self.position_buttons = {}
        for row, col, position in grid_positions:
            button = tk.Button(grid_frame, text=position_mapping[position], 
                             font=("黑体", 12, "bold"), width=4, height=2,
                             bg="#e0e0e0", fg="black",
                             activebackground="#d0d0d0", activeforeground="black",
                             relief="solid", bd=1,
                             command=lambda pos=position: self._select_position(pos))
            button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self.position_buttons[position] = button
            
            # 设置网格权重
            grid_frame.grid_rowconfigure(row, weight=1)
            grid_frame.grid_columnconfigure(col, weight=1)
        
        # 调整网格框架的尺寸，使按钮更接近正方形
        grid_frame.configure(width=150, height=150)
        
        # 特殊位置按钮（覆盖全图和自定义位置）
        special_frame = tk.Frame(position_frame, bg="#f5f5f5")
        special_frame.pack(pady=10, fill=tk.X)
        
        # 覆盖全图按钮
        full_cover_btn = tk.Button(special_frame, text="覆盖全图", 
                                 font=("黑体", 10), width=10, height=1,
                                 bg="#e0e0e0", fg="black",
                                 activebackground="#d0d0d0", activeforeground="black",
                                 relief="solid", bd=1,
                                 command=lambda: self._select_position("full_cover"))
        full_cover_btn.pack(side="left", padx=5, pady=5)
        self.position_buttons["full_cover"] = full_cover_btn
        
        # 自定义位置按钮
        custom_btn = tk.Button(special_frame, text="自定义位置", 
                             font=("黑体", 10), width=10, height=1,
                             bg="#e0e0e0", fg="black",
                             activebackground="#d0d0d0", activeforeground="black",
                             relief="solid", bd=1,
                             command=lambda: self._select_position("custom"))
        custom_btn.pack(side="left", padx=5, pady=5)
        self.position_buttons["custom"] = custom_btn
        
        # 位置显示标签
        self.position_label = tk.Label(position_frame, text="当前位置：居中", 
                                     bg="#f5f5f5", font=("黑体", 10))
        self.position_label.pack(pady=5)
        
        # 自定义位置滑块控件
        if not hasattr(self.gui, 'custom_position_frame'):
            self.gui.custom_position_frame = tk.Frame(self.parent, bg="#f5f5f5")
            
            # X轴滑块
            tk.Label(self.gui.custom_position_frame, text="X位置:", bg="#f5f5f5").pack(anchor="w", padx=5, pady=5)
            x_slider_frame = tk.Frame(self.gui.custom_position_frame, bg="#f5f5f5")
            x_slider_frame.pack(fill=tk.X, padx=5, pady=5)
            
            tk.Label(x_slider_frame, text="左").pack(side="left", padx=5)
            if not hasattr(self.gui, 'custom_x_var'):
                self.gui.custom_x_var = tk.IntVar(value=50)
            if not hasattr(self.gui, 'custom_x_slider') or self.gui.custom_x_slider is None:
                self.gui.custom_x_slider = tk.Scale(x_slider_frame, from_=0, to=100, variable=self.gui.custom_x_var,
                                          orient="horizontal", bg="#f5f5f5", command=lambda x: self._update_custom_position())
            self.gui.custom_x_slider.pack(side="left", fill=tk.X, expand=True, padx=5)
            tk.Label(x_slider_frame, text="右").pack(side="right", padx=5)
            
            # Y轴滑块
            tk.Label(self.gui.custom_position_frame, text="Y位置:", bg="#f5f5f5").pack(anchor="w", padx=5, pady=5)
            y_slider_frame = tk.Frame(self.gui.custom_position_frame, bg="#f5f5f5")
            y_slider_frame.pack(fill=tk.X, padx=5, pady=5)
            
            tk.Label(y_slider_frame, text="上").pack(side="left", padx=5)
            if not hasattr(self.gui, 'custom_y_var'):
                self.gui.custom_y_var = tk.IntVar(value=50)
            if not hasattr(self.gui, 'custom_y_slider') or self.gui.custom_y_slider is None:
                self.gui.custom_y_slider = tk.Scale(y_slider_frame, from_=0, to=100, variable=self.gui.custom_y_var,
                                          orient="horizontal", bg="#f5f5f5", command=lambda x: self._update_custom_position())
            self.gui.custom_y_slider.pack(side="left", fill=tk.X, expand=True, padx=5)
            tk.Label(y_slider_frame, text="下").pack(side="right", padx=5)
            
            # 初始化自定义位置
            if not hasattr(self.gui, 'custom_position'):
                self.gui.custom_position = (50, 50)
        
        # 默认隐藏自定义位置输入框
        self.gui.custom_position_frame.pack_forget()
        
        # 设置默认位置
        self._select_position(DEFAULT_CONFIG["default_position"])
    
    def _select_position(self, position):
        """选择位置"""
        # 重置所有按钮样式
        for btn_position, button in self.position_buttons.items():
            button.config(bg="#e0e0e0", fg="black")
        
        # 设置选中按钮样式（桂电蓝 #005FA5）
        if position in self.position_buttons:
            self.position_buttons[position].config(bg="#005FA5", fg="white")
        
        # 更新位置变量
        self.gui.position_var.set(position)
        self.gui.set_position(position)
        
        # 更新位置显示标签
        position_names = {
            "top-left": "左上角", "top": "顶部居中", "top-right": "右上角",
            "left": "左侧居中", "center": "居中", "right": "右侧居中",
            "bottom-left": "左下角", "bottom": "底部居中", "bottom-right": "右下角",
            "full_cover": "覆盖全图", "custom": "自定义位置"
        }
        self.position_label.config(text=f"当前位置：{position_names.get(position, position)}")
        
        # 显示/隐藏自定义位置输入框
        if position == "custom":
            self.gui.custom_position_frame.pack(pady=5, padx=10, fill=tk.X, before=self.position_label)
        else:
            self.gui.custom_position_frame.pack_forget()
    
    def _update_custom_position(self):
        """更新自定义位置坐标"""
        try:
            # 获取滑块的百分比值
            x_percent = self.gui.custom_x_var.get() if hasattr(self.gui, 'custom_x_var') else 50
            y_percent = self.gui.custom_y_var.get() if hasattr(self.gui, 'custom_y_var') else 50
            
            # 将百分比转换为实际坐标
            if self.gui.original_image:
                image_width, image_height = self.gui.original_image.size
                x = int(image_width * (x_percent / 100))
                y = int(image_height * (y_percent / 100))
                self.gui.custom_position = (x, y)
            
            # 如果当前选择的是自定义位置，则更新预览
            if hasattr(self.gui, 'watermark_position') and self.gui.watermark_position == "custom":
                self.gui.update_preview()
        except ValueError:
            # 输入非数字时忽略
            pass