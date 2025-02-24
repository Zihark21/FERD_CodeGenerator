import customtkinter, re
import Sources.Config as Config
import Sources.UDF as UDF
from Sources.CTkScrollableDropdown import *

class CodeGeneratorGUI:

    def __init__(self):

        # Initialize the main window
        self.root = customtkinter.CTk()
        self.root.title("Radiant Dawn Code Wizard")
        self.root.wm_attributes('-alpha', True)
        self.set_icon(self.root)

        # Set up UI components
        self.base_options()
        self.character_editor()
        self.character_items_editor()
        self.class_editor()
        self.items_editor()
        self.code_database()

        # Set the window size and position
        self.root.resizable(False, False)
        self.center_window(self.root)

    def set_icon(self, window):
        window.after(250, lambda: window.iconbitmap(Config.ICO_PATH))

    def center_window(self, window):

        # Update UI elements
        window.update()
        window.update_idletasks()

        # Get screen scaling
        scale = customtkinter.ScalingTracker.get_window_dpi_scaling(window)

        # Calculate the center position
        sw = int(window.winfo_screenwidth() * scale // 2)
        sh = int(window.winfo_screenheight() * scale // 2)

        # Get the window size
        w = window.winfo_width()
        h = window.winfo_height()

        # Calculate the position
        pos_x = int(sw - (w // 2))
        pos_y = int(sh - (h // 2))

        # Set the window geometry
        window.geometry(f'{pos_x}+{pos_y}')

    def copy_code(self, code):

        # Copy the code to the clipboard and close the output window
        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        self.output_window.destroy()

    def output_code(self, code):

        # Initialize the output window
        win_name = ' '.join([self.type, "Code"])
        self.output_window = customtkinter.CTkToplevel(self.root)
        self.output_window.title(win_name)
        self.set_icon(self.output_window)
        self.output_window.wm_attributes('-topmost', True)

        # Display the code in the output window
        output_label = customtkinter.CTkLabel(self.output_window, text=code, justify="center", wraplength=400, width=40, fg_color='grey17', corner_radius=6, padx=10, pady=10, anchor="center")
        output_label.pack(padx=10, pady=10, side="top")

        # Extract the code part from the full text
        match = re.search(r'Code:\n((?:.*\n*)+)', code)
        code_part = match.group(1).strip() if match else code

        # Add a button to copy the code to the clipboard if the code is valid
        if "Error:" not in code:
            copy_button = customtkinter.CTkButton(self.output_window, text="Copy to Clipboard", command=lambda: self.copy_code(code_part))
            copy_button.pack(pady=5)

        # Set the window size and position
        self.center_window(self.output_window)

    def output_error(self, error_message):
        
        # Initialize the output window
        self.error_window = customtkinter.CTkToplevel(self.root)
        self.error_window.title("Error")
        self.set_icon(self.error_window)
        self.error_window.wm_attributes('-topmost', True)

        # Display the error message in the output window
        error_label = customtkinter.CTkLabel(self.error_window, text=error_message, justify="center", wraplength=400, width=40, anchor="center")
        error_label.pack(padx=10, pady=10, side="top")

        # Set the window size and position
        self.center_window(self.error_window)

    def close(self, window):

        # Re-enable the button and hide the window
        window.withdraw()

    def base_options(self):

        # Define values used in this function
        option_box_width = 300
        box_frame_height = 75

        # Create function to update the buttons based on the selected controller
        def update_buttons(choice):

            # Clear previous checkboxes
            self.checkboxes = []

            # Clear previous buttons
            for item in self.button_select.winfo_children():
                item.destroy()

            # Update the buttons based on the selected controller
            if choice == "None - Always On":
                customtkinter.CTkLabel(self.button_select, text='Button Selection will appear here when a valid controller is selected.').pack()
            else:
                for i, option in enumerate(Config.KEYBINDS[choice]):
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
        self.controller = customtkinter.CTkOptionMenu(controller_select, values=list(Config.KEYBINDS), dynamic_resizing=False, width=option_box_width/2, command=update_buttons)
        self.controller.grid(row=1, column=0, padx=5, pady=5)

        # Create Version Frame
        version_select = customtkinter.CTkFrame(self.root, fg_color='gray17')
        version_select.grid(row=0, column=1, padx=5, pady=5)

        version_label = customtkinter.CTkLabel(version_select, text='Version', fg_color="gray20", corner_radius=6)
        version_label.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.version = customtkinter.CTkOptionMenu(version_select, values=Config.VER_LIST, dynamic_resizing=False, width=option_box_width)
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

        self.char_button = customtkinter.CTkButton(base_buttons, text='Character', command=lambda: self.character_window.deiconify())
        self.char_button.grid(row=0, column=0, padx=5, pady=5)

        self.class_button = customtkinter.CTkButton(base_buttons, text='Class', command=lambda: self.class_window.deiconify())
        self.class_button.grid(row=0, column=1, padx=5, pady=5)

        self.item_button = customtkinter.CTkButton(base_buttons, text='Item', command=lambda: self.item_window.deiconify())
        self.item_button.grid(row=0, column=2, padx=5, pady=5)

        # all_button = customtkinter.CTkButton(base_buttons, text='Generate All Codes')
        # all_button.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky='nsew')

        database_button = customtkinter.CTkButton(base_buttons, text='Database', command=lambda: self.database_window.deiconify())
        database_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

    def character_editor(self):

        combobox_width = 300

        # Create the character window if it doesn't exist
        self.character_window = customtkinter.CTkToplevel(self.root)
        self.character_window.withdraw()
        self.character_window.title('Character Editor')
        self.set_icon(self.character_window)
        self.character_window.protocol('WM_DELETE_WINDOW', lambda: self.close(self.character_window))

        # Character Selection

        character_select = customtkinter.CTkFrame(self.character_window, fg_color='gray17')
        character_select.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        character_select.columnconfigure(0, weight=1)

        character_label = customtkinter.CTkLabel(character_select, text='Character', fg_color='gray20', corner_radius=6)
        character_label.grid(padx=5, pady=5, sticky='nsew')

        self.character_sel = customtkinter.CTkComboBox(character_select, width=combobox_width/3)
        CTkScrollableDropdown(self.character_sel, values=['All']+Config.CHAR_LIST, autocomplete=True)
        self.character_sel.set('')
        self.character_sel.grid(padx=5, pady=5, sticky='nsew')

        character_reset = customtkinter.CTkButton(character_select, text='Reset', command=lambda: self.character_sel.set(''))
        character_reset.grid(padx=5, pady=5, sticky='nsew')

        # Character Class Selection

        character_class = customtkinter.CTkFrame(self.character_window, fg_color='gray17')
        character_class.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        character_class.columnconfigure(0, weight=1)

        class_label = customtkinter.CTkLabel(character_class, text='Class', fg_color='gray20', corner_radius=6)
        class_label.grid(padx=5, pady=5, sticky='nsew')

        self.character_class = customtkinter.CTkComboBox(character_class, width=combobox_width)
        CTkScrollableDropdown(self.character_class, values=Config.CLASS_LIST, autocomplete=True)
        self.character_class.set('')
        self.character_class.grid(padx=5, pady=5, sticky='nsew')

        character_class_reset = customtkinter.CTkButton(character_class, text='Reset', command=lambda: self.character_class.set(''))
        character_class_reset.grid(padx=5, pady=5, sticky='nsew')

        # Character Stats Entries

        def reset_stats():
            for entry in self.character_stats:
                entry.delete(0, 'end')

        character_stats = customtkinter.CTkFrame(self.character_window, fg_color='gray17')
        character_stats.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        character_stats.columnconfigure(0, weight=1)

        stats_label = customtkinter.CTkLabel(character_stats, text='Stats', fg_color='gray20', corner_radius=6)
        stats_label.grid(padx=5, pady=5, columnspan=2, sticky='nsew')

        self.character_stats = []
        for i, stat in enumerate(Config.CHAR_STATS):
            i +=1
            entry_label = customtkinter.CTkLabel(character_stats, text=stat.replace("_", " "))
            entry_label.grid(row=i, column=0, padx=5, pady=5)
            entry = customtkinter.CTkEntry(character_stats, width=40, justify='center')
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.character_stats.append(entry)

        character_stats_reset = customtkinter.CTkButton(character_stats, text='Reset', command=reset_stats)
        character_stats_reset.grid(padx=5, pady=5, columnspan=2, sticky='nsew')

        # Character Ranks Selections

        def reset_ranks():
            for sel in self.character_ranks:
                sel.set('')
        
        character_ranks = customtkinter.CTkFrame(self.character_window, fg_color='gray17')
        character_ranks.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        character_ranks.grid_columnconfigure([0, 1], weight=1)

        ranks_header = customtkinter.CTkLabel(character_ranks, text='Ranks', fg_color='gray20', corner_radius=6)
        ranks_header.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        self.character_ranks = []
        for i, rank in enumerate(Config.CHAR_RANKS):
            i += 1
            character_ranks.grid_rowconfigure(i, weight=1)
            entry_label = customtkinter.CTkLabel(character_ranks, text=rank.replace("_", " "))
            entry_label.grid(row=i, column=0, padx=5, pady=5)
            entry = customtkinter.CTkOptionMenu(character_ranks, values=['']+Config.RANKS, dynamic_resizing=False, width=80)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.character_ranks.append(entry)
        
        character_ranks_reset = customtkinter.CTkButton(character_ranks, text='Reset', command=reset_ranks)
        character_ranks_reset.grid(padx=5, pady=5, columnspan=2, sticky='nsew')

        # Buttons

        character_items = customtkinter.CTkButton(self.character_window, text='Items', command=lambda: self.character_items_window.deiconify())
        character_items.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        char_button = customtkinter.CTkButton(self.character_window, text='Generate Character Code', command=lambda: self.code_creation(0))
        char_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        close_button = customtkinter.CTkButton(self.character_window, text='Close', command=lambda: self.close(self.character_window))
        close_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        self.character_window.resizable(False, False)
        self.center_window(self.character_window)

    def character_items_editor(self):

        def reset_inventory():
            for row in self.character_inventory:
                for widget in row:
                    if isinstance(widget, customtkinter.CTkEntry):
                        widget.delete(0, 'end')
                    elif isinstance(widget, customtkinter.CTkCheckBox):
                        widget.deselect()
                    else:
                        widget.set('')

        self.character_items_window = customtkinter.CTkToplevel(self.root)
        self.character_items_window.withdraw()
        self.character_items_window.title('Character Items Editor')
        self.set_icon(self.character_items_window)
        self.character_items_window.grid_anchor('center')
        self.character_items_window.protocol('WM_DELETE_WINDOW', lambda: self.close(self.character_items_window))
        
        for i in range(len(Config.CHAR_INV)):
            self.character_items_window.columnconfigure(i, weight=1)
        
        self.character_inventory = []

        for r in range(9):
            inv_row = []
            
            for c, title in enumerate(Config.CHAR_INV):
                self.character_items_window.grid_columnconfigure(c, weight=1)
                if r == 0:
                    header = customtkinter.CTkLabel(self.character_items_window, text=title, fg_color='gray17', corner_radius=6)
                    header.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
                elif r == 8:
                    reset_button = customtkinter.CTkButton(self.character_items_window, text='Reset', command=reset_inventory)
                    reset_button.grid(row=r, column=0, columnspan=len(Config.CHAR_INV), padx=5, pady=5, sticky='nsew')

                    close_button = customtkinter.CTkButton(self.character_items_window, text='Close', command=lambda: self.close(self.character_items_window))
                    close_button.grid(row=r+1, column=0, columnspan=len(Config.CHAR_INV), padx=5, pady=5, sticky='nsew')
                    break
                elif title == 'Item':
                    combobox = customtkinter.CTkComboBox(self.character_items_window)
                    CTkScrollableDropdown(combobox, values=Config.ITEM_LIST, autocomplete=True)
                    combobox.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
                    inv_row.append(combobox)
                    combobox.set('')
                elif title in ['Uses', 'Forge Name', 'Mt', 'Hit', 'Crit']:
                    w = 120 if title == 'Forge Name' else 40
                    entry = customtkinter.CTkEntry(self.character_items_window, width=w)
                    entry.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
                    inv_row.append(entry)
                elif title in ['Wt', 'Forged', 'Blessed']:
                    checkbox = customtkinter.CTkCheckBox(self.character_items_window, text=None, width=0)
                    checkbox.grid(row=r, column=c, padx=5, pady=5, sticky='ns')
                    inv_row.append(checkbox)
                else:
                    raise "Error in character inventory."

            self.character_inventory.append(inv_row)
    
        self.character_items_window.resizable(False, False)
        self.center_window(self.character_items_window)

    def class_editor(self):

        combobox_width = 300

        self.class_window = customtkinter.CTkToplevel(self.root)
        self.class_window.withdraw()
        self.class_window.title('Class Editor')
        self.set_icon(self.class_window)
        self.class_window.protocol('WM_DELETE_WINDOW', lambda: self.close(self.class_window))

        # Class Selection

        class_select = customtkinter.CTkFrame(self.class_window, fg_color='gray17')
        class_select.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        class_label = customtkinter.CTkLabel(class_select, text='Class', fg_color='gray20', corner_radius=6)
        class_label.grid(padx=5, pady=5, sticky='nsew')

        self.class_sel = customtkinter.CTkComboBox(class_select, width=combobox_width)
        CTkScrollableDropdown(self.class_sel, values=['All']+Config.CLASS_LIST, autocomplete=True)
        self.class_sel.set('')
        self.class_sel.grid(padx=5, pady=5, sticky='nsew')

        class_reset = customtkinter.CTkButton(class_select, text='Reset', command=lambda: self.class_sel.set(''))
        class_reset.grid(padx=5, pady=5, sticky='nsew')

        # Class Promote Selection

        class_promote_select = customtkinter.CTkFrame(self.class_window, fg_color='gray17')
        class_promote_select.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        class_promote_select.columnconfigure(0, weight=1)

        class_promote_label = customtkinter.CTkLabel(class_promote_select, text='Promote', fg_color='gray20', corner_radius=6)
        class_promote_label.grid(padx=5, pady=5, sticky='nsew')

        self.class_promote = customtkinter.CTkComboBox(class_promote_select)
        CTkScrollableDropdown(self.class_promote, values=Config.CLASS_LIST, autocomplete=True, width=400)
        self.class_promote.set('')
        self.class_promote.grid(padx=5, pady=5, sticky='nsew')

        class_promote_reset = customtkinter.CTkButton(class_promote_select, text='Reset', command=lambda: self.class_promote.set(''))
        class_promote_reset.grid(padx=5, pady=5, sticky='nsew')

        # Class Stats Entries

        def reset_class_stats():
            for entry in self.class_stats:
                entry.delete(0, 'end')
        
        self.class_stats = []

        class_stats_entries = customtkinter.CTkFrame(self.class_window, fg_color='gray17')
        class_stats_entries.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        class_stats_entries.grid_anchor('n')
        class_stats_entries.grid_columnconfigure([0,1], weight=1)

        class_stats_label = customtkinter.CTkLabel(class_stats_entries, text='Stats', fg_color='gray20', corner_radius=6)
        class_stats_label.grid(padx=5, pady=5, columnspan=2, sticky='nsew')

        for i, stat in enumerate(Config.CLASS_STATS):
            i += 1
            class_stats_entries.grid_rowconfigure(i, weight=1)
            entry_label = customtkinter.CTkLabel(class_stats_entries, text=stat.replace("_", " "))
            entry_label.grid(row=i, column=0, padx=5, pady=5)
            entry = customtkinter.CTkEntry(class_stats_entries, width=40, justify='center')
            entry.grid(row=i, column=1, padx=5, pady=5)

            self.class_stats.append(entry)

        class_stats_reset = customtkinter.CTkButton(class_stats_entries, text='Reset', command=reset_class_stats)
        class_stats_reset.grid(padx=5, pady=5, columnspan=2, sticky='nsew')

        # Class Ranks Selections

        def reset_class_ranks(reset_list):
            for sel in reset_list:
                sel.set('')
        
        self.class_min_ranks = []
        self.class_max_ranks = []

        class_ranks_selections = customtkinter.CTkFrame(self.class_window, fg_color='gray17')
        class_ranks_selections.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        class_ranks_selections.grid_anchor('center')
        class_ranks_selections.columnconfigure([0,1,2], weight=1)

        class_ranks_label = customtkinter.CTkLabel(class_ranks_selections, text='Ranks', fg_color='gray20', corner_radius=6)
        class_ranks_label.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        class_ranks_min_header = customtkinter.CTkLabel(class_ranks_selections, text='Min Ranks', fg_color='gray20', corner_radius=6)
        class_ranks_min_header.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        class_ranks_max_header = customtkinter.CTkLabel(class_ranks_selections, text='Max Ranks', fg_color='gray20', corner_radius=6)
        class_ranks_max_header.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

        for i, rank in enumerate(Config.CHAR_RANKS):
            i += 1
            entry_label = customtkinter.CTkLabel(class_ranks_selections, text=rank.replace("_", " "))
            entry_label.grid(row=i, column=0, padx=5, pady=5)

            min_entry = customtkinter.CTkOptionMenu(class_ranks_selections, values=['']+Config.RANKS, dynamic_resizing=False, width=80)
            min_entry.grid(row=i, column=1, padx=5, pady=5)
            self.class_min_ranks.append(min_entry)

            max_entry = customtkinter.CTkOptionMenu(class_ranks_selections, values=['']+Config.RANKS, dynamic_resizing=False, width=80)
            max_entry.grid(row=i, column=2, padx=5, pady=5)
            self.class_max_ranks.append(max_entry)

        class_ranks_reset_all = customtkinter.CTkButton(class_ranks_selections, text='Reset All', command=lambda: reset_class_ranks(self.class_min_ranks + self.class_max_ranks))
        class_ranks_reset_all.grid(row=len(self.class_max_ranks)+1, column=0, padx=5, pady=5, sticky='nsew')

        class_min_ranks_reset = customtkinter.CTkButton(class_ranks_selections, text='Reset Min', command=lambda: reset_class_ranks(self.class_min_ranks))
        class_min_ranks_reset.grid(row=len(self.class_min_ranks)+1, column=1, padx=5, pady=5, sticky='nsew')

        class_max_ranks_reset = customtkinter.CTkButton(class_ranks_selections, text='Reset Max', command=lambda: reset_class_ranks(self.class_max_ranks))
        class_max_ranks_reset.grid(row=len(self.class_max_ranks)+1, column=2, padx=5, pady=5, sticky='nsew')

        # Buttons

        class_button = customtkinter.CTkButton(self.class_window, text='Generate Character Code', command=lambda: self.code_creation(1))
        class_button.grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        close_button = customtkinter.CTkButton(self.class_window, text='Close', command=lambda: self.close(self.class_window))
        close_button.grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        self.class_window.resizable(False, False)
        self.center_window(self.class_window)

    def items_editor(self):
        
        self.item_window = customtkinter.CTkToplevel(self.root)
        self.item_window.withdraw()
        self.item_window.title('Item Editor')
        self.set_icon(self.item_window)
        self.item_window.protocol('WM_DELETE_WINDOW', lambda: self.close(self.item_window))

        # Item Select

        item_select = customtkinter.CTkFrame(self.item_window, fg_color='gray17')
        item_select.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
        item_select.grid_anchor('center')
        item_select.grid_columnconfigure(0, weight=1)

        item_label = customtkinter.CTkLabel(item_select, text='Item', fg_color='gray20', corner_radius=6)
        item_label.grid(padx=5, pady=5, sticky='nsew')

        self.item_sel = customtkinter.CTkComboBox(item_select)
        CTkScrollableDropdown(self.item_sel, values=['All']+Config.ITEM_LIST, autocomplete=True, width=300)
        self.item_sel.set('')
        self.item_sel.grid(padx=5, pady=5, sticky='nsew')

        item_reset = customtkinter.CTkButton(item_select, text='Reset', command=lambda: self.item_sel.set(''))
        item_reset.grid(columnspan=3, padx=5, pady=5, sticky='nsew')

        # Item Data

        def reset_data():
            for entry in self.item_data:
                if isinstance(entry, customtkinter.CTkEntry):
                    entry.delete(0, 'end')
                elif isinstance(entry, customtkinter.CTkOptionMenu):
                    entry.set('')
                elif isinstance(entry, customtkinter.CTkCheckBox):
                    entry.deselect()

        item_data_frame = customtkinter.CTkFrame(self.item_window, fg_color='gray17')
        item_data_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        item_data_frame.grid_anchor('center')
        item_data_frame.grid_columnconfigure([0,1], weight=1)

        customtkinter.CTkLabel(item_data_frame, text='Item Data', fg_color='gray20', corner_radius=6).grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        item_data_width = 80
        self.item_data = []
        for i, data in enumerate(Config.ITEM_DATA):
            i += 1
            item_data_frame.grid_rowconfigure(i, weight=1)
            customtkinter.CTkLabel(item_data_frame, text=data.replace("_", " ")).grid(row=i, column=0, padx=5, pady=5, sticky='nsew')
            if data in ['Attack_Type', 'Weapon_Rank']:
                opt_list = ['ATK', 'MAG'] if data == 'Attack_Type' else Config.RANKS
                option_menu = customtkinter.CTkOptionMenu(item_data_frame, values=opt_list, dynamic_resizing=False, width=item_data_width)
                option_menu.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
                option_menu.set('')
                self.item_data.append(option_menu)
            elif data in ['EXP_Gain']:
                entry = customtkinter.CTkEntry(item_data_frame, width=item_data_width, justify='center')
                entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
                self.item_data.append(entry)
            elif data in ['Unlock', 'Char_Unlock', 'Infinite', 'Brave', 'Heal']:
                checkbox = customtkinter.CTkCheckBox(item_data_frame, text=None, width=0)
                checkbox.grid(row=i, column=1, padx=5, pady=5, sticky='ns')
                self.item_data.append(checkbox)

        item_data_reset = customtkinter.CTkButton(item_data_frame, text='Reset', command=reset_data)
        item_data_reset.grid(columnspan=2, padx=5, pady=5, sticky='ew')

        # Item Stats

        item_stat_width = 40
        self.item_stats = []

        item_stats_frame = customtkinter.CTkFrame(self.item_window, fg_color='gray17')
        item_stats_frame.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        item_stats_frame.grid_anchor('center')
        item_stats_frame.grid_columnconfigure([0,1], weight=1)

        customtkinter.CTkLabel(item_stats_frame, text='Item Stats', fg_color='gray20', corner_radius=6).grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        for i, stat in enumerate(Config.ITEM_STATS):
            i += 1
            item_stats_frame.grid_rowconfigure(i, weight=1)
            customtkinter.CTkLabel(item_stats_frame, text=stat.replace("_", " ")).grid(row=i, column=0, padx=5, pady=5, sticky='nsew')
            entry = customtkinter.CTkEntry(item_stats_frame, width=item_stat_width, justify='center')
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            self.item_stats.append(entry)

        item_stat_reset = customtkinter.CTkButton(item_stats_frame, text='Reset', command=lambda: [entry.delete(0, 'end') for entry in self.item_stats])
        item_stat_reset.grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        # Item Equip Bonuses

        item_equip_width = 40

        item_equip_frame = customtkinter.CTkFrame(self.item_window, fg_color='gray17')
        item_equip_frame.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

        customtkinter.CTkLabel(item_equip_frame, text='Equip Bonuses', fg_color='gray20', corner_radius=6).grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        self.item_equip = []
        for i, bonus in enumerate(Config.ITEM_EQUIP_BONUS):
            i += 1
            customtkinter.CTkLabel(item_equip_frame, text=bonus.replace("_", " ")).grid(row=i, column=0, padx=5, pady=5, sticky='nsew')
            entry = customtkinter.CTkEntry(item_equip_frame, width=item_equip_width, justify='center')
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='nsew')
            self.item_equip.append(entry)
        
        item_equip_reset = customtkinter.CTkButton(item_equip_frame, text='Reset', command=lambda: [entry.delete(0, 'end') for entry in self.item_equip])
        item_equip_reset.grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        # Buttons

        item_button = customtkinter.CTkButton(self.item_window, text='Generate Item Code', command=lambda: self.code_creation(2))
        item_button.grid(columnspan=3, padx=5, pady=5, sticky='nsew')

        item_close = customtkinter.CTkButton(self.item_window, text='Close', command=lambda: self.close(self.item_window))
        item_close.grid(columnspan=3, padx=5, pady=5, sticky='nsew')

        self.item_window.resizable(False, False)
        self.center_window(self.item_window)

    def code_database(self):
        
        # Initialize the database window
        self.database_window = customtkinter.CTkToplevel(self.root)
        self.database_window.withdraw()
        self.database_window.title("Code Database")
        self.set_icon(self.database_window)
        self.database_window.wm_attributes('-topmost', True)
        self.database_window.protocol('WM_DELETE_WINDOW', lambda: self.close(self.database_window))

        num_per_row = 5

        # Create add buttons for each code
        for i, code in enumerate(Config.CODE_DATABASE):
            self.database_window.grid_columnconfigure(i, weight=1)
            code_button = customtkinter.CTkButton(self.database_window, text=code, command=lambda cd=code: self.generate_database_code(cd))
            code_button.grid(row=i // num_per_row, column=i % num_per_row, padx=5, pady=5, sticky='nsew')

        database_close = customtkinter.CTkButton(self.database_window, text='Close', command=lambda: self.close(self.database_window))
        database_close.grid(columnspan=num_per_row, padx=5, pady=5, sticky='nsew')

        # Set the window size and position
        self.database_window.resizable(False, False)
        self.center_window(self.database_window)

    def append_keycode(self, code):
        key_code = UDF.get_keybind_code(self._get_keybinds_data())
        output = '\n'.join([key_code, code, 'E0000000 80008000'])
        self.output_code(output)

    def code_verification(self, code):
        if 'Error:' in code:
            self.output_code(code)
        else:
            self.append_keycode(code)

    def code_creation(self, option):
        UDF.set_version(self.version.get())

        if option == 0 or option == 'All':
            self._create_char_code()
        if option == 1 or option == 'All':
            self._create_class_code()
        if option == 2 or option == 'All':
            self._create_item_code()

    def _create_char_code(self):
        self.type = 'Character'
        character_data = self._get_character_data()
        char_code = UDF.get_char_code(character_data)
        self.code_verification(char_code)

    def _create_class_code(self):
        self.type = 'Class'
        class_data = self._get_class_data()
        class_code = UDF.get_class_code(class_data)
        self.code_verification(class_code)

    def _create_item_code(self):
        self.type = 'Item'
        item_data = self._get_item_data()
        item_code = UDF.get_item_code(item_data)
        self.code_verification(item_code)

    def _get_character_data(self):

        def get_inventory():
            inv_list = ['item', 'uses', 'forge_name', 'mt', 'hit', 'crit', 'wt', 'forged', 'blessed']
            inv_data = []
            for row in self.character_inventory:
                row_data = {}
                if row:
                    for widget, header in zip(row, inv_list):
                        row_data[header] = widget.get()
                    inv_data.append(row_data)
            
            return inv_data

        return {
            "character": self.character_sel.get(),
            "class": self.character_class.get(),
            "stats": [stat.get() for stat in self.character_stats],
            "ranks": [rank.get() for rank in self.character_ranks],
            "items": get_inventory()
        }

    def _get_class_data(self):
        return {
            "class": self.class_sel.get(),
            "promote": self.class_promote.get(),
            "ranks": [min.get() for min in self.class_min_ranks] + [max.get() for max in self.class_max_ranks],
            "stats": [stat.get() for stat in self.class_stats]
        }

    def _get_item_data(self):

        def get_item_attrs():
            item_data = {}
            for data, field in zip(self.item_data, Config.ITEM_DATA):
                item_data[field] = data.get()
            
            return item_data

        return {
            "item": self.item_sel.get(),
            "data": get_item_attrs(),
            "stats": [stat.get() for stat in self.item_stats],
            "bonuses": [bonus.get() for bonus in self.item_equip]
        }

    def _get_keybinds_data(self):
        return {
            "controller": self.controller.get(),
            "keys": [key.get() for key in self.checkboxes],
        }

    def generate_database_code(self, sel_code):
        self.type = 'Database'
        version = UDF.set_version(self.version.get())
        desc = Config.CODE_DATABASE[sel_code]['DESC']
        key_code = UDF.get_keybind_code(self._get_keybinds_data())
        code = Config.CODE_DATABASE[sel_code][version]
        output = '\n'.join([desc, key_code, code, 'E0000000 80008000'])
        self.output_code(output)