import re, ctypes
import tkinter as tk
from tkinter import ttk
import src.Config as Config
import src.UDF as UDF

class CodeGeneratorGUI:

    def __init__(self):

        ctypes.windll.shcore.SetProcessDpiAwareness(True)

        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Radiant Dawn Code Wizard")
        self.set_dark_mode()
        self.root.attributes('-topmost', True)
        self.set_icon(self.root)

        # Set up UI components
        self.base_options()
        self.character_editor()
        self.character_items_editor()
        self.class_editor()
        self.items_editor()
        self.code_database()
        self.help_window()

        # Set the window size and position
        self.root.resizable(False, False)
        self.center_window(self.root)

    def set_dark_mode(self):
        self.bg_color = 'grey20'
        self.fg_color = 'white'
        
        self.app_font = ("Figtree", 12)
        self.root.option_add("*Font", self.app_font)


        self.root.configure(bg=self.bg_color)

        style = ttk.Style()
        # style.theme_use("clam")

        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        style.configure("TFrame", background=self.bg_color)
        style.configure("TCheckbutton", background=self.bg_color, foreground=self.fg_color)
        style.configure("TButton", background=self.bg_color, font=self.app_font)
        style.configure("TCombobox", background=self.bg_color)

    def set_icon(self, window):
        window.after(250, lambda: window.iconbitmap(Config.ICO_PATH))

    def get_screen_info(self):
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()  # Enable DPI awareness
        screen_width = user32.GetSystemMetrics(0)  # Width
        screen_height = user32.GetSystemMetrics(1)  # Height
        
        # Get scaling factor
        hdc = ctypes.windll.gdi32.CreateDCW("DISPLAY", None, None, None)
        dpi_x = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
        dpi_y = ctypes.windll.gdi32.GetDeviceCaps(hdc, 90)  # LOGPIXELSY
        ctypes.windll.gdi32.DeleteDC(hdc)
        
        scaling_factor = dpi_x / 96  # Standard DPI is 96

        return {
            "width": screen_width,
            "height": screen_height,
            "scaling_factor": scaling_factor,
            "dpi_x": dpi_x,
            "dpi_y": dpi_y
        }

    def center_window(self, window):

        # Get screen elements
        screen_info = self.get_screen_info()

        # Update UI elements
        window.update()
        window.update_idletasks()

        # Get screen scaling
        scale = screen_info["scaling_factor"]

        # Calculate the center position
        sw = int(screen_info['width'] // 2)
        sh = int(screen_info['height'] // 2)

        # Get the window size
        w = window.winfo_width()
        h = window.winfo_height()

        # Ensure width and height are properly retrieved
        if w == 1 or h == 1:
            w = window.winfo_reqwidth()
            h = window.winfo_reqheight()

        # Calculate the position
        pos_x = int(sw - (w // 2))
        pos_y = int(sh - (h // 2))

        # Corrected format: "WIDTHxHEIGHT+X+Y"
        window.geometry(f"{w}x{h}+{pos_x}+{pos_y}")

    def copy_code(self, code):

        # Copy the code to the clipboard and close the output window
        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        self.output_window.destroy()

    def output_code(self, code):

        text_width = 30
        text_height_mod = 5 if 'Info' in code else 1
        text_height = str(code).count('\n') + text_height_mod

        # Initialize the output window
        win_name = ' '.join([self.type, "Code"])
        self.output_window = tk.Toplevel(self.root, background=self.bg_color)
        self.output_window.title(win_name)
        self.output_window.resizable(False, False)
        self.set_icon(self.output_window)
        self.output_window.wm_attributes('-topmost', True)
        
        # Display the code in the output window
        output_label = tk.Text(self.output_window, wrap='word', width=text_width, height=text_height, background=self.bg_color, foreground=self.fg_color, padx=10, pady=10)
        output_label.tag_configure('center', justify='center')
        output_label.insert(1.0, code, 'center')
        output_label.config(state='disabled')
        output_label.pack()

        # Extract the code part from the full text
        match = re.search(r'Code:\n((?:.*\n*)+)', code)
        code_part = match.group(1).strip() if match else code

        # Add a button to copy the code to the clipboard if the code is valid
        if "Error:" not in code:
            copy_button = ttk.Button(self.output_window, text="Copy to Clipboard", command=lambda: self.copy_code(code_part))
            copy_button.pack(fill='x')

        # Set the window size and position
        self.center_window(self.output_window)
        self.output_window.focus_force()
        self.output_window.focus_set()

    def output_error(self, error_message):
        
        # Initialize the output window
        self.error_window = tk.Toplevel(self.root)
        self.error_window.title("Error")
        self.set_icon(self.error_window)
        self.error_window.wm_attributes('-topmost', True)

        # Display the error message in the output window
        error_label = ttk.Label(self.error_window, text=error_message, justify="center", wraplength=400, width=40, anchor="center")
        error_label.pack(padx=10, pady=10, side="top")

        # Set the window size and position
        self.center_window(self.error_window)

    def close(self, window):

        # Re-enable the button and hide the window
        window.withdraw()

    def base_options(self):

        # Define values used in this function
        controller_width = len(max(list(Config.KEYBINDS), key=len))
        difficulty_width = len(max(Config.DIFF_LIST, key=len))
        version_width = len(max(Config.VER_LIST, key=len))
        button_width = int((controller_width + difficulty_width + version_width) / 3)
        
        # Create function to update the buttons based on the selected controller
        def update_buttons():

            # Get new selection
            choice = self.controller.get()

            # Clear previous checkboxes
            self.checkboxes.clear()

            # Clear previous buttons
            for item in self.button_select.winfo_children():
                item.destroy()

            # Update the buttons based on the selected controller
            if choice == "None - Always On":
                ttk.Label(self.button_select, text='Button Selection will appear here when a valid controller is selected.').pack()
            else:
                for i, option in enumerate(Config.KEYBINDS[choice]):
                    c = i // 4
                    r = i % 4  # This avoids manual subtraction

                    var = tk.BooleanVar()
                    checkbox = ttk.Checkbutton(self.button_select, text=option, variable=var)
                    checkbox.grid(row=r, column=c, pady=5)
                    self.checkboxes.append(var)

                for col in range(c + 1):  # Ensure all columns are configured
                    self.button_select.grid_columnconfigure(col, weight=1, uniform='equal')

            self.root.update_idletasks()
            self.root.geometry("")

        dropdown_frame = ttk.Frame(self.root)
        dropdown_frame.grid(row=0, column=0, padx=5, pady=5)
        dropdown_frame.grid_columnconfigure(0, weight=1, uniform="equal")

        # Create Controller Frame

        controller_label = ttk.Label(dropdown_frame, text='Controller')
        controller_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        controller_label.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.controller = ttk.Combobox(dropdown_frame, values=list(Config.KEYBINDS), width=controller_width)
        self.controller.set(list(Config.KEYBINDS)[0])
        self.controller.bind("<<ComboboxSelected>>", lambda event: update_buttons())
        self.controller.grid(row=1, column=0, padx=5, pady=5)

        # Create Difficulty Frame

        difficulty_label = ttk.Label(dropdown_frame, text='Difficulty')
        difficulty_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        difficulty_label.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.difficulty = ttk.Combobox(dropdown_frame, values=Config.DIFF_LIST, width=difficulty_width)
        self.difficulty.set(Config.DIFF_LIST[1])
        self.difficulty.grid(row=1, column=1, padx=5, pady=5)

        # Create Version Frame

        version_label = ttk.Label(dropdown_frame, text='Version')
        version_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        version_label.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        self.version = ttk.Combobox(dropdown_frame, values=Config.VER_LIST, width=version_width)
        self.version.set(Config.VER_LIST[1])
        self.version.grid(row=1, column=2, padx=5, pady=5)

        # Create Checkbox Frame
        self.checkboxes = []
        self.button_select = ttk.Frame(self.root)
        ttk.Label(self.button_select, text='Button Selection will appear here when a valid controller is selected.').pack()
        self.button_select.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        self.button_select.grid_anchor(anchor='center')

        # Create Buttons
        base_buttons = ttk.Frame(self.root)
        base_buttons.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')
        base_buttons.grid_anchor('center')

        self.char_button = ttk.Button(base_buttons, text='Character', width=button_width, command=lambda: self.character_window.deiconify())
        self.char_button.grid(row=0, column=0, padx=5, pady=5)

        self.class_button = ttk.Button(base_buttons, text='Class', width=button_width, command=lambda: self.class_window.deiconify())
        self.class_button.grid(row=0, column=1, padx=5, pady=5)

        self.item_button = ttk.Button(base_buttons, text='Item', width=button_width, command=lambda: self.item_window.deiconify())
        self.item_button.grid(row=0, column=2, padx=5, pady=5)

        # all_button = ttk.Button(base_buttons, text='Generate All Codes')
        # all_button.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky='nsew')

        database_button = ttk.Button(base_buttons, text='Database', width=button_width, command=lambda: self.database_window.deiconify())
        database_button.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

        help_button = ttk.Button(base_buttons, text='Help', width=button_width, command=lambda: self.help_win.deiconify())
        help_button.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')

        discord_button = ttk.Button(base_buttons, text='Discord', width=button_width, command=self.show_discord)
        discord_button.grid(row=2, column=2, padx=5, pady=5, sticky='nsew')

    def character_editor(self):

        character_width = len(max(Config.CHAR_LIST, key=len))
        class_width = len(max(Config.CLASS_LIST, key=len))
        stat_width = 5
        rank_width = 5

        # Create the character window if it doesn't exist
        self.character_window = tk.Toplevel(self.root, background=self.bg_color)
        self.character_window.withdraw()
        self.character_window.title('Character Editor')
        self.set_icon(self.character_window)
        self.character_window.protocol('WM_DELETE_WINDOW', lambda: self.close(self.character_window))

        # Character Selection

        character_select = ttk.Frame(self.character_window)
        character_select.grid(row=0, column=0, sticky='nsew')
        character_select.columnconfigure(0, weight=1)

        character_label = ttk.Label(character_select, text='Character')
        character_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        character_label.grid(padx=5, pady=5, sticky='nsew')

        self.character_sel = ttk.Combobox(character_select, values=['All']+Config.CHAR_LIST, width=character_width)
        self.character_sel.set('')
        self.character_sel.grid(padx=5, pady=5, sticky='nsew')

        character_reset = ttk.Button(character_select, text='Reset', command=lambda: self.character_sel.set(''))
        character_reset.grid(padx=5, pady=5, sticky='nsew')

        # Character Class Selection

        character_class = ttk.Frame(self.character_window)
        character_class.grid(row=0, column=1, sticky='nsew')
        character_class.columnconfigure(0, weight=1)

        class_label = ttk.Label(character_class, text='Class')
        class_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        class_label.grid(padx=5, pady=5, sticky='nsew')

        self.character_class = ttk.Combobox(character_class, values=Config.CLASS_LIST, width=class_width)
        self.character_class.set('')
        self.character_class.grid(padx=5, pady=5, sticky='nsew')

        character_class_reset = ttk.Button(character_class, text='Reset', command=lambda: self.character_class.set(''))
        character_class_reset.grid(padx=5, pady=5, sticky='nsew')

        # Character Stats Entries

        def reset_stats():
            for entry in self.character_stats:
                entry.delete(0, 'end')

        character_stats = ttk.Frame(self.character_window)
        character_stats.grid(row=1, column=0, sticky='nsew')
        character_stats.columnconfigure(0, weight=1)

        stats_label = ttk.Label(character_stats, text='Stats')
        stats_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        stats_label.grid(padx=5, pady=5, columnspan=2, sticky='nsew')

        self.character_stats = []
        for i, stat in enumerate(Config.CHAR_STATS):
            i +=1
            entry_label = ttk.Label(character_stats, text=stat.replace("_", " "))
            entry_label.grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(character_stats, width=stat_width, justify='center')
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.character_stats.append(entry)

        character_stats_reset = ttk.Button(character_stats, text='Reset', command=reset_stats)
        character_stats_reset.grid(padx=5, pady=5, columnspan=2, sticky='nsew')

        # Character Ranks Selections

        def reset_ranks():
            for sel in self.character_ranks:
                sel.set('')
        
        character_ranks = ttk.Frame(self.character_window)
        character_ranks.grid(row=1, column=1, sticky='nsew')
        character_ranks.grid_columnconfigure([0, 1], weight=1)

        ranks_label = ttk.Label(character_ranks, text='Ranks')
        ranks_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        ranks_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        self.character_ranks = []
        for i, rank in enumerate(Config.CHAR_RANKS):
            i += 1
            character_ranks.grid_rowconfigure(i, weight=1)
            entry_label = ttk.Label(character_ranks, text=rank.replace("_", " "))
            entry_label.grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Combobox(character_ranks, values=['']+Config.RANKS, width=rank_width)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.character_ranks.append(entry)
        
        character_ranks_reset = ttk.Button(character_ranks, text='Reset', command=reset_ranks)
        character_ranks_reset.grid(padx=5, pady=5, columnspan=2, sticky='nsew')

        # Buttons

        character_items = ttk.Button(self.character_window, text='Items', command=lambda: self.character_items_window.deiconify())
        character_items.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        char_button = ttk.Button(self.character_window, text='Generate Character Code', command=lambda: self.code_creation(0))
        char_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        close_button = ttk.Button(self.character_window, text='Close', command=lambda: self.close(self.character_window))
        close_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        self.character_window.resizable(False, False)
        self.center_window(self.character_window)

    def character_items_editor(self):

        item_width = len(max(Config.ITEM_LIST, key=len))
        num_width = 5
        name_width = 20


        def reset_inventory():
            for row in self.character_inventory:
                for widget in row:
                    if isinstance(widget, ttk.Entry):
                        widget.delete(0, 'end')
                    elif isinstance(widget, tk.BooleanVar):
                        widget.set(0)
                    else:
                        widget.set('')

        self.character_items_window = tk.Toplevel(self.root, background=self.bg_color)
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
                    header = ttk.Label(self.character_items_window, text=title)
                    header.config(font=self.app_font + ('underline',), justify='center', anchor='center')
                    header.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
                elif r == 8:
                    reset_button = ttk.Button(self.character_items_window, text='Reset', command=reset_inventory)
                    reset_button.grid(row=r, column=0, columnspan=len(Config.CHAR_INV), padx=5, pady=5, sticky='nsew')

                    close_button = ttk.Button(self.character_items_window, text='Close', command=lambda: self.close(self.character_items_window))
                    close_button.grid(row=r+1, column=0, columnspan=len(Config.CHAR_INV), padx=5, pady=5, sticky='nsew')
                    break
                elif title == 'Item':
                    combobox = ttk.Combobox(self.character_items_window, values=Config.ITEM_LIST, width=item_width)
                    combobox.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
                    inv_row.append(combobox)
                    combobox.set('')
                elif title in ['Uses', 'Forge Name', 'Mt', 'Hit', 'Crit']:
                    w = name_width if title == 'Forge Name' else num_width
                    entry = ttk.Entry(self.character_items_window, width=w)
                    entry.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
                    inv_row.append(entry)
                elif title in ['Wt', 'Forged', 'Blessed']:
                    var = tk.BooleanVar()
                    var.set(False)
                    checkbox = ttk.Checkbutton(self.character_items_window, text=None, variable=var)
                    checkbox.state(['!selected'])
                    checkbox.grid(row=r, column=c, padx=5, pady=5, sticky='ns')
                    inv_row.append(var)
                else:
                    raise "Error in character inventory."

            self.character_inventory.append(inv_row)
    
        self.character_items_window.resizable(False, False)
        self.center_window(self.character_items_window)

    def class_editor(self):

        class_width = len(max(Config.CLASS_LIST, key=len))
        stat_width = 5
        rank_width = 5

        self.class_window = tk.Toplevel(self.root, background=self.bg_color)
        self.class_window.withdraw()
        self.class_window.title('Class Editor')
        self.set_icon(self.class_window)
        self.class_window.protocol('WM_DELETE_WINDOW', lambda: self.close(self.class_window))

        # Class Selection

        class_select = ttk.Frame(self.class_window)
        class_select.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        class_label = ttk.Label(class_select, text='Class')
        class_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        class_label.grid(padx=5, pady=5, sticky='nsew')

        self.class_sel = ttk.Combobox(class_select, values=['All']+Config.CLASS_LIST, width=class_width)
        self.class_sel.set('')
        self.class_sel.grid(padx=5, pady=5, sticky='nsew')

        class_reset = ttk.Button(class_select, text='Reset', command=lambda: self.class_sel.set(''))
        class_reset.grid(padx=5, pady=5, sticky='nsew')

        # Class Promote Selection

        class_promote_select = ttk.Frame(self.class_window)
        class_promote_select.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        class_promote_select.columnconfigure(0, weight=1)

        class_promote_label = ttk.Label(class_promote_select, text='Promote')
        class_promote_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        class_promote_label.grid(padx=5, pady=5, sticky='nsew')

        self.class_promote = ttk.Combobox(class_promote_select, values=Config.CLASS_LIST, width=class_width)
        self.class_promote.set('')
        self.class_promote.grid(padx=5, pady=5, sticky='nsew')

        class_promote_reset = ttk.Button(class_promote_select, text='Reset', command=lambda: self.class_promote.set(''))
        class_promote_reset.grid(padx=5, pady=5, sticky='nsew')

        # Class Stats Entries

        def reset_class_stats():
            for entry in self.class_stats:
                entry.delete(0, 'end')
        
        self.class_stats = []

        class_stats_entries = ttk.Frame(self.class_window)
        class_stats_entries.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        class_stats_entries.grid_anchor('n')
        class_stats_entries.grid_columnconfigure([0,1], weight=1)

        class_stats_label = ttk.Label(class_stats_entries, text='Stats')
        class_stats_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        class_stats_label.grid(padx=5, pady=5, columnspan=2, sticky='nsew')

        for i, stat in enumerate(Config.CLASS_STATS):
            i += 1
            class_stats_entries.grid_rowconfigure(i, weight=1)
            entry_label = ttk.Label(class_stats_entries, text=stat.replace("_", " "))
            entry_label.grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(class_stats_entries, width=stat_width, justify='center')
            entry.grid(row=i, column=1, padx=5, pady=5)

            self.class_stats.append(entry)

        class_stats_reset = ttk.Button(class_stats_entries, text='Reset', command=reset_class_stats)
        class_stats_reset.grid(padx=5, pady=5, columnspan=2, sticky='nsew')

        # Class Ranks Selections

        def reset_class_ranks(reset_list):
            for sel in reset_list:
                sel.set('')
        
        self.class_min_ranks = []
        self.class_max_ranks = []

        class_ranks_selections = ttk.Frame(self.class_window)
        class_ranks_selections.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        class_ranks_selections.grid_anchor('center')
        class_ranks_selections.columnconfigure([0,1,2], weight=1)

        class_ranks_label = ttk.Label(class_ranks_selections, text='Ranks')
        class_ranks_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        class_ranks_label.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        class_ranks_min_label = ttk.Label(class_ranks_selections, text='Min Ranks')
        class_ranks_min_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        class_ranks_min_label.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        class_ranks_max_label = ttk.Label(class_ranks_selections, text='Max Ranks')
        class_ranks_max_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        class_ranks_max_label.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

        for i, rank in enumerate(Config.CHAR_RANKS):
            i += 1
            entry_label = ttk.Label(class_ranks_selections, text=rank.replace("_", " "))
            entry_label.grid(row=i, column=0, padx=5, pady=5)

            min_entry = ttk.Combobox(class_ranks_selections, values=['']+Config.RANKS, width=rank_width)
            min_entry.grid(row=i, column=1, padx=5, pady=5)
            self.class_min_ranks.append(min_entry)

            max_entry = ttk.Combobox(class_ranks_selections, values=['']+Config.RANKS, width=rank_width)
            max_entry.grid(row=i, column=2, padx=5, pady=5)
            self.class_max_ranks.append(max_entry)

        class_ranks_reset_all = ttk.Button(class_ranks_selections, text='Reset All', command=lambda: reset_class_ranks(self.class_min_ranks + self.class_max_ranks))
        class_ranks_reset_all.grid(row=len(self.class_max_ranks)+1, column=0, padx=5, pady=5, sticky='nsew')

        class_min_ranks_reset = ttk.Button(class_ranks_selections, text='Reset Min', command=lambda: reset_class_ranks(self.class_min_ranks))
        class_min_ranks_reset.grid(row=len(self.class_min_ranks)+1, column=1, padx=5, pady=5, sticky='nsew')

        class_max_ranks_reset = ttk.Button(class_ranks_selections, text='Reset Max', command=lambda: reset_class_ranks(self.class_max_ranks))
        class_max_ranks_reset.grid(row=len(self.class_max_ranks)+1, column=2, padx=5, pady=5, sticky='nsew')

        # Buttons

        class_button = ttk.Button(self.class_window, text='Generate Character Code', command=lambda: self.code_creation(1))
        class_button.grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        close_button = ttk.Button(self.class_window, text='Close', command=lambda: self.close(self.class_window))
        close_button.grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        self.class_window.resizable(False, False)
        self.center_window(self.class_window)

    def items_editor(self):

        item_width = 30
        item_data_width = 10
        item_stat_width = 5
        item_bonus_width = 5
        
        self.item_window = tk.Toplevel(self.root, background=self.bg_color)
        self.item_window.withdraw()
        self.item_window.title('Item Editor')
        self.set_icon(self.item_window)
        self.item_window.protocol('WM_DELETE_WINDOW', lambda: self.close(self.item_window))

        # Item Select

        item_select = ttk.Frame(self.item_window)
        item_select.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
        item_select.grid_anchor('center')
        item_select.grid_columnconfigure(0, weight=1)

        item_label = ttk.Label(item_select, text='Item')
        item_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        item_label.grid(padx=5, pady=5, sticky='nsew')

        self.item_sel = ttk.Combobox(item_select, values=['All']+Config.ITEM_LIST, width=item_width)
        self.item_sel.set('')
        self.item_sel.grid(padx=5, pady=5, sticky='nsew')

        item_reset = ttk.Button(item_select, text='Reset', command=lambda: self.item_sel.set(''))
        item_reset.grid(columnspan=3, padx=5, pady=5, sticky='nsew')

        # Item Data

        def reset_data():
            for entry in self.item_data:
                if isinstance(entry, ttk.Entry):
                    entry.delete(0, 'end')
                elif isinstance(entry, ttk.Combobox):
                    entry.set('')
                elif isinstance(entry, ttk.Checkbutton):
                    entry.deselect()

        item_data_frame = ttk.Frame(self.item_window)
        item_data_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        item_data_frame.grid_anchor('center')
        item_data_frame.grid_columnconfigure([0,1], weight=1)

        item_data_label = ttk.Label(item_data_frame, text='Item Data')
        item_data_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        item_data_label.grid(columnspan=2, padx=5, pady=5, sticky='nsew')
        
        self.item_data = []
        for i, data in enumerate(Config.ITEM_DATA):
            i += 1
            item_data_frame.grid_rowconfigure(i, weight=1)
            ttk.Label(item_data_frame, text=data.replace("_", " ")).grid(row=i, column=0, padx=5, pady=5, sticky='nsew')
            if data in ['Attack_Type', 'Weapon_Rank']:
                opt_list = ['ATK', 'MAG'] if data == 'Attack_Type' else Config.RANKS
                option_menu = ttk.Combobox(item_data_frame, values=opt_list, width=item_data_width)
                option_menu.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
                option_menu.set('')
                self.item_data.append(option_menu)
            elif data in ['EXP_Gain']:
                entry = ttk.Entry(item_data_frame, width=item_data_width, justify='center')
                entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
                self.item_data.append(entry)
            elif data in ['Unlock', 'Char_Unlock', 'Infinite', 'Brave', 'Heal']:
                checkbox = ttk.Checkbutton(item_data_frame, text=None, width=0)
                checkbox.grid(row=i, column=1, padx=5, pady=5, sticky='ns')
                self.item_data.append(checkbox)

        item_data_reset = ttk.Button(item_data_frame, text='Reset', command=reset_data)
        item_data_reset.grid(columnspan=2, padx=5, pady=5, sticky='ew')

        # Item Stats

        self.item_stats = []

        item_stats_frame = ttk.Frame(self.item_window)
        item_stats_frame.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        item_stats_frame.grid_anchor('center')
        item_stats_frame.grid_columnconfigure([0,1], weight=1)

        item_stat_label = ttk.Label(item_stats_frame, text='Item Stats')
        item_stat_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        item_stat_label.grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        for i, stat in enumerate(Config.ITEM_STATS):
            i += 1
            item_stats_frame.grid_rowconfigure(i, weight=1)
            ttk.Label(item_stats_frame, text=stat.replace("_", " ")).grid(row=i, column=0, padx=5, pady=5, sticky='nsew')
            entry = ttk.Entry(item_stats_frame, width=item_stat_width, justify='center')
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            self.item_stats.append(entry)

        item_stat_reset = ttk.Button(item_stats_frame, text='Reset', command=lambda: [entry.delete(0, 'end') for entry in self.item_stats])
        item_stat_reset.grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        # Item Equip Bonuses

        item_equip_frame = ttk.Frame(self.item_window)
        item_equip_frame.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

        item_bonus_label = ttk.Label(item_equip_frame, text='Equip Bonuses')
        item_bonus_label.config(font=self.app_font + ('underline',), justify='center', anchor='center')
        item_bonus_label.grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        self.item_equip = []
        for i, bonus in enumerate(Config.ITEM_EQUIP_BONUS):
            i += 1
            ttk.Label(item_equip_frame, text=bonus.replace("_", " ")).grid(row=i, column=0, padx=5, pady=5, sticky='nsew')
            entry = ttk.Entry(item_equip_frame, width=item_bonus_width, justify='center')
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='nsew')
            self.item_equip.append(entry)
        
        item_equip_reset = ttk.Button(item_equip_frame, text='Reset', command=lambda: [entry.delete(0, 'end') for entry in self.item_equip])
        item_equip_reset.grid(columnspan=2, padx=5, pady=5, sticky='nsew')

        # Buttons

        item_button = ttk.Button(self.item_window, text='Generate Item Code', command=lambda: self.code_creation(2))
        item_button.grid(columnspan=3, padx=5, pady=5, sticky='nsew')

        item_close = ttk.Button(self.item_window, text='Close', command=lambda: self.close(self.item_window))
        item_close.grid(columnspan=3, padx=5, pady=5, sticky='nsew')

        self.item_window.resizable(False, False)
        self.center_window(self.item_window)

    def code_database(self):
        
        # Initialize the database window
        self.database_window = tk.Toplevel(self.root, background=self.bg_color)
        self.database_window.withdraw()
        self.database_window.title("Code Database")
        self.set_icon(self.database_window)
        self.database_window.wm_attributes('-topmost', True)
        self.database_window.protocol('WM_DELETE_WINDOW', lambda: self.close(self.database_window))

        num_per_row = 5

        # Create add buttons for each code
        for i, code in enumerate(Config.CODE_DATABASE):
            if i < num_per_row:
                self.database_window.grid_columnconfigure(i, weight=1, uniform='equal')
            code_button = ttk.Button(self.database_window, text=code, command=lambda cd=code: self.generate_database_code(cd))
            code_button.grid(row=i // num_per_row, column=i % num_per_row, padx=5, pady=5, sticky='nsew')

        database_close = ttk.Button(self.database_window, text='Close', command=lambda: self.close(self.database_window))
        database_close.grid(columnspan=num_per_row, padx=5, pady=5, sticky='nsew')

        # Set the window size and position
        self.database_window.resizable(False, False)
        self.center_window(self.database_window)

    def help_window(self):

        self.help_win = tk.Toplevel(self.root, background=self.bg_color)
        self.help_win.withdraw()
        self.help_win.title('Help')
        self.help_win.geometry('600x600')
        self.set_icon(self.help_win)
        self.help_win.grid_anchor('center')
        self.help_win.protocol('WM_DELETE_WINDOW', lambda: self.close(self.help_win))

        # Help Options
        self.help_menu = ttk.Combobox(self.help_win, values=['App', 'Controller', 'Difficulty', 'Version', 'Character', 'Class', 'Item', 'Database'])
        self.help_menu.set('App')
        self.help_menu.bind("<<ComboboxSelected>>", lambda event: self.get_help_data())
        self.help_menu.pack(padx=10, pady=10, fill='x')

        self.help_details = tk.Text(self.help_win, wrap='word', background=self.bg_color, foreground=self.fg_color)
        self.help_details.pack(side='left', padx=10, pady=(0,10), expand=True, fill='both')
        self.get_help_data()

        self.help_win.resizable(False, False)
        self.center_window(self.help_win)

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
        UDF.set_difficulty(self.difficulty.get())


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

    def get_help_data(self):

        self.help_details.config(state='normal')

        opt = self.help_menu.get()
        try:
            self.help_details.delete(1.0, tk.END)
        except:
            pass

        self.help_details.insert(1.0, Config.HELP[opt])
        self.help_details.config(state='disabled')

    def show_discord(self):
        self.type = 'Discord'
        server = 'https://discord.gg/dE5zRznC'

        self.output_code(server)