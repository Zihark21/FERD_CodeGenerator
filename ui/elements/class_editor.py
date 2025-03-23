import customtkinter
from ui import app
from .custom_combobox import CustomCombobox
from src import config

class ClassEditor(customtkinter.CTkToplevel):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master

        self._close()
        self.title('Class Editor')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self._close)

        self.row = 0
        self.col = 0

        self._class()
        self._class_promote()
        self._class_stats()
        self._class_ranks()
        self._class_buttons()

        app.set_icon(self)
        app.center_window(self)

    def _close(self):
        self.withdraw()

    def _class(self):

        def _reset():
            self.class_sel.set('')
            self.class_sel.update_text(self)

        _values = ['All']+config.class_list
        _width = len(max(_values, key=len)) * 8

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=5, pady=5, sticky='nsew')

        customtkinter.CTkLabel(frame, text='Class', fg_color='gray20', corner_radius=6).grid(padx=5, pady=5, sticky='nsew')

        self.class_sel = CustomCombobox(frame, values=_values, width=_width)
        self.class_sel.grid(padx=5, pady=5, sticky='nsew')

        customtkinter.CTkButton(frame, text='Reset', command=_reset).grid(padx=5, pady=5, sticky='nsew')

    def _class_promote(self):

        def _reset():
            self.class_promote.set('')
            self.class_promote.update_text(self, open=False)

        self.col += 1

        _values = config.class_list
        _width = len(max(_values, key=len)) * 8

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(0, weight=1)

        customtkinter.CTkLabel(frame, text='Promote', fg_color='gray20', corner_radius=6).grid(padx=5, pady=5, sticky='nsew')

        self.class_promote = CustomCombobox(frame, values=_values, width=_width)
        self.class_promote.grid(padx=5, pady=5, sticky='nsew')

        customtkinter.CTkButton(frame, text='Reset', command=_reset).grid(padx=5, pady=5, sticky='nsew')

    def _class_stats(self):

        self.row += 1
        self.col = 0

        def reset_class_stats():
            entry: customtkinter.CTkEntry
            for entry in self.class_stats:
                entry.delete(0, 'end')
        
        self.class_stats = []

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=5, pady=5, sticky='nsew')
        frame.grid_anchor('n')
        frame.grid_columnconfigure([0,1], weight=1)

        customtkinter.CTkLabel(frame, text='Stats', fg_color='gray20', corner_radius=6).grid(padx=5, pady=5, columnspan=2, sticky='nsew')

        for i, stat in enumerate(config.class_stats):
            i += 1
            frame.grid_rowconfigure(i, weight=1)
            customtkinter.CTkLabel(frame, text=stat.replace("_", " ")).grid(row=i, column=0, padx=5, pady=5)
            entry = customtkinter.CTkEntry(frame, width=config.num_entry_width, justify='center')
            entry.grid(row=i, column=1, padx=5, pady=5)

            self.class_stats.append(entry)

        customtkinter.CTkButton(frame, text='Reset', command=reset_class_stats).grid(padx=5, pady=5, columnspan=2, sticky='nsew')

    def _class_ranks(self):

        self.col += 1

        def reset_class_ranks(reset_list):
            option: customtkinter.CTkOptionMenu
            for option in reset_list:
                option.set('')
        
        self.class_min_ranks = []
        self.class_max_ranks = []

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=5, pady=5, sticky='nsew')
        frame.grid_anchor('center')
        frame.columnconfigure([0,1,2], weight=1)

        customtkinter.CTkLabel(frame, text='Ranks', fg_color='gray20', corner_radius=6).grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        customtkinter.CTkLabel(frame, text='Min Ranks', fg_color='gray20', corner_radius=6).grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        customtkinter.CTkLabel(frame, text='Max Ranks', fg_color='gray20', corner_radius=6).grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

        for i, rank in enumerate(config.character_ranks):
            i += 1
            customtkinter.CTkLabel(frame, text=rank.replace("_", " ")).grid(row=i, column=0, padx=5, pady=5)

            min_entry = customtkinter.CTkOptionMenu(frame, values=config.weapon_ranks, dynamic_resizing=False, width=config.option_width)
            min_entry.set('')
            min_entry.grid(row=i, column=1, padx=5, pady=5)
            self.class_min_ranks.append(min_entry)

            max_entry = customtkinter.CTkOptionMenu(frame, values=config.weapon_ranks, dynamic_resizing=False, width=config.option_width)
            max_entry.set('')
            max_entry.grid(row=i, column=2, padx=5, pady=5)
            self.class_max_ranks.append(max_entry)

        customtkinter.CTkButton(frame, text='Reset All', command=lambda: reset_class_ranks(self.class_min_ranks + self.class_max_ranks)).grid(row=len(self.class_max_ranks)+1, column=0, padx=5, pady=5, sticky='nsew')

        customtkinter.CTkButton(frame, text='Reset Min', command=lambda: reset_class_ranks(self.class_min_ranks)).grid(row=len(self.class_min_ranks)+1, column=1, padx=5, pady=5, sticky='nsew')

        customtkinter.CTkButton(frame, text='Reset Max', command=lambda: reset_class_ranks(self.class_max_ranks)).grid(row=len(self.class_max_ranks)+1, column=2, padx=5, pady=5, sticky='nsew')

    def _class_buttons(self):

        customtkinter.CTkButton(self, text='Generate Character Code', command=lambda: app.App.handleCode(self.root, 'class')).grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        customtkinter.CTkButton(self, text='Close', command=self._close).grid(columnspan=2, padx=5, pady=5, sticky='nsew')