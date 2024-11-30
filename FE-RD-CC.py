import tkinter as tk
from Assets.CodeGenUI import CodeGeneratorGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeGeneratorGUI(root)
    root.mainloop()