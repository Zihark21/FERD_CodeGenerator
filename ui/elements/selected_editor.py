import customtkinter
from ui import app
from .custom_combobox import CustomCombobox
from src import config

class SelectedEditor(customtkinter.CTkToplevel):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master

        self._close()
        self.title('Selected Editor')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self._close)

        self.row = 0
        self.col = 0

        self._selected_class()
        self._selected_stats()
        self._selected_ranks()
        self._selected_buttons()

        app.set_icon(self)
        app.center_window(self)

    def _close(self):
        self.withdraw()

    def _selected_class(self):

        def _reset():
            self.selected_class.set('')
            self.selected_class.update_text(self, open=False)

        _values = config.class_list
        _width = len(max(_values, key=len)) * 8

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, columnspan=2, padx=5, pady=5, sticky='nsew')
        frame.columnconfigure(0, weight=1)

        customtkinter.CTkLabel(frame, text='Class', fg_color='gray20', corner_radius=6).grid(sticky='ew')

        self.selected_class = CustomCombobox(frame, values=_values, width=_width)
        self.selected_class.grid(pady=5, sticky='ew')

        customtkinter.CTkButton(frame, text='Reset', command=_reset).grid(sticky='ew')

    def _selected_stats(self):

        self.row += 1
        self.col = 0

        def reset_stats():
            entry: customtkinter.CTkEntry
            for entry in self.selected_stats:
                entry.delete(0, 'end')

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=5, pady=(0,5), sticky='nsew')
        frame.columnconfigure(0, weight=1)

        customtkinter.CTkLabel(frame, text='Stats', fg_color='gray20', corner_radius=6).grid(columnspan=2, sticky='ew', pady=(0,5))

        self.selected_stats = []
        for i, stat in enumerate(config.character_stats):
            i += 1
            customtkinter.CTkLabel(frame, text=stat.replace("_", " ")).grid(row=i, column=0, padx=3, pady=(0,5))
            entry = customtkinter.CTkEntry(frame, width=config.num_entry_width, justify='center')
            entry.grid(row=i, column=1, pady=(0,5))
            self.selected_stats.append(entry)

        customtkinter.CTkButton(frame, text='Reset', command=reset_stats).grid(columnspan=2, sticky='ew')

    def _selected_ranks(self):
        
        self.col += 1

        def reset_ranks():
            option: customtkinter.CTkOptionMenu
            for option in self.selected_ranks:
                option.set('')
        
        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=(0,5), pady=(0,5), sticky='nsew')
        frame.grid_columnconfigure([0, 1], weight=1)

        customtkinter.CTkLabel(frame, text='Ranks', fg_color='gray20', corner_radius=6).grid(row=0, column=0, columnspan=2, pady=(0,5), sticky='ew')

        self.selected_ranks = []
        for i, rank in enumerate(config.character_ranks):
            i += 1
            frame.grid_rowconfigure(i, weight=1)
            customtkinter.CTkLabel(frame, text=rank.replace("_", " ")).grid(row=i, column=0, padx=3, pady=(0,5))
            entry = customtkinter.CTkOptionMenu(frame, values=config.weapon_ranks, dynamic_resizing=False, width=config.option_width)
            entry.set('')
            entry.grid(row=i, column=1, pady=(0,5))
            self.selected_ranks.append(entry)
        
        customtkinter.CTkButton(frame, text='Reset', command=reset_ranks).grid(columnspan=2, sticky='ew')

    def _selected_buttons(self):

        customtkinter.CTkButton(self, text='Generate Selected Code', command=lambda: app.App.handleCode(self.root, 'selected')).grid(columnspan=2, padx=5, pady=(0,5), sticky='ew')

        customtkinter.CTkButton(self, text='Close', command=self._close).grid(columnspan=2, padx=5, pady=(0,5), sticky='ew')