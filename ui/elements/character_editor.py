import customtkinter
from ui import app
from .custom_combobox import CustomCombobox
from src import config

class CharacterEditor(customtkinter.CTkToplevel):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master

        self._close()
        self.title('Character Editor')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self._close)

        self.row = 0
        self.col = 0

        self._character()
        self._character_class()
        self._character_stats()
        self._character_ranks()
        self._character_buttons()

        app.set_icon(self)
        app.center_window(self)

    def _close(self):
        self.withdraw()

    def _character(self):

        def _reset():
            self.character_sel.set('')
            self.character_sel.update_text(self)

        _values = ['All']+config.character_list
        _width = len(max(_values, key=len)) * 10

        frame = customtkinter.CTkFrame(self, fg_color='gray17', bg_color='transparent')
        frame.grid(row=self.row, column=self.col, sticky='nsew', padx=5, pady=5)
        frame.columnconfigure(0, weight=1)

        customtkinter.CTkLabel(frame, text='Character', fg_color='gray20', corner_radius=6).grid(sticky='nsew')

        self.character_sel = CustomCombobox(frame, values=_values, width=_width)
        self.character_sel.grid(sticky='nsew', pady=5)

        customtkinter.CTkButton(frame, text='Reset', command=_reset).grid(sticky='nsew')

    def _character_class(self):

        def _reset():
            self.character_class.set('')
            self.character_class.update_text(self, open=False)

        self.col += 1

        _values = config.class_list
        _width = len(max(_values, key=len)) * 8

        frame = customtkinter.CTkFrame(self, fg_color='gray17', bg_color='transparent')
        frame.grid(row=self.row, column=self.col, sticky='nsew', padx=(0,5), pady=5)
        frame.columnconfigure(0, weight=1)

        customtkinter.CTkLabel(frame, text='Class', fg_color='gray20', corner_radius=6).grid(sticky='nsew')

        self.character_class = CustomCombobox(frame, values=_values, width=_width)
        self.character_class.grid(pady=5, sticky='nsew')

        customtkinter.CTkButton(frame, text='Reset', command=_reset).grid(sticky='nsew')

    def _character_stats(self):

        self.row += 1
        self.col = 0

        def reset_stats():
            entry: customtkinter.CTkEntry
            for entry in self.character_stats:
                entry.delete(0, 'end')

        frame = customtkinter.CTkFrame(self, fg_color='gray17', bg_color='transparent')
        frame.grid(row=self.row, column=self.col, sticky='nsew', padx=5, pady=(0,5))
        frame.grid_columnconfigure([0, 1], weight=1, uniform="equal")

        customtkinter.CTkLabel(frame, text='Stats', fg_color='gray20', corner_radius=6).grid(columnspan=2, sticky='ew', pady=(0,5))

        self.character_stats = []
        for i, stat in enumerate(config.character_stats):
            i +=1
            customtkinter.CTkLabel(frame, text=stat.replace("_", " ")).grid(row=i, column=0, padx=3, pady=(0,5))
            entry = customtkinter.CTkEntry(frame, width=config.num_entry_width, justify='center')
            entry.grid(row=i, column=1, pady=(0,5))
            self.character_stats.append(entry)

        customtkinter.CTkButton(frame, text='Reset', command=reset_stats).grid(columnspan=2, sticky='ew')

    def _character_ranks(self):
        
        self.col += 1

        def reset_ranks():
            option: customtkinter.CTkOptionMenu
            for option in self.character_ranks:
                option.set('')
        
        frame = customtkinter.CTkFrame(self, fg_color='gray17', bg_color='transparent')
        frame.grid(row=self.row, column=self.col, sticky='nsew', padx=(0,5), pady=(0,5))
        frame.grid_columnconfigure([0, 1], weight=1, uniform="equal")

        customtkinter.CTkLabel(frame, text='Ranks', fg_color='gray20', corner_radius=6).grid(columnspan=2, sticky='ew', pady=(0,5))

        self.character_ranks = []
        for i, rank in enumerate(config.character_ranks):
            i += 1
            frame.grid_rowconfigure(i, weight=1)
            customtkinter.CTkLabel(frame, text=rank.replace("_", " ")).grid(row=i, column=0, padx=3, pady=(0,5))
            entry = customtkinter.CTkOptionMenu(frame, values=config.weapon_ranks, dynamic_resizing=False, width=config.option_width)
            entry.set('')
            entry.grid(row=i, column=1, pady=(0,5))
            self.character_ranks.append(entry)
        
        customtkinter.CTkButton(frame, text='Reset', command=reset_ranks).grid(columnspan=2, sticky='ew')

    def _character_buttons(self):

        customtkinter.CTkButton(self, text='Items', command=lambda: app.App._show(self.root, 'inventory')).grid(columnspan=2, padx=5, pady=(0,5), sticky='nsew')

        customtkinter.CTkButton(self, text='Generate Character Code', command=lambda: app.App.handleCode(self.root, 'character')).grid(columnspan=2, padx=5, pady=(0,5), sticky='nsew')

        customtkinter.CTkButton(self, text='Close', command=self._close).grid(columnspan=2, padx=5, pady=(0,5), sticky='nsew')