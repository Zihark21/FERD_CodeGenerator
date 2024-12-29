import customtkinter, re, os, sys
from tkinter import ttk
from Sources.Config import CHAR_LIST, CLASS_LIST, ITEM_LIST, DESC, CHAR_STATS, CHAR_RANKS, CLASS_STATS, ITEM_STATS, ITEM_DATA, ITEM_BONUS, CODE_DATABASE, VER_LIST, RANKS, CHAR_INV
from Sources.UDF import get_char_code, get_class_code, get_item_code, get_keybind_code, set_version

class CodeGeneratorGUI:

    def __init__(self):
        self.root = customtkinter.CTk()
        self.root.title("FE:RD Code Creator")
        self.root.wm_attributes('-alpha', True)

        base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.abspath(".")
        self.icon_path = os.path.join(base_path, "Assets", "FE-RD.ico")
        self.set_icon(self.root)

        self.set_variables()
        self.base_options()
        self.root.resizable(False, False)
        self.center_window(self.root)

    def set_icon(self, window):
        window.after(250, lambda: window.iconbitmap(self.icon_path))

    def set_variables(self):
        self.keybinds = {
            "None - Always On": "",
            "Classic": [
                "Left", "Right", "Up", "Down", "A", "B", "X", "Y", "ZL", "ZR", "L", "R", "+", "-"
            ],
            "GameCube": [
                "Left", "Right", "Up", "Down", "A", "B", "X", "Y", "Z", "L", "R", "Start"
            ],
        }

        self.default_button_color = customtkinter.CTkButton(None).cget('fg_color')

    def center_window(self, window):
        window.update()
        window.update_idletasks()

        scale = customtkinter.ScalingTracker.get_window_dpi_scaling(window)

        sw = int(window.winfo_screenwidth() * scale // 2)
        sh = int(window.winfo_screenheight() * scale // 2)

        w = window.winfo_width()
        h = window.winfo_height()

        pos_x = int(sw - (w // 2))
        pos_y = int(sh - (h // 2))

        window.geometry(f'{pos_x}+{pos_y}')

    def copy_and_close(self, code, message_window):
        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        message_window.destroy()

    def output_code(self, code):
        win_name = ' '.join([self.type, "Code"])
        message_window = customtkinter.CTkToplevel(self.root)
        message_window.title(win_name)

        output_label = customtkinter.CTkLabel(message_window, text=code, justify="center", wraplength=400, width=40, anchor="center")
        output_label.pack(padx=10, pady=10, side="top")

        match = re.search(r'Code:\n((?:.*\n*)+)', code)
        code_part = match.group(1).strip() if match else code

        if "Error:" not in code:
            copy_button = customtkinter.CTkButton(message_window, text="Copy to Clipboard", command=lambda: self.copy_and_close(code_part, message_window))
            copy_button.pack(pady=5)

        self.center_window(message_window)

    def selector(self, choice, button, selection):
            
        button.configure(state='disabled')

        def update_selection(selection, window, update):
            update.configure(text=selection)
            button.configure(state='normal', fg_color='purple')
            window.destroy()
            
        if choice == 0:
            choice = CHAR_LIST
            title = 'Character'
        elif choice == 1:
            choice = CLASS_LIST
            title = 'Class'
        elif choice == 2:
            choice = ITEM_LIST
            title = 'Item'

        # Create a scrollable list in a Toplevel window
        selector_window = customtkinter.CTkToplevel(self.root)
        selector_window.title(f"Select {title}")
        self.set_icon(selector_window)
        selector_window.wm_attributes('-topmost', True)
        selector_window.geometry('300x600')
        selector_window.protocol('WM_DELETE_WINDOW', lambda: self.close(button, selector_window))

        # Add a scrollable frame
        scrollable_frame = customtkinter.CTkScrollableFrame(selector_window)
        scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add buttons for each character in CHAR_LIST
        for item in choice:
            customtkinter.CTkButton(scrollable_frame, text=item, command=lambda sel=item: update_selection(sel, selector_window, selection)).pack(pady=2)

        selector_window.resizable(False, False)
        self.center_window(selector_window)
        selector_window.after(100, lambda: selector_window.wm_attributes('-topmost', False))

    def close(self, button, window):
        button.configure(state='normal')
        window.withdraw()

    def base_options(self):

        box_frame_height = 75

        def update_buttons(choice):

            self.checkboxes = []

            for item in self.button_select.winfo_children():
                item.destroy()

            if choice == "None - Always On":
                customtkinter.CTkLabel(self.button_select, text='Button Selection will appear here when a valid controller is selected.').pack()
            else:
                for i, option in enumerate(self.keybinds[choice]):
                    c = i // 4
                    r = i - (c*4)
                    var = customtkinter.BooleanVar()
                    checkbox = customtkinter.CTkCheckBox(self.button_select, text=option, variable=var)
                    checkbox.grid(row=r, column=c, pady=5)
                    self.checkboxes.append(var)
            
                for col in range(c):
                    self.button_select.grid_columnconfigure(col, weight=1)

        # Create Controller Frame
        controller_select = customtkinter.CTkFrame(self.root, fg_color='gray17')
        controller_select.grid(row=0, column=0, padx=5, pady=5)

        controller_label = customtkinter.CTkLabel(controller_select, text='Controller', fg_color="gray20", corner_radius=6)
        controller_label.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.controller = customtkinter.CTkOptionMenu(controller_select, values=list(self.keybinds.keys()), dynamic_resizing=False, width=175, command=update_buttons)
        self.controller.grid(row=1, column=0, padx=5, pady=5)

        # Create Version Frame
        version_select = customtkinter.CTkFrame(self.root, fg_color='gray17')
        version_select.grid(row=0, column=1, padx=5, pady=5)

        version_label = customtkinter.CTkLabel(version_select, text='Version', fg_color="gray20", corner_radius=6)
        version_label.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.version = customtkinter.CTkOptionMenu(version_select, values=VER_LIST, dynamic_resizing=False, width=275)
        self.version.set("NTSC 1.01")
        self.version.grid(row=1, column=0, padx=5, pady=5)

        # Create Checkbox Frame
        self.checkboxes = []
        self.button_select = customtkinter.CTkFrame(self.root, height=box_frame_height, fg_color='gray17')
        customtkinter.CTkLabel(self.button_select, text='Button Selection will appear here when a valid controller is selected.').pack()
        self.button_select.grid(row=1, column=0, padx=5, pady=5, columnspan=2, sticky='nsew')
        self.button_select.grid_anchor(anchor='center')

        # Create Buttons
        base_buttons = customtkinter.CTkFrame(self.root)
        base_buttons.grid(row=3, column=0, padx=5, pady=5, columnspan=2, sticky='nsew')
        base_buttons.grid_anchor('center')

        self.char_button = customtkinter.CTkButton(base_buttons, text='Character', command=self.character_window)
        self.char_button.grid(row=0, column=0, padx=5, pady=5)

        class_button = customtkinter.CTkButton(base_buttons, text='Class')
        class_button.grid(row=0, column=1, padx=5, pady=5)

        item_button = customtkinter.CTkButton(base_buttons, text='Item')
        item_button.grid(row=0, column=2, padx=5, pady=5)

        all_button = customtkinter.CTkButton(base_buttons, text='Generate All Codes')
        all_button.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky='nsew')

        database_button = customtkinter.CTkButton(base_buttons, text='Database')
        database_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

    def character_window(self):

        self.char_button.configure(state='disabled')

        try:
            self.cw.deiconify()
        except:
            self.cw = customtkinter.CTkToplevel(self.root)
            self.cw.title('Character')
            self.set_icon(self.cw)
            self.cw.wm_attributes('-topmost', True)
            self.cw.protocol('WM_DELETE_WINDOW', lambda: self.close(self.char_button, self.cw))

            # Character
            def reset_character():
                self.character.configure(text="Charater")
                character_button.configure(fg_color=self.default_button_color)
            
            character_select = customtkinter.CTkFrame(self.cw, fg_color='gray17')
            character_select.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
            character_select.columnconfigure(0, weight=1)

            self.character = customtkinter.CTkLabel(character_select, text="Charater", fg_color='gray20', corner_radius=6)
            self.character.grid(padx=5, pady=5, sticky='nsew')

            character_button = customtkinter.CTkButton(character_select, text='Select Character', command=lambda: self.selector(0, character_button, self.character))
            character_button.grid(padx=5, pady=5, sticky='nsew')

            character_reset = customtkinter.CTkButton(character_select, text='Reset', command=reset_character)
            character_reset.grid(padx=5, pady=5, sticky='nsew')

            # Character Class
            def reset_class():
                self.character_class.configure(text="Class")
                character_class_button.configure(fg_color=self.default_button_color)

            character_class = customtkinter.CTkFrame(self.cw, fg_color='gray17')
            character_class.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
            character_class.columnconfigure(0, weight=1)

            self.character_class = customtkinter.CTkLabel(character_class, text="Class", fg_color='gray20', corner_radius=6)
            self.character_class.grid(padx=5, pady=5, sticky='nsew')

            character_class_button = customtkinter.CTkButton(character_class, text='Select Class', command=lambda: self.selector(1, character_class_button, self.character_class))
            character_class_button.grid(padx=5, pady=5, sticky='nsew')

            character_class_reset = customtkinter.CTkButton(character_class, text='Reset', command=reset_class)
            character_class_reset.grid(padx=5, pady=5, sticky='nsew')

            # Character Stats
            def reset_stats():
                for entry in self.character_stats:
                    entry.delete(0, 'end')

            character_stats = customtkinter.CTkFrame(self.cw, fg_color='gray17')
            character_stats.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
            character_stats.columnconfigure([0, 1], weight=1)

            stat_header = customtkinter.CTkLabel(character_stats, text='Stats', fg_color='gray20', corner_radius=6)
            stat_header.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

            self.character_stats = []
            for i, stat in enumerate(CHAR_STATS):
                entry_label = customtkinter.CTkLabel(character_stats, text=stat.replace("_", " "))
                entry_label.grid(row=i+1, column=0, padx=5, pady=5)
                entry = customtkinter.CTkEntry(character_stats, width=40)
                entry.grid(row=i+1, column=1, padx=5, pady=5)
                self.character_stats.append(entry)

            character_stats_reset = customtkinter.CTkButton(character_stats, text='Reset', command=reset_stats)
            character_stats_reset.grid(padx=5, pady=5, columnspan=2, sticky='nsew')

            # Character Ranks
            def reset_ranks():
                for sel in self.character_ranks:
                    sel.set('')
            
            character_ranks = customtkinter.CTkFrame(self.cw, fg_color='gray17')
            character_ranks.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
            character_ranks.columnconfigure([0, 1], weight=1)

            ranks_header = customtkinter.CTkLabel(character_ranks, text='Ranks', fg_color='gray20', corner_radius=6)
            ranks_header.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

            self.character_ranks = []
            for i, rank in enumerate(CHAR_RANKS):
                entry_label = customtkinter.CTkLabel(character_ranks, text=rank.replace("_", " "))
                entry_label.grid(row=i+1, column=0, padx=5, pady=5)
                entry = customtkinter.CTkOptionMenu(character_ranks, values=RANKS, dynamic_resizing=False, width=80)
                entry.grid(row=i+1, column=1, padx=5, pady=5)
                self.character_ranks.append(entry)
            
            character_ranks_reset = customtkinter.CTkButton(character_ranks, text='Reset', command=reset_ranks)
            character_ranks_reset.grid(padx=5, pady=5, columnspan=2, sticky='nsew')

            # Buttons
            self.character_items = customtkinter.CTkButton(self.cw, text='Items', command=self.character_items_window)
            self.character_items.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

            char_button = customtkinter.CTkButton(self.cw, text='Generate Character Code')
            char_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

            close_button = customtkinter.CTkButton(self.cw, text='Close', command=lambda: self.close(self.char_button, self.cw))
            close_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

            self.cw.resizable(False, False)
            self.center_window(self.cw)
            self.cw.after(100, lambda: self.cw.wm_attributes('-topmost', False))

    def character_items_window(self):

        self.character_items.configure(state='disabled')

        def reset_inventory():
            for row in self.character_inventory:
                for widget in row:
                    if isinstance(widget, customtkinter.CTkEntry):
                        # Clear text from entry widgets
                        widget.delete(0, 'end')
                    elif isinstance(widget, customtkinter.CTkButton):
                        # Reset button text and color
                        widget.configure(text='Select Item', fg_color=self.default_button_color)
                    elif isinstance(widget, customtkinter.CTkCheckBox):
                        # Uncheck the checkbox
                        widget.deselect()

        try:
            self.ciw.deiconify()
        except:
            self.ciw = customtkinter.CTkToplevel(self.root)
            self.ciw.title('Character Items')
            self.set_icon(self.ciw)
            self.ciw.wm_attributes('-topmost', True)
            self.ciw.grid_anchor('center')
            self.ciw.columnconfigure([0,1,2,3,4,5,6], weight=1)
            self.cw.protocol('WM_DELETE_WINDOW', lambda: self.close(self.character_items, self.ciw))

            self.character_inventory = []
            for r in range(9):
                inv_row = []
                
                for c, title in enumerate(CHAR_INV):
                    if r == 0:
                        header = customtkinter.CTkLabel(self.ciw, text=title, fg_color='gray17', corner_radius=6)
                        header.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
                    elif r == 8:
                        reset_button = customtkinter.CTkButton(self.ciw, text='Reset', command=reset_inventory)
                        reset_button.grid(row=r, column=0, columnspan=len(CHAR_INV), padx=5, pady=5, sticky='nsew')

                        close_button = customtkinter.CTkButton(self.ciw, text='Close', command=lambda: self.close(self.character_items, self.ciw))
                        close_button.grid(row=r+1, column=0, columnspan=len(CHAR_INV), padx=5, pady=5, sticky='nsew')
                        break
                    elif title == 'Item':
                        item_button = customtkinter.CTkButton(self.ciw, text='Select Item')
                        item_button.configure(command=lambda btn=item_button: self.selector(2, btn, btn))
                        item_button.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
                        inv_row.append(item_button)
                    elif title in ['Uses', 'Forge Name', 'Mt', 'Hit', 'Crit']:
                        w = 120 if title == 'Forge Name' else 40
                        entry = customtkinter.CTkEntry(self.ciw, width=w)
                        entry.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
                        inv_row.append(entry)
                    elif title in ['Wt', 'Forged', 'Blessed']:
                        checkbox = customtkinter.CTkCheckBox(self.ciw, text=None, width=0)
                        checkbox.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
                        inv_row.append(checkbox)
                    else:
                        raise "Error in character inventory."

                self.character_inventory.append(inv_row)
        
            self.ciw.resizable(False, False)
            self.center_window(self.ciw)
            self.ciw.after(100, lambda: self.ciw.wm_attributes('-topmost', False))