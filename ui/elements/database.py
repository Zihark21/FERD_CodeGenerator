import customtkinter
from ui import app
from src import config

class Database(customtkinter.CTkToplevel):
      
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master

        self._close()
        self.title('Code Database')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self._close)

        self._database()

        app.set_icon(self)
        app.center_window(self)

    def _close(self):
        self.withdraw()

    def _database(self):

        num_per_row = 5

        for i, code in enumerate(config.code_database):
            self.grid_columnconfigure(i, weight=1)
            customtkinter.CTkButton(self, text=code, command=lambda cd=code: app.App.handleCode(self.root, 'database', cd)).grid(row=i // num_per_row, column=i % num_per_row, padx=5, pady=5, sticky='nsew')

        customtkinter.CTkButton(self, text='Close', command=self._close).grid(columnspan=num_per_row, padx=5, pady=5, sticky='nsew')
