import tkinter as tk


class FlipSection:
    """翻转设置部分"""
    
    def __init__(self, parent, gui):
        self.parent = parent
        self.gui = gui
        self.create_section()
    
    def create_section(self):
        """创建翻转设置部分"""
        tk.Label(self.parent, text="水印翻转", bg="#f5f5f5", font=("黑体", 12, "bold")).pack(pady=(10, 5), anchor="w", padx=10)
        
        flip_frame = tk.Frame(self.parent, bg="#f5f5f5")
        flip_frame.pack(pady=5, padx=10, fill=tk.X)
        
        # 初始化变量（如果不存在）
        if not hasattr(self.gui, 'flip_horizontal'):
            self.gui.flip_horizontal = tk.BooleanVar(value=False)
        if not hasattr(self.gui, 'flip_vertical'):
            self.gui.flip_vertical = tk.BooleanVar(value=False)
        
        # 水平翻转按钮
        self.horizontal_button = tk.Button(flip_frame, 
                                         text="水平翻转", 
                                         width=8,
                                         bg="#e0e0e0",
                                         fg="black",
                                         activebackground="#d0d0d0",
                                         activeforeground="black",
                                         command=self._toggle_horizontal)
        self.horizontal_button.pack(side="left", padx=5)
        
        # 垂直翻转按钮
        self.vertical_button = tk.Button(flip_frame, 
                                       text="垂直翻转", 
                                       width=8,
                                       bg="#e0e0e0",
                                       fg="black",
                                       activebackground="#d0d0d0",
                                       activeforeground="black",
                                       command=self._toggle_vertical)
        self.vertical_button.pack(side="left", padx=5)
        
        # 更新按钮初始状态
        self._update_button_states()
    
    def _toggle_horizontal(self):
        """切换水平翻转状态"""
        self.gui.flip_horizontal.set(not self.gui.flip_horizontal.get())
        self._update_button_states()
        self.gui.update_preview()
    
    def _toggle_vertical(self):
        """切换垂直翻转状态"""
        self.gui.flip_vertical.set(not self.gui.flip_vertical.get())
        self._update_button_states()
        self.gui.update_preview()
    
    def _update_button_states(self):
        """更新按钮状态显示"""
        # 水平翻转按钮状态
        if self.gui.flip_horizontal.get():
            self.horizontal_button.config(bg="#005FA5", fg="white")
        else:
            self.horizontal_button.config(bg="#e0e0e0", fg="black")
        
        # 垂直翻转按钮状态
        if self.gui.flip_vertical.get():
            self.vertical_button.config(bg="#005FA5", fg="white")
        else:
            self.vertical_button.config(bg="#e0e0e0", fg="black")