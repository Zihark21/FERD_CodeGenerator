import tkinter as tk
from tkinter import ttk
import re, ctypes, os, sys
from Sources.Config import CHAR_LIST, CLASS_LIST, ITEM_LIST, SECTION_HEADER, DESC, CHAR_STATS, CHAR_RANKS, CLASS_STATS, ITEM_STATS, ITEM_DATA, ITEM_BONUS, CODE_DATABASE
from Sources.UDF import get_char_code, get_class_code, get_item_code, get_keybind_code, set_version

dpi = ctypes.windll.shcore.SetProcessDpiAwareness(True)

class CodeGeneratorGUI:

    #region GUI Setup and Output

    def __init__(self, root):
        self.root = root
        self.root.title("FE:RD Code Creator")
    
        # Set no resize
        self.root.resizable(False, False)
    
        # Determine the base path
        base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.abspath(".")
    
        icon_path = os.path.join(base_path, "Assets", "FE-RD.ico")
        self.root.iconbitmap(icon_path)
    
        # Set dark mode colors
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#000000", foreground="#ffffff")
        style.configure("TNotebook.Tab", background="#000000", foreground="#ffffff")
        style.map("TNotebook.Tab", background=[("selected", "#2e2e2e")])
    
        # Configure text color for various widgets
        style.configure("TFrame", background="#2e2e2e")
        style.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
        style.configure("TEntry", fieldbackground="#ffffff", foreground="#000000")
        style.configure("TCombobox", fieldbackground="#ffffff", foreground="#000000")
        style.map("TCombobox", fieldbackground=[("readonly", "#ffffff")], foreground=[("readonly", "#000000")])
        style.configure("TCheckbutton", background="#2e2e2e", foreground="#000000")
    
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)
    
        self.options_tab()
        self.character_tab()
        self.class_tab()
        self.items_tab()
        self.database_tab()
    
    def copy_and_close(self, code, message_window):
        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        message_window.destroy()
    
    def output_code(self, code):
        # Create a new window for the message box
        message_window = tk.Toplevel(self.root)
        message_window.title("Code")
        message_window.configure(bg="#2e2e2e")
    
        # Add a label to display the output
        output_label = ttk.Label(message_window, text=code, justify="center", wraplength=300)
        output_label.pack(padx=10, pady=10)
    
        match = re.search(r'Code:\n((?:.*\n*)+)', code)
        code_part = match.group(1).strip() if match else code
    
        error_list = [
            "No character selected!",
            "No class selected!",
            "No item selected!",
            "No changes made!"
        ]
        if code not in error_list and "Error:" not in code:
            # Add a button to copy to clipboard
            copy_button = ttk.Button(message_window, text="Copy to Clipboard", command=lambda: self.copy_and_close(code_part, message_window))
            copy_button.pack(pady=5)

    #endregion

    #region Options Tab

    def options_tab(self):
        options_tab = ttk.Frame(self.notebook)
        self.notebook.add(options_tab, text="Options")
    
        self._options_separators(options_tab)
        self._options_controller(options_tab)
        self._options_version(options_tab)
        self._options_info(options_tab)
        self._options_button(options_tab)
    
    def _options_separators(self, options_tab):
        ttk.Separator(options_tab, orient="horizontal").grid(row=1, column=0, columnspan=99, sticky="ew")
        ttk.Separator(options_tab, orient="vertical").grid(row=0, column=2, rowspan=4, sticky="ns")
        ttk.Separator(options_tab, orient="vertical").grid(row=0, column=4, rowspan=4, sticky="ns")
        ttk.Separator(options_tab, orient="horizontal").grid(row=3, column=0, columnspan=99, sticky="ew")
    
    def _options_controller(self, options_tab):
        self.keybinds = {
            "": "",
            "Classic Controller": [
                "Left", "Right", "Up", "Down", "A", "B", "X", "Y", "ZL", "ZR", "L", "R", "+", "-"
            ],
            "GameCube Controller": [
                "Left", "Right", "Up", "Down", "A", "B", "X", "Y", "Z", "L", "R", "Start"
            ],
        }
    
        controller_frame = ttk.Frame(options_tab)
        controller_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
        ttk.Label(controller_frame, text="Controller:", font=SECTION_HEADER).grid(row=0, column=0, padx=5)
        self.controller = ttk.Combobox(controller_frame, values=list(self.keybinds.keys()))
        self.controller.grid(row=0, column=1)
        self.controller.bind("<<ComboboxSelected>>", self.update_checkboxes)
    
        self.checkboxes = []
        self.checkbox_frame = ttk.Frame(options_tab)
        self.checkbox_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    
    def _options_version(self, options_tab):
        version_frame = ttk.Frame(options_tab)
        version_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")
    
        ttk.Label(version_frame, text="Version:", font=SECTION_HEADER).grid(row=0, column=0, padx=5)
        self.version = ttk.Combobox(version_frame, values=["NTSC 1.00", "NTSC 1.01", "PAL"])
        self.version.grid(row=0, column=1)
    
    def _options_info(self, options_tab):
        options_info = ttk.Frame(options_tab)
        options_info.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")
    
        opt_desc = DESC["Option_Desc"]
        ttk.Label(options_info, text=opt_desc, wraplength=1000, justify="left").grid(row=0, column=0)
    
    def _options_button(self, options_tab):
        gen_all_button = ttk.Button(options_tab, text="Generate All Codes", command=self.generate_all)
        gen_all_button.grid(row=4, column=0, columnspan=99, sticky='nsew')
    
    def update_checkboxes(self, event):
        for checkbox in self.checkbox_frame.winfo_children():
            checkbox.destroy()
        self.checkboxes = []
    
        selected_option = self.controller.get()
        if selected_option == "":
            return
    
        if selected_option in self.keybinds:
            length = len(self.keybinds[selected_option])
            ttk.Label(self.checkbox_frame, text="Buttons", font=SECTION_HEADER).grid(row=0, column=0, rowspan=length, padx=5)
            ttk.Separator(self.checkbox_frame, orient="vertical").grid(row=0, column=1, rowspan=length, sticky="ns")
            for i, option in enumerate(self.keybinds[selected_option]):
                ttk.Label(self.checkbox_frame, text=option).grid(row=i, column=3, padx=5, sticky="e")
                var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(self.checkbox_frame, variable=var)
                checkbox.grid(row=i, column=4)
                self.checkboxes.append(var)

    #endregion

    #region Character

    def character_tab(self):
        char_tab = ttk.Frame(self.notebook)
        self.notebook.add(char_tab, text="Character")
    
        self._char_separators(char_tab)
        self._char_class(char_tab)
        self._char_items(char_tab)
        self._char_stats(char_tab)
        self._char_ranks(char_tab)
        self._char_button(char_tab)
    
    def _char_separators(self, tab):
        ttk.Separator(tab, orient="vertical").grid(row=0, column=3, sticky="ns")
        ttk.Separator(tab, orient="horizontal").grid(row=1, column=0, columnspan=99, sticky="ew")
        ttk.Separator(tab, orient="vertical").grid(row=2, column=1, sticky="ns")
        ttk.Separator(tab, orient="vertical").grid(row=2, column=3, sticky="ns")
        ttk.Separator(tab, orient="horizontal").grid(row=3, column=0, columnspan=99, sticky="ew")
    
    def _char_class(self, tab):
        char_frame = ttk.Frame(tab)
        char_frame.grid(row=0, column=0, sticky="nsew", columnspan=3, padx=10, pady=10)
        ttk.Label(char_frame, text="Character:", font=SECTION_HEADER).grid(row=0, column=0)
        self.char_select = ttk.Combobox(char_frame, values=CHAR_LIST)
        self.char_select.grid(row=0, column=1, padx=10)
    
        char_class_frame = ttk.Frame(tab)
        char_class_frame.grid(row=0, column=4, sticky="nsew", columnspan=4, padx=10, pady=10)
        ttk.Label(char_class_frame, text="Class:", font=SECTION_HEADER).grid(row=0, column=0)
        self.char_class = ttk.Combobox(char_class_frame, values=CLASS_LIST, width=40)
        self.char_class.grid(row=0, column=1, padx=10)
    
    def _char_items(self, tab):
        self.char_items = []
        char_items_frame = ttk.Frame(tab)
        char_items_frame.grid(row=2, column=5, padx=10, pady=10, sticky='nsew')
    
        char_item_table = ttk.Frame(char_items_frame)
        char_item_table.grid(row=0, column=0, sticky='n')
    
        headers = ["Items", "Uses", "Forged Name", "Mt", "Hit", "Crit", "Weightless", "Forged", "Blessed"]
        for i, header in enumerate(headers):
            ttk.Label(char_item_table, text=header, font=SECTION_HEADER).grid(row=0, column=i, padx=5, pady=5 if header in ['Blessed', 'Forged', 'Weightless'] else 0)
    
        for row in range(1, 8):
            char_item_row = []
            char_item_combobox = ttk.Combobox(char_item_table, values=ITEM_LIST, width=25)
            char_item_combobox.grid(row=row, column=0, padx=1, pady=1)
            char_item_row.append(char_item_combobox)
    
            for col in range(1, 9):
                if col in [6, 7, 8]:
                    char_item_var = tk.BooleanVar(value=False)
                    checkbox = ttk.Checkbutton(char_item_table, text="", variable=char_item_var)
                    checkbox.grid(row=row, column=col)
                    char_item_row.append(char_item_var)
                else:
                    width = 20 if col == 2 else 5
                    char_item_entry = ttk.Entry(char_item_table, width=width)
                    char_item_entry.grid(row=row, column=col, padx=1, pady=1)
                    char_item_row.append(char_item_entry)
    
            self.char_items.append(char_item_row)
    
        char_desc_frame = ttk.Frame(char_items_frame)
        char_desc_frame.grid(row=1, column=0, sticky='nsew')
        char_desc = DESC['Char_Tab_Desc']
        ttk.Label(char_desc_frame, text=char_desc, wraplength=1000, justify='left').grid(row=0, column=0, padx=5, pady=5)
    
    def _char_stats(self, tab):
        char_stat_frame = ttk.Frame(tab)
        char_stat_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        ttk.Label(char_stat_frame, text="Stats", font=SECTION_HEADER).grid(row=0, column=0, columnspan=2, pady=5)
        self.char_stats = []
    
        for i, stat in enumerate(CHAR_STATS):
            ttk.Label(char_stat_frame, text=stat).grid(row=i+1, column=0, padx=5, sticky="e")
            char_stat_entry = ttk.Entry(char_stat_frame, width=5)
            char_stat_entry.grid(row=i+1, column=1, pady=1)
            self.char_stats.append(char_stat_entry)
    
    def _char_ranks(self, tab):
        char_rank_frame = ttk.Frame(tab)
        char_rank_frame.grid(row=2, column=2, padx=10, pady=10, sticky='nsew')
        ttk.Label(char_rank_frame, text="Weapon Ranks", font=SECTION_HEADER).grid(row=0, column=3, columnspan=2, pady=5)
        self.char_ranks = []
    
        for i, rank in enumerate(CHAR_RANKS):
            ttk.Label(char_rank_frame, text=rank.replace('_', ' ')).grid(row=i + 1, column=3, padx=5, sticky="e")
            char_ranks_combobox = ttk.Combobox(char_rank_frame, values=["SS", "S", "A", "B", "C", "D", "E"], width=5)
            char_ranks_combobox.grid(row=i + 1, column=4, pady=1)
            self.char_ranks.append(char_ranks_combobox)
    
    def _char_button(self, tab):
        char_button = ttk.Button(tab, text="Generate", command=self.generate_character)
        char_button.grid(row=4, column=0, columnspan=99, sticky="nsew")

    #endregion

    #region Class

    def class_tab(self):
        class_tab = ttk.Frame(self.notebook)
        self.notebook.add(class_tab, text="Class")
    
        self._class_separators(class_tab)
        self._class_select(class_tab)
        self._class_promote(class_tab)
        self._class_min_ranks(class_tab)
        self._class_max_ranks(class_tab)
        self._class_stats(class_tab)
        self._class_info(class_tab)
        self._class_button(class_tab)
    
    def _class_separators(self, tab):
        ttk.Separator(tab, orient="vertical").grid(row=0, column=5, sticky="ns")
        ttk.Separator(tab, orient="horizontal").grid(row=1, column=0, columnspan=99, sticky="ew")
        ttk.Separator(tab, orient="horizontal").grid(row=3, column=0, columnspan=99, sticky="ew")
        ttk.Separator(tab, orient="vertical").grid(row=2, column=1, rowspan=99, sticky="ns")
        ttk.Separator(tab, orient="vertical").grid(row=2, column=3, rowspan=99, sticky="ns")
        ttk.Separator(tab, orient="vertical").grid(row=2, column=5, rowspan=99, sticky="ns")
    
    def _class_select(self, tab):
        class_frame = ttk.Frame(tab)
        class_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=5, sticky="nsew")
        ttk.Label(class_frame, text="Class:", font=SECTION_HEADER).grid(row=0, column=0)
        self.class_select = ttk.Combobox(class_frame, values=['All'] + CLASS_LIST, width=40)
        self.class_select.grid(row=0, column=1, padx=10)
    
    def _class_promote(self, tab):
        class_promote_frame = ttk.Frame(tab)
        class_promote_frame.grid(row=0, column=6, padx=10, pady=10, columnspan=99, sticky="nsew")
        ttk.Label(class_promote_frame, text="Next Class:", font=SECTION_HEADER).grid(row=0, column=3)
        self.class_promote = ttk.Combobox(class_promote_frame, values=CLASS_LIST, width=40)
        self.class_promote.grid(row=0, column=4, padx=10)
    
    def _class_min_ranks(self, tab):
        class_min_rank_frame = ttk.Frame(tab)
        class_min_rank_frame.grid(row=2, column=0, padx=10, pady=10, sticky='n')
        ttk.Label(class_min_rank_frame, text="Min Weapon Ranks", font=SECTION_HEADER).grid(row=0, column=0, pady=5, columnspan=2)
        min_weapon_ranks = ['Min_' + i for i in CHAR_RANKS]
        self.class_min_ranks = []
        for i, rank in enumerate(min_weapon_ranks):
            ttk.Label(class_min_rank_frame, text=rank.replace('_', ' ')).grid(row=i + 1, column=0, padx=5, sticky="e")
            class_min_rank_combobox = ttk.Combobox(class_min_rank_frame, values=["SS", "S", "A", "B", "C", "D", "E"], width=5)
            class_min_rank_combobox.grid(row=i + 1, column=1, pady=1)
            self.class_min_ranks.append(class_min_rank_combobox)
    
    def _class_max_ranks(self, tab):
        class_max_rank_frame = ttk.Frame(tab)
        class_max_rank_frame.grid(row=2, column=2, padx=10, pady=10, sticky='n')
        ttk.Label(class_max_rank_frame, text="Max Weapon Ranks", font=SECTION_HEADER).grid(row=0, column=0, pady=5, columnspan=2)
        max_weapon_ranks = ['Max_' + i for i in CHAR_RANKS]
        self.class_max_ranks = []
        for i, rank in enumerate(max_weapon_ranks):
            ttk.Label(class_max_rank_frame, text=rank.replace('_', ' ')).grid(row=i + 1, column=0, padx=5, sticky="e")
            class_max_rank_combobox = ttk.Combobox(class_max_rank_frame, values=["SS", "S", "A", "B", "C", "D", "E"], width=5)
            class_max_rank_combobox.grid(row=i + 1, column=1, pady=1)
            self.class_max_ranks.append(class_max_rank_combobox)
    
    def _class_stats(self, tab):
        class_stats_frame = ttk.Frame(tab)
        class_stats_frame.grid(row=2, column=4, padx=10, pady=10, sticky='n')
        ttk.Label(class_stats_frame, text="Stats", font=SECTION_HEADER).grid(row=0, column=0, pady=5, columnspan=2)
        self.class_stats = []
        for i, stat in enumerate(CLASS_STATS):
            ttk.Label(class_stats_frame, text=stat.replace('_', ' ')).grid(row=i + 1, column=0, padx=5, sticky="e")
            class_stats_entry = ttk.Entry(class_stats_frame, width=5)
            class_stats_entry.grid(row=i + 1, column=1, pady=1)
            self.class_stats.append(class_stats_entry)
    
    def _class_info(self, tab):
        class_desc_frame = ttk.Frame(tab)
        class_desc_frame.grid(row=2, column=6, padx=10, pady=10, sticky='n')
        class_desc = DESC['Class_Tab_Desc']
        ttk.Label(class_desc_frame, text=class_desc, wraplength=650, justify='left').grid(row=0, column=0)
    
    def _class_button(self, tab):
        class_button = ttk.Button(tab, text="Generate", command=self.generate_class)
        class_button.grid(row=4, column=0, columnspan=99, sticky="nsew")

    #endregion

    #region Items

    def items_tab(self):
        items_tab = ttk.Frame(self.notebook)
        self.notebook.add(items_tab, text="Items")
    
        self._items_separators(items_tab)
        self._items_select(items_tab)
        self._items_data(items_tab)
        self._items_stats(items_tab)
        self._items_bonuses(items_tab)
        self._items_button(items_tab)
    
    def _items_separators(self, tab):
        ttk.Separator(tab, orient="horizontal").grid(row=1, column=0, columnspan=99, sticky="ew")
        ttk.Separator(tab, orient="horizontal").grid(row=3, column=0, columnspan=99, sticky="ew")
        ttk.Separator(tab, orient="vertical").grid(row=2, column=1, rowspan=99, sticky="ns")
        ttk.Separator(tab, orient="vertical").grid(row=2, column=3, rowspan=99, sticky="ns")
    
    def _items_select(self, tab):
        item_frame = ttk.Frame(tab)
        item_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=99, sticky="nsew")
    
        ttk.Label(item_frame, text="Item:", font=SECTION_HEADER).grid(row=0, column=0)
        self.item_select = ttk.Combobox(item_frame, values=['All'] + ITEM_LIST, width=25)
        self.item_select.grid(row=0, column=1, padx=10)
    
    def _items_data(self, tab):
        item_data_frame = ttk.Frame(tab)
        item_data_frame.grid(row=2, column=0, padx=10, pady=10, sticky="n")
    
        ttk.Label(item_data_frame, text="Weapon Data", font=SECTION_HEADER).grid(row=0, column=0, columnspan=2, pady=5)
        
        self.item_data = {}
    
        for i, label in enumerate(ITEM_DATA):
            ttk.Label(item_data_frame, text=label.replace('_', ' ')).grid(row=i + 1, column=0, padx=5, sticky="e")
    
            if label == "Attack_Type":
                self.item_data[label] = ttk.Combobox(item_data_frame, values=["STR", "MAG"], width=5)
            elif label == "Weapon_Rank":
                self.item_data[label] = ttk.Combobox(item_data_frame, values=["SS", "S", "A", "B", "C", "D", "E"], width=5)
            elif label in ["Unlock", "Char_Unlock", "Infinite", "Brave", "Heal"]:
                self.item_data[label] = tk.BooleanVar()
                ttk.Checkbutton(item_data_frame, variable=self.item_data[label]).grid(row=i + 1, column=1)
                continue
            else:
                self.item_data[label] = ttk.Entry(item_data_frame, width=5)
    
            self.item_data[label].grid(row=i + 1, column=1, pady=1)
    
    def _items_stats(self, tab):
        item_stats_frame = ttk.Frame(tab)
        item_stats_frame.grid(row=2, column=2, padx=10, pady=10, sticky="n")
    
        ttk.Label(item_stats_frame, text="Weapon Stats", font=SECTION_HEADER).grid(row=0, column=0, columnspan=2, pady=5)
        self.item_stats = []
    
        for i, stat in enumerate(ITEM_STATS):
            ttk.Label(item_stats_frame, text=stat.replace('_', ' ')).grid(row=i+1, column=0, padx=5, sticky="e")
            item_stats_entry = ttk.Entry(item_stats_frame, width=5)
            item_stats_entry.grid(row=i+1, column=1, pady=1)
            self.item_stats.append(item_stats_entry)
    
    def _items_bonuses(self, tab):
        item_bonus_frame = ttk.Frame(tab)
        item_bonus_frame.grid(row=2, column=4, padx=10, pady=10, sticky="n")
    
        ttk.Label(item_bonus_frame, text="Equip Bonuses", font=SECTION_HEADER).grid(row=0, column=0, columnspan=2, pady=5)
    
        self.item_bonuses = []
    
        for i, label in enumerate(ITEM_BONUS):
            ttk.Label(item_bonus_frame, text=label.replace('_', ' ')).grid(row=i + 1, column=0, padx=5, sticky="e")
            item_bonus_entry = ttk.Entry(item_bonus_frame, width=5)
            item_bonus_entry.grid(row=i + 1, column=1, pady=1)
            self.item_bonuses.append(item_bonus_entry)
    
    def _items_button(self, tab):
        item_button = ttk.Button(tab, text="Generate", command=self.generate_item)
        item_button.grid(row=4, column=0, columnspan=99, sticky="nsew")

    #endregion

    #region Database

    def database_tab(self):
        database_tab = ttk.Frame(self.notebook)
        self.notebook.add(database_tab, text="Database")
    
        for r, code_id in enumerate(CODE_DATABASE):
            code_id_button = ttk.Button(database_tab, text=code_id, command=lambda cid=code_id: self.generate_database_code(cid), width=15)
            code_id_button.grid(row=r // 8, column=r % 8, padx=5, pady=5)

    #endregion

    #region Code Generation

    def generate_all(self):
        character_data = self._get_character_data()
        class_data = self._get_class_data()
        item_data = self._get_item_data()
        keybinds_data = self._get_keybinds_data()
    
        ver_sel = self.version.get()
        version = set_version(ver_sel)
    
        key_code = get_keybind_code(keybinds_data)
        char_out = get_char_code(character_data, key_code)
        cls_out = get_class_code(class_data)
        item_out = get_item_code(item_data)
    
        output = '\n'.join([char_out, cls_out, item_out])
        self.output_code(output)
    
    def generate_character(self):
        character_data = self._get_character_data()
        keybinds_data = self._get_keybinds_data()
    
        ver_sel = self.version.get()
        version = set_version(ver_sel)
    
        key_code = get_keybind_code(keybinds_data)
        output = get_char_code(character_data, key_code)
        self.output_code(output)
    
    def generate_class(self):
        class_data = self._get_class_data()
    
        ver_sel = self.version.get()
        version = set_version(ver_sel)
    
        output = get_class_code(class_data)
        self.output_code(output)
    
    def generate_item(self):
        item_data = self._get_item_data()
    
        ver_sel = self.version.get()
        version = set_version(ver_sel)
    
        output = get_item_code(item_data)
        self.output_code(output)
    
    def generate_database_code(self, sel_code):
        ver_sel = self.version.get()
        version = set_version(ver_sel)
    
        keybinds_data = self._get_keybinds_data()
        key_code = get_keybind_code(keybinds_data)
    
        desc = CODE_DATABASE[sel_code]['DESC']
        code = CODE_DATABASE[sel_code][version]
    
        output = ' '.join([sel_code, code]) if 'unknown' in code else '\n'.join([desc, key_code, code, 'E0000000 80008000'])
        self.output_code(output)
    
    def _get_character_data(self):
        return {
            "character": self.char_select.get(),
            "class": self.char_class.get(),
            "stats": [stat.get() for stat in self.char_stats],
            "ranks": [rank.get() for rank in self.char_ranks],
            "items": [
                {
                    "item": row[0].get(),
                    "uses": row[1].get(),
                    "forge_name": row[2].get(),
                    "mt": row[3].get(),
                    "hit": row[4].get(),
                    "crit": row[5].get(),
                    "wt": row[6].get(),
                    "forged": row[7].get(),
                    "blessed": row[8].get(),
                }
                for row in self.char_items
            ]
        }
    
    def _get_class_data(self):
        return {
            "class": self.class_select.get(),
            "promote": self.class_promote.get(),
            "ranks": [min.get() for min in self.class_min_ranks] + [max.get() for max in self.class_max_ranks],
            "stats": [stat.get() for stat in self.class_stats]
        }
    
    def _get_item_data(self):
        return {
            "item": self.item_select.get(),
            "data": {
                key: (var.get() if isinstance(var, tk.BooleanVar) else var.get())
                for key, var in self.item_data.items()
            },
            "stats": [stat.get() for stat in self.item_stats],
            "bonuses": [bonus.get() for bonus in self.item_bonuses]
        }
    
    def _get_keybinds_data(self):
        return {
            "controller": self.controller.get(),
            "keys": [key.get() for key in self.checkboxes],
        }

    #endregion