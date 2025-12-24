import tkinter as tk
from gui_main import WatermarkGUI


def main():
    """主程序入口"""
    root = tk.Tk()
    app = WatermarkGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
