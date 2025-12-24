import tkinter as tk
from utils import DEFAULT_CONFIG


class OpacitySection:
    """透明度设置部分"""
    
    def __init__(self, parent, gui):
        self.parent = parent
        self.gui = gui
        self.create_section()
    
    def create_section(self):
        """创建透明度设置部分"""
        tk.Label(self.parent, text="透明度", bg="#f5f5f5", font=("黑体", 12, "bold")).pack(pady=(10, 5), anchor="w", padx=10)
        
        opacity_frame = tk.Frame(self.parent, bg="#f5f5f5")
        opacity_frame.pack(pady=5, padx=10, fill=tk.X)
        
        tk.Label(opacity_frame, text="0%").pack(side="left", padx=5)
        # 初始化变量（如果不存在）
        if not hasattr(self.gui, 'opacity_var'):
            self.gui.opacity_var = tk.IntVar(value=DEFAULT_CONFIG["default_opacity"])
        opacity_slider = tk.Scale(opacity_frame, from_=0, to=100, variable=self.gui.opacity_var, 
                                 orient="horizontal", bg="#f5f5f5", command=lambda x: self.gui.update_preview())
        opacity_slider.pack(side="left", fill=tk.X, expand=True, padx=5)
        
        # 添加手动输入框
        opacity_input_frame = tk.Frame(opacity_frame, bg="#f5f5f5")
        opacity_input_frame.pack(side="left", padx=5)
        
        if not hasattr(self.gui, 'opacity_entry') or self.gui.opacity_entry is None:
            self.gui.opacity_entry = tk.Entry(opacity_input_frame, width=5, justify="center")
        
        self.gui.opacity_entry.pack(side="left", padx=2)
        self.gui.opacity_entry.delete(0, tk.END)
        self.gui.opacity_entry.insert(0, str(self.gui.opacity_var.get()))
        
        # 验证输入
        validate_cmd = (self.gui.opacity_entry.register(self.gui.validate_opacity_input), '%P')
        self.gui.opacity_entry.config(validate="key", validatecommand=validate_cmd)
        self.gui.opacity_entry.bind("<FocusOut>", self.gui.set_opacity_from_entry)
        self.gui.opacity_entry.bind("<Return>", self.gui.set_opacity_from_entry)
        
        # 添加重置按钮
        reset_opacity_btn = tk.Button(opacity_frame, text="重置", width=4, 
                                     command=lambda: self.gui.reset_opacity(), 
                                     bg="#e0e0e0", relief="flat")
        reset_opacity_btn.pack(side="right", padx=5)