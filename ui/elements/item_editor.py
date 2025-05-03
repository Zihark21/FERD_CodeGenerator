import customtkinter
from ui import app
from .custom_combobox import CustomCombobox
from src import config

class ItemEditor(customtkinter.CTkToplevel):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master

        self._close()
        self.title('Item Editor')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self._close)

        self.row = 0
        self.col = 0

        self._items()
        self._item_data()
        self._item_stats()
        self._item_bonus()
        self._item_buttons()

        app.set_icon(self)
        app.center_window(self)

    def _close(self):
        self.withdraw()

    def _items(self):

        def _reset():
            self.item_sel.set('')
            self.item_sel.update_text(self)

        _values = ['All']+config.item_list

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, columnspan=3, padx=5, pady=5, sticky='nsew')
        frame.grid_anchor('center')
        frame.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(frame, text='Item', fg_color='gray20', corner_radius=6).grid(sticky='ew')

        self.item_sel = CustomCombobox(frame, values=_values)
        self.item_sel.grid(pady=5, sticky='ew')

        customtkinter.CTkButton(frame, text='Reset', command=_reset).grid(columnspan=3, sticky='ew')

    def _item_data(self):

        self.row += 1

        def reset_data():

            for widget in self.item_data:
                if isinstance(widget, customtkinter.CTkEntry):
                    widget.delete(0, 'end')
                elif isinstance(widget, customtkinter.CTkOptionMenu):
                    widget.set('')
                elif isinstance(widget, customtkinter.CTkCheckBox):
                    widget.deselect()
                else:
                    continue

            for widget in self.effectiveness:
                widget.deselect()

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=5, pady=(0,5), sticky='nsew')
        frame.grid_anchor('center')
        frame.grid_columnconfigure([0,1], weight=1)

        customtkinter.CTkLabel(frame, text='Item Data', fg_color='gray20', corner_radius=6).grid(columnspan=2, sticky='ew', pady=(0,5))

        self.item_data = []
        self.effectiveness = []

        for i, data in enumerate(config.item_data):
            i += 1
            frame.grid_rowconfigure(i, weight=1)
            customtkinter.CTkLabel(frame, text=data.replace("_", " ")).grid(row=i, column=0, padx=3, pady=(0,5), sticky='ew')
            if data in ['Attack_Type', 'Rank']:
                _width = config.option_width*1.75
                opt_list = list(config.attack_type) if data == 'Attack_Type' else config.weapon_ranks
                option_menu = customtkinter.CTkOptionMenu(frame, values=opt_list, dynamic_resizing=False, width=_width)
                option_menu.grid(row=i, column=1, padx=(0,3), pady=(0,5))
                option_menu.set('')
                self.item_data.append(option_menu)
            elif data in ['Effectiveness']:
                frame2 = customtkinter.CTkFrame(frame)
                for effect in config.weapon_effectiveness:
                    checkbox = customtkinter.CTkCheckBox(frame2, text=effect, width=0)
                    checkbox.pack(pady=(0,5), anchor='w')
                    self.effectiveness.append(checkbox)
                self.item_data.append(self.effectiveness)
                frame2.grid(row=i, column=1)
            elif data in ['Unlock', 'Char_Unlock', 'Infinite', 'Brave', 'Heal']:
                checkbox = customtkinter.CTkCheckBox(frame, text=None, width=0)
                checkbox.grid(row=i, column=1, pady=(0,5), sticky='ns')
                self.item_data.append(checkbox)

        customtkinter.CTkButton(frame, text='Reset', command=reset_data).grid(columnspan=2, sticky='ew')

    def _item_stats(self):

        self.col += 1

        def reset_stats():
            entry: customtkinter.CTkEntry
            for entry in self.item_stats:
                entry.delete(0, 'end')

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=(0,5), pady=(0,5), sticky='nsew')

        customtkinter.CTkLabel(frame, text='Item Stats', fg_color='gray20', corner_radius=6).grid(columnspan=2, pady=(0,5), sticky='ew')

        self.item_stats = []

        for i, stat in enumerate(config.item_stats):
            i += 1
            frame.grid_rowconfigure(i, weight=1)
            customtkinter.CTkLabel(frame, text=stat.replace("_", " ")).grid(row=i, column=0, padx=3, pady=(0,5), sticky='ew')
            entry = customtkinter.CTkEntry(frame, justify='center', width=config.num_entry_width)
            entry.grid(row=i, column=1, padx=(0,3), pady=(0,5))
            self.item_stats.append(entry)

        customtkinter.CTkButton(frame, text='Reset', command=reset_stats).grid(columnspan=2, sticky='ew')

    def _item_bonus(self):

        self.col += 1

        def reset_bonus():
            entry: customtkinter.CTkEntry
            for entry in self.item_bonus:
                entry.delete(0, 'end')

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=(0,5), pady=(0,5), sticky='nsew')

        customtkinter.CTkLabel(frame, text='Equip Bonuses', fg_color='gray20', corner_radius=6).grid(columnspan=2, pady=(0,5), sticky='ew')

        self.item_bonus = []

        for i, bonus in enumerate(config.item_bonus):
            i += 1
            frame.grid_rowconfigure(i, weight=1)
            customtkinter.CTkLabel(frame, text=bonus.replace("_", " ")).grid(row=i, column=0, padx=3, pady=(0,5))
            entry = customtkinter.CTkEntry(frame, justify='center', width=config.num_entry_width)
            entry.grid(row=i, column=1, padx=(0,3), pady=(0,5))
            self.item_bonus.append(entry)
        
        customtkinter.CTkButton(frame, text='Reset', command=reset_bonus).grid(columnspan=2, sticky='ew')

    def _item_buttons(self):

        customtkinter.CTkButton(self, text='Generate Item Code', command=lambda: app.App.handleCode(self.root, 'item')).grid(columnspan=3, padx=5, pady=(0,5), sticky='ew')

        customtkinter.CTkButton(self, text='Close', command=self._close).grid(columnspan=3, padx=5, pady=(0,5), sticky='ew')