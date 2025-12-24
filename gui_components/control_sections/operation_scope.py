import tkinter as tk


class OperationScopeSection:
    """操作范围选择部分"""
    
    def __init__(self, parent, gui):
        self.parent = parent
        self.gui = gui
        # self.create_section()
    
    def create_section(self):
        """创建操作范围选择部分"""
        tk.Label(self.parent, text="操作范围", bg="#f5f5f5", font=("黑体", 12, "bold")).pack(pady=(10, 5))
        
        # 初始化变量（如果不存在）
        if not hasattr(self.gui, 'operation_scope'):
            self.gui.operation_scope = tk.StringVar(value="single")
        
        operation_scope_frame = tk.Frame(self.parent, bg="#f5f5f5")
        operation_scope_frame.pack(pady=5, padx=10, fill=tk.X)
        
        tk.Radiobutton(operation_scope_frame, text="当前图片", variable=self.gui.operation_scope, value="single", 
                       bg="#f5f5f5").pack(side="left", padx=5)
        tk.Radiobutton(operation_scope_frame, text="所有图片", variable=self.gui.operation_scope, value="all", 
                       bg="#f5f5f5").pack(side="left", padx=5)