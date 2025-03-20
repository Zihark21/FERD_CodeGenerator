import customtkinter
from ui import app
from src import config

class Help(customtkinter.CTkToplevel):
      
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master

        self._close()
        self.title('Help')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self._close)

        width = 400
        height = 500

        self._help(width)

        app.set_icon(self)
        self.geometry(f'{width}x{height}')
        app.center_window(self)

    def _close(self):
        self.withdraw()

    def _help(self, width):

        customtkinter.CTkOptionMenu(self, values=list(config.help), command=self.get_help_data).pack(padx=10, pady=10, fill='x')

        frame = customtkinter.CTkScrollableFrame(self)
        frame.pack(padx=10, pady=(0,10), expand=True, fill='both')

        self.help_details = customtkinter.CTkLabel(frame, text=config.help['App'], wraplength=width*0.85, justify='left')
        self.help_details.pack(padx=10, pady=(0,10), expand=True, fill='both')

    def get_help_data(self, opt):
        self.help_details.configure(text=config.help[opt])
