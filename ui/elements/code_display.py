import customtkinter, re
from ui import app

class CodeDisplay(customtkinter.CTkToplevel):

    def __init__(self, master=None, title='', message=''):
        super().__init__(master)
        self.root = master

        win_name = ' '.join([title, "Code"])

        self.title(win_name)
        self.resizable(False, False)
        self.wm_attributes('-topmost', True)

        message = self._unknown_code(message)
        self._output_code(message)

        app.set_icon(self)
        app.center_window(self)
        self.lift()
        self.focus_force()

    def _unknown_code(self, message: str):

        if "Unknown" in message:
            message = 'This code is unknown for this version of the game.\nPlease request it from me on Discord.'

        return message

    def _output_code(self, message):

        customtkinter.CTkLabel(self, text=message, justify="center", wraplength=400, width=40, fg_color='grey17', corner_radius=6, padx=5, pady=5, anchor="center").pack(padx=5, pady=5, side="top")

        match = re.search(r'Code:\n((?:.*\n*)+)', message)
        code_part = match.group(1).strip() if match else message

        if "Error:" not in message:
            customtkinter.CTkButton(self, text="Copy to Clipboard", command=lambda: self._copy_code(code_part)).pack(padx=5, pady=(0,5), fill='x')

    def _copy_code(self, code):

        self.clipboard_clear()
        self.clipboard_append(code)
        self.destroy()