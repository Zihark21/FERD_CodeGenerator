import customtkinter
from ui import app
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
        # self._character_model()
        # self._character_support()
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
            self.character_sel.configure(values=_values)

        _values = ['All']+config.character_list
        _width = len(max(_values, key=len)) * 10

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(0, weight=1)

        customtkinter.CTkLabel(frame, text='Character', fg_color='gray20', corner_radius=6).grid(padx=5, pady=5, sticky='nsew')

        self.character_sel = customtkinter.CTkComboBox(frame, values=_values, width=_width)
        self.character_sel.bind("<KeyRelease>", lambda event: app.update_text(event, self.character_sel, _values))
        self.character_sel.set('')
        self.character_sel.grid(padx=5, pady=5, sticky='nsew')

        customtkinter.CTkButton(frame, text='Reset', command=_reset).grid(padx=5, pady=5, sticky='nsew')

    def _character_class(self):

        def _reset():
            self.character_class.set('')
            self.character_class.configure(values=_values)

        self.col += 1

        _values = config.class_list
        _width = len(max(_values, key=len)) * 8

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(0, weight=1)

        customtkinter.CTkLabel(frame, text='Class', fg_color='gray20', corner_radius=6).grid(padx=5, pady=5, sticky='nsew')

        self.character_class = customtkinter.CTkComboBox(frame, values=_values, width=_width)
        self.character_class.bind("<KeyRelease>", lambda event: app.update_text(event, self.character_class, _values))
        self.character_class.set('')
        self.character_class.grid(padx=5, pady=5, sticky='nsew')

        customtkinter.CTkButton(frame, text='Reset', command=_reset).grid(padx=5, pady=5, sticky='nsew')

    def _character_model(self):

        def _reset():
            self.character_model.set('')
            self.character_model.configure(values=_values)

        self.row += 1
        self.col = 0

        _values = config.character_model_list
        _width = len(max(_values, key=len)) * 10

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(0, weight=1)

        customtkinter.CTkLabel(frame, text='Model', fg_color='gray20', corner_radius=6).grid(padx=5, pady=5, sticky='nsew')

        self.character_model = customtkinter.CTkComboBox(frame, values=_values, width=_width)
        self.character_model.bind("<KeyRelease>", lambda event: app.update_text(event, self.character_model, _values))
        self.character_model.set('')
        self.character_model.grid(padx=5, pady=5, sticky='nsew')

        customtkinter.CTkButton(frame, text='Reset', command=_reset).grid(padx=5, pady=5, sticky='nsew')

    def _character_support(self):

        def _reset():
            self.character_support.set('')
            self.character_support.configure(values=_values)

        self.col += 1

        _values = config.character_list
        _width = len(max(_values, key=len)) * 10

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(0, weight=1)

        customtkinter.CTkLabel(frame, text='Support', fg_color='gray20', corner_radius=6).grid(padx=5, pady=5, sticky='nsew')

        self.character_support = customtkinter.CTkComboBox(frame, values=_values, width=_width)
        self.character_support.bind("<KeyRelease>", lambda event: app.update_text(event, self.character_support, _values))
        self.character_support.set('')
        self.character_support.grid(padx=5, pady=5, sticky='nsew')

        customtkinter.CTkButton(frame, text='Reset', command=_reset).grid(padx=5, pady=5, sticky='nsew')

    def _character_stats(self):

        self.row += 1
        self.col = 0

        def reset_stats():
            entry: customtkinter.CTkEntry
            for entry in self.character_stats:
                entry.delete(0, 'end')

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(0, weight=1)

        customtkinter.CTkLabel(frame, text='Stats', fg_color='gray20', corner_radius=6).grid(padx=5, pady=5, columnspan=2, sticky='nsew')

        self.character_stats = []
        for i, stat in enumerate(config.character_stats):
            i +=1
            customtkinter.CTkLabel(frame, text=stat.replace("_", " ")).grid(row=i, column=0, padx=5, pady=5)
            entry = customtkinter.CTkEntry(frame, width=config.num_entry_width, justify='center')
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.character_stats.append(entry)

        customtkinter.CTkButton(frame, text='Reset', command=reset_stats).grid(padx=5, pady=5, columnspan=2, sticky='nsew')

    def _character_ranks(self):
        
        self.col += 1

        def reset_ranks():
            option: customtkinter.CTkOptionMenu
            for option in self.character_ranks:
                option.set('')
        
        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=5, pady=5, sticky='nsew')
        frame.grid_columnconfigure([0, 1], weight=1)

        customtkinter.CTkLabel(frame, text='Ranks', fg_color='gray20', corner_radius=6).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        self.character_ranks = []
        for i, rank in enumerate(config.character_ranks):
            i += 1
            frame.grid_rowconfigure(i, weight=1)
            customtkinter.CTkLabel(frame, text=rank.replace("_", " ")).grid(row=i, column=0, padx=5, pady=5)
            entry = customtkinter.CTkOptionMenu(frame, values=config.weapon_ranks, dynamic_resizing=False, width=config.option_width)
            entry.set('')
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.character_ranks.append(entry)
        
        customtkinter.CTkButton(frame, text='Reset', command=reset_ranks).grid(padx=5, pady=5, columnspan=2, sticky='nsew')

    def _character_buttons(self):

        customtkinter.CTkButton(self, text='Items', command=lambda: app.App._show(self.root, 'inventory')).grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        customtkinter.CTkButton(self, text='Generate Character Code', command=lambda: app.App.handleCode(self.root, 'character')).grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        customtkinter.CTkButton(self, text='Close', command=self._close).grid(columnspan=2, padx=5, pady=5, sticky='nsew')