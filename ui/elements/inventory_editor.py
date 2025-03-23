import customtkinter
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

        def _reset_inventory():
            for row in self.character_inventory:
                for widget in row:
                    if isinstance(widget, customtkinter.CTkEntry):
                        widget.delete(0, 'end')
                    elif isinstance(widget, customtkinter.CTkCheckBox):
                        widget.deselect()
                    elif isinstance(widget, customtkinter.CTkComboBox):
                        widget.set('')
                        widget.update_text(self, open=False)
                    else:
                        continue

        _values = config.item_list
        _width = len(max(_values, key=len)) * 10

        for i in range(len(headers)):
            self.columnconfigure(i, weight=1)
        
        self.character_inventory = []

        for r in range(9):
            inv_row = []
            
            for c, title in enumerate(headers):
                self.grid_columnconfigure(c, weight=1)
                if r == 0:
                    customtkinter.CTkLabel(self, text=title, fg_color='gray17', corner_radius=6).grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
                elif r == 8:
                    customtkinter.CTkButton(self, text='Reset', command=_reset_inventory).grid(row=r, column=0, columnspan=len(headers), padx=5, pady=5, sticky='nsew')

                    customtkinter.CTkButton(self, text='Close', command=self._close).grid(row=r+1, column=0, columnspan=len(headers), padx=5, pady=5, sticky='nsew')
                    break
                elif title == 'Item':
                    combobox = CustomCombobox(self, values=_values, width=_width)
                    combobox.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
                    inv_row.append(combobox)
                elif title in ['Uses', 'Forge Name', 'Mt', 'Hit', 'Crit']:
                    _width = config.text_entry_width if title == 'Forge Name' else config.num_entry_width
                    entry = customtkinter.CTkEntry(self, width=_width)
                    entry.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
                    inv_row.append(entry)
                elif title in ['Wt', 'Forged', 'Blessed']:
                    checkbox = customtkinter.CTkCheckBox(self, text=None, width=0)
                    checkbox.grid(row=r, column=c, padx=5, pady=5, sticky='ns')
                    inv_row.append(checkbox)
                else:
                    raise "Error in character inventory."

            self.character_inventory.append(inv_row)