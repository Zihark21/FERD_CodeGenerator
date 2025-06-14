import customtkinter
from src import config, handler
from .elements import base
from .elements import character_editor
from .elements import inventory_editor
from .elements import class_editor
from .elements import item_editor
from .elements import selected_editor
from .elements import database
from .elements import help
from .elements import code_display

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("dark")

        self.title("Radiant Dawn Code Wizard")
        self.wm_attributes('-alpha', True)
        self.resizable(False, False)
        
        self.base = base.Base(master=self)
        self.character_editor = character_editor.CharacterEditor(master=self)
        self.inventory_editor = inventory_editor.InventoryEditor(master=self)
        self.class_editor = class_editor.ClassEditor(master=self)
        self.item_editor = item_editor.ItemEditor(master=self)
        self.selected_editor = selected_editor.SelectedEditor(master=self)
        self.database = database.Database(master=self)
        self.help = help.Help(master=self)

        set_icon(self)
        center_window(self)

    def _show(self, option):

        window: customtkinter.CTkToplevel

        if option == 'character':
            window = self.character_editor
        elif option == 'inventory':
            window = self.inventory_editor
        elif option == 'class':
            window = self.class_editor
        elif option == 'item':
            window = self.item_editor
        elif option == 'selected':
            window = self.selected_editor
        elif option == 'database':
            window = self.database
        elif option == 'help':
            window = self.help

        window.deiconify()
        window.lift()
        window.focus_force()

    def handleCode(self, option: str, code_name: str = None):

        base_data = self.handleBase()
        title = option.title()
        
        if option == 'character':
            data = self.handleCharacter()
            code = handler.code_handler(base_data, data, 'character')
        elif option == 'class':
            data = self.handleClass()
            code = handler.code_handler(base_data, data, 'class')
        elif option == 'item':
            data = self.handleItem()
            code = handler.code_handler(base_data, data, 'item')
        elif option == 'selected':
            data = self.handleSelected()
            code = handler.code_handler(base_data, data, 'selected')
        elif option == 'database':
            data = self.handleDatabase(code_name)
            code = handler.code_handler(base_data, data, 'database')
        else:
            pass

        if code is None:
            title = 'Error'
            code = 'No code returned'

        code_display.CodeDisplay(self, title, code)

    def handleBase(self):

        return {
            "controller": self.base.controller.get(),
            "version": self.base.version.get(),
            "difficulty": self.base.difficulty.get(),
            "keys": [key.get() for key in self.base.checkboxes],
        }

    def handleCharacter(self):

        def get_inventory():

            inv_data = []
            for row in self.inventory_editor.character_inventory:
                row_data = {}
                if row:
                    for widget, header in zip(row, config.character_inventory):
                        if isinstance(widget, customtkinter.CTkEntry | customtkinter.CTkComboBox | customtkinter.CTkCheckBox):
                            row_data[header] = widget.get()
                        elif isinstance(widget, customtkinter.CTkButton):
                            color = widget.cget('fg_color')
                            if color != '#808080':
                                row_data[header] = color
                            else:
                                row_data[header] = ''
                    inv_data.append(row_data)
            
            return inv_data

        return {
            "character": self.character_editor.character_sel.get(),
            "class": self.character_editor.character_class.get(),
            # "model": self.character_editor.character_model.get(),
            # "support": self.character_editor.character_support.get(),
            "stats": [stat.get() for stat in self.character_editor.character_stats],
            "ranks": [rank.get() for rank in self.character_editor.character_ranks],
            "items": get_inventory()
        }
    
    def handleClass(self):

        return {
            "class": self.class_editor.class_sel.get(),
            "promote": self.class_editor.class_promote.get(),
            "ranks": [min.get() for min in self.class_editor.class_min_ranks] + [max.get() for max in self.class_editor.class_max_ranks],
            "stats": [stat.get() for stat in self.class_editor.class_stats]
        }
    
    def handleItem(self):

        def get_item_attrs():
            item_data = {}
            for data, field in zip(self.item_editor.item_data, config.item_data):
                if field in ['Attack_Type', 'Rank']:
                    item_data[field] = data.get()
                elif field == 'Effects':
                    item_data[field] = self.item_editor.item_effect.get()
                else:
                    item_data[field] = [entry.get() for entry in data]
            
            return item_data

        return {
            "item": self.item_editor.item_sel.get(),
            "data": get_item_attrs(),
            "stats": [stat.get() for stat in self.item_editor.item_stats],
            "bonuses": [bonus.get() for bonus in self.item_editor.item_bonus]
        }

    def handleSelected(self):

        # def get_inventory():

        #     inv_data = []
        #     for row in self.inventory_editor.character_inventory:
        #         row_data = {}
        #         if row:
        #             for widget, header in zip(row, config.character_inventory):
        #                 row_data[header] = widget.get()
        #             inv_data.append(row_data)
            
        #     return inv_data

        return {
            "class": self.selected_editor.selected_class.get(),
            "stats": [stat.get() for stat in self.selected_editor.selected_stats],
            "ranks": [rank.get() for rank in self.selected_editor.selected_ranks],
            # "items": get_inventory()
        }

    def handleDatabase(self, sel_code):

        return config.code_database[sel_code]
    
    def handleDiscord(self):

        title='Discord'
        message='https://discord.gg/AjSmXddnXk'

        code_display.CodeDisplay(master=self, title=title, message=message)

def set_icon(window: customtkinter.CTkToplevel):

    window.after(250, lambda: window.iconbitmap(config.icon_path))

def center_window(window: customtkinter.CTkToplevel):

    window.update()
    window.update_idletasks()

    scale = customtkinter.ScalingTracker.get_window_dpi_scaling(window)

    sw = int(window.winfo_screenwidth() * scale // 2)
    sh = int(window.winfo_screenheight() * scale // 2)

    w = window.winfo_reqwidth()
    h = window.winfo_reqheight()

    pos_x = int(sw - (w // 2))
    pos_y = int(sh - (h // 2))

    window.geometry(f'{pos_x}+{pos_y}')