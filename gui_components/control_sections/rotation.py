import tkinter as tk
from utils import DEFAULT_CONFIG


class RotationSection:
    """旋转角度设置部分"""
    
    def __init__(self, parent, gui):
        self.parent = parent
        self.gui = gui
        self.create_section()
    
    def create_section(self):
        """创建旋转角度设置部分"""
        tk.Label(self.parent, text="旋转角度", bg="#f5f5f5", font=("黑体", 12, "bold")).pack(pady=(10, 5), anchor="w", padx=10)
        
        rotation_frame = tk.Frame(self.parent, bg="#f5f5f5")
        rotation_frame.pack(pady=5, padx=10, fill=tk.X)
        
        tk.Label(rotation_frame, text="-180°").pack(side="left", padx=5)
        # 初始化变量（如果不存在）
        if not hasattr(self.gui, 'rotation_var'):
            self.gui.rotation_var = tk.IntVar(value=DEFAULT_CONFIG["default_rotation"])
        rotation_slider = tk.Scale(rotation_frame, from_=-180, to=180, variable=self.gui.rotation_var, 
                                  orient="horizontal", bg="#f5f5f5", command=lambda x: self.gui.update_preview())
        rotation_slider.pack(side="left", fill=tk.X, expand=True, padx=5)
        
        # 添加手动输入框
        rotation_input_frame = tk.Frame(rotation_frame, bg="#f5f5f5")
        rotation_input_frame.pack(side="left", padx=5)
        
        if not hasattr(self.gui, 'rotation_entry') or self.gui.rotation_entry is None:
            self.gui.rotation_entry = tk.Entry(rotation_input_frame, width=5, justify="center")
        
        self.gui.rotation_entry.pack(side="left", padx=2)
        self.gui.rotation_entry.delete(0, tk.END)
        self.gui.rotation_entry.insert(0, str(self.gui.rotation_var.get()))
        
        # 验证输入
        validate_cmd = (self.gui.rotation_entry.register(self.gui.validate_rotation_input), '%P')
        self.gui.rotation_entry.config(validate="key", validatecommand=validate_cmd)
        self.gui.rotation_entry.bind("<FocusOut>", self.gui.set_rotation_from_entry)
        self.gui.rotation_entry.bind("<Return>", self.gui.set_rotation_from_entry)
        
        # 添加重置按钮
        reset_rotation_btn = tk.Button(rotation_frame, text="重置", width=4, 
                                      command=lambda: self.gui.reset_rotation(), 
                                      bg="#e0e0e0", relief="flat")
        reset_rotation_btn.pack(side="right", padx=5)