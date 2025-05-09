import customtkinter
from tkinter import colorchooser
from ui import app
from .custom_combobox import CustomCombobox
from src import config

class InventoryEditor(customtkinter.CTkToplevel):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master

        self._close()
        self.title('Inventory Editor')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self._close)

        inventory_headers = config.character_inventory
        self._inventory(inventory_headers)

        app.set_icon(self)
        app.center_window(self)
        
    def _close(self):
        self.withdraw()

    def _inventory(self, headers):

        frame = customtkinter.CTkFrame(self, fg_color='gray17', bg_color='transparent')
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        def _reset_inventory():
            for row in self.character_inventory:
                for widget in row:
                    if isinstance(widget, customtkinter.CTkEntry):
                        widget.delete(0, 'end')
                    elif isinstance(widget, customtkinter.CTkCheckBox):
                        widget.deselect()
                    elif isinstance(widget, customtkinter.CTkComboBox | CustomCombobox):
                        widget.set('')
                        widget.update_text(self, open=False)
                    elif isinstance(widget, customtkinter.CTkButton):
                        widget.configure(fg_color='#808080')
                    else:
                        continue

        def _choose_color(button: customtkinter.CTkButton):
            color = colorchooser.askcolor(parent=self)[1]
            if color:
                button.configure(fg_color=color)
                return color

        _values = config.item_list
        _width = len(max(_values, key=len)) * 10

        for i in range(len(headers)):
            self.columnconfigure(i, weight=1)
        
        self.character_inventory = []

        for r in range(9):
            inv_row = []

            for c, title in enumerate(headers):

                if r == 0:
                    _pady=0
                else:
                    _pady=(5,0)

                if c == 0:
                    _padx=0
                else:
                    _padx=(5,0)

                self.grid_columnconfigure(c, weight=1)
                if r == 0:
                    customtkinter.CTkLabel(frame, text=title, fg_color='gray20', corner_radius=6).grid(row=r, column=c, padx=_padx, pady=_pady, sticky='nsew')
                elif r == 8:
                    customtkinter.CTkButton(frame, text='Reset', command=_reset_inventory).grid(row=r, column=0, columnspan=len(headers), padx=_padx, pady=_pady, sticky='nsew')

                    customtkinter.CTkButton(frame, text='Close', command=self._close).grid(row=r+1, column=0, columnspan=len(headers), padx=_padx, pady=_pady, sticky='nsew')
                    break
                elif title == 'Item':
                    combobox = CustomCombobox(frame, values=_values, width=_width)
                    combobox.grid(row=r, column=c, padx=_padx, pady=_pady, sticky='nsew')
                    inv_row.append(combobox)
                elif title in ['Uses', 'Forge Name', 'Mt', 'Hit', 'Crit']:
                    _width = config.text_entry_width if title == 'Forge Name' else config.num_entry_width
                    entry = customtkinter.CTkEntry(frame, width=_width)
                    entry.grid(row=r, column=c, padx=_padx, pady=_pady, sticky='nsew')
                    inv_row.append(entry)
                elif title in ['Weightless', 'Forged', 'Blessed']:
                    checkbox = customtkinter.CTkCheckBox(frame, text=None, width=0)
                    checkbox.grid(row=r, column=c, padx=_padx, pady=_pady, sticky='ns')
                    inv_row.append(checkbox)
                elif title in ['Color']:
                    color_button = customtkinter.CTkButton(frame, width=50, fg_color='#808080', text=None)
                    color_button.configure(command=lambda btn=color_button: _choose_color(btn))
                    color_button.grid(row=r, column=c, padx=_padx, pady=_pady, sticky='nsew')
                    inv_row.append(color_button)
                else:
                    raise "Error in character inventory."

            self.character_inventory.append(inv_row)