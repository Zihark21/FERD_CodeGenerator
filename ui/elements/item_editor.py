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

        def check_human_laguz(checkbox: customtkinter.CTkCheckBox, misc: str):
            if misc == 'Human' and checkbox.get():
                for cb in self.effectiveness:
                    if cb.cget('text') in ["Magic User", "Flying", "Mounted", "Armored"]:
                        cb.deselect()
                        cb.configure(state='disabled')
            elif misc == 'Human' and not checkbox.get():
                for cb in self.effectiveness:
                    if cb.cget('text') in ["Magic User", "Flying", "Mounted", "Armored"]:
                        cb.configure(state='normal')
            elif misc == 'Laguz' and checkbox.get():
                for cb in self.effectiveness:
                    if cb.cget('text') in ["Beast", "Dragon", "Bird"]:
                        cb.deselect()
                        cb.configure(state='disabled')
            elif misc == 'Laguz' and not checkbox.get():
                for cb in self.effectiveness:
                    if cb.cget('text') in ["Beast", "Dragon", "Bird"]:
                        cb.configure(state='normal')

        def _add_checkbox_frame(frame: customtkinter.CTkFrame, list: list[str], values: list[str]):

            for misc in values:
                checkbox = customtkinter.CTkCheckBox(frame, text=misc.replace('_', ' '), width=0)
                checkbox.configure(command=lambda cb=checkbox, mc=misc: check_human_laguz(cb, mc))
                checkbox.pack(padx=(5,0), pady=3, anchor='w')
                list.append(checkbox)
            self.item_data.append(list)

        def _reset_data():

            for widget in self.item_data:
                if isinstance(widget, customtkinter.CTkOptionMenu):
                    widget.set('')
                else:
                    continue

            for widget in self.effectiveness:
                widget.deselect()
                widget.configure(state='normal')

            self.item_effect.set('')

            for widget in self.misc:
                widget.deselect()

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=5, pady=(0,5), sticky='nsew', rowspan=2)
        frame.grid_anchor('center')
        frame.grid_columnconfigure([0,1], weight=1)

        customtkinter.CTkLabel(frame, text='Item Data', fg_color='gray20', corner_radius=6).grid(columnspan=2, sticky='ew', pady=(0,5))

        self.item_data = []
        self.effectiveness = []
        self.effects = []
        self.misc = []
        self.item_effect = customtkinter.StringVar(value='')

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
            elif data in ['Effectiveness', 'Misc']:
                _list = self.effectiveness if data == 'Effectiveness' else self.misc
                _values = config.weapon_effectiveness if data == 'Effectiveness' else config.weapon_misc
                eff_misc = customtkinter.CTkFrame(frame, border_color='gray30', border_width=1)
                _add_checkbox_frame(eff_misc, _list, _values)
                eff_misc.grid(row=i, column=1, sticky='ew', pady=(0,5))
            elif data in ['Effects']:
                eff = customtkinter.CTkFrame(frame, border_color='gray30', border_width=1)
                for effect in config.weapon_effects:
                    radio = customtkinter.CTkRadioButton(eff, text=effect, variable=self.item_effect, value=effect, width=0)
                    radio.bind('<Button-3>', lambda event, r=radio: r.deselect())
                    radio.pack(padx=(5,0), pady=3, anchor='w')
                    self.effects.append(radio)
                self.item_data.append(self.effects)
                eff.grid(row=i, column=1, sticky='ew', pady=(0,5))

        customtkinter.CTkButton(frame, text='Reset', command=_reset_data).grid(columnspan=2, sticky='ew')

    def _item_stats(self):

        self.col += 1

        def _reset_stats():
            entry: customtkinter.CTkEntry
            for entry in self.item_stats:
                entry.delete(0, 'end')

            for entry in self.item_bonus:
                entry.delete(0, 'end')

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=(0,5), pady=(0,5), sticky='nsew')

        customtkinter.CTkLabel(frame, text='Item Stats', fg_color='gray20', corner_radius=6).grid(columnspan=2, pady=(0,5), sticky='ew')

        self.item_stats = []
        self.item_bonus = []

        self._add_entries(frame, self.item_stats, config.item_stats)

        customtkinter.CTkButton(frame, text='Reset', command=_reset_stats).grid(columnspan=2, sticky='ew')

    def _item_bonus(self):

        self.row += 1

        def _reset_bonuses():
            entry: customtkinter.CTkEntry
            for entry in self.item_bonus:
                entry.delete(0, 'end')

        frame = customtkinter.CTkFrame(self, fg_color='gray17')
        frame.grid(row=self.row, column=self.col, padx=(0,5), pady=(0,5), sticky='nsew')

        customtkinter.CTkLabel(frame, text='Item Bonuses', fg_color='gray20', corner_radius=6).grid(columnspan=2, pady=(0,5), sticky='ew')

        self._add_entries(frame, self.item_bonus, config.item_bonus)

        customtkinter.CTkButton(frame, text='Reset', command=_reset_bonuses).grid(columnspan=2, sticky='ew')

    def _item_buttons(self):

        customtkinter.CTkButton(self, text='Generate Item Code', command=lambda: app.App.handleCode(self.root, 'item')).grid(columnspan=3, padx=5, pady=(0,5), sticky='ew')

        customtkinter.CTkButton(self, text='Close', command=self._close).grid(columnspan=3, padx=5, pady=(0,5), sticky='ew')

    @staticmethod
    def _add_entries(frame: customtkinter.CTkFrame, list: list[str], values: list[str]):
            for i, v in enumerate(values):
                i += 1
                frame.grid_rowconfigure(i, weight=1, uniform=True)
                customtkinter.CTkLabel(frame, text=v.replace("_", " ")).grid(row=i, column=1, padx=(0,3), pady=(0,5), sticky='w')
                entry = customtkinter.CTkEntry(frame, justify='center', width=config.num_entry_width)
                entry.grid(row=i, column=0, padx=3, pady=(0,5), sticky='w')
                list.append(entry)