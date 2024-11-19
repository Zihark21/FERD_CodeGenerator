import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import json

characters = json.load(open('Character_Offsets.json', 'r'))
classes = json.load(open('Class_Offsets.json', 'r'))
items = json.load(open('Item_Offsets.json', 'r'))

char_sel = list(characters['Name'])
class_sel = list(classes['Name'])
item_sel = list(items['Name'])

def get_char_code(data, kb):
    output = []
    output.append(kb)
    char = data['character']
    if not char:
        return "No character selected!"
    for i in range(0,7):
        item = data['items'][i]['item']
        fname = data['items'][i]['forge_name']
        uses = data['items'][i]['uses']
        blessed = data['items'][i]['blessed']
        forged = data['items'][i]['forged']
        mt = data['items'][i]['mt']
        hit = data['items'][i]['hit']
        crit = data['items'][i]['crit']
        wt = data['items'][i]['wt']

        fname_off = characters[f'Item_{i+1}'][char]
        fstat_off = characters[f'Item_{i+1}_Forge'][char]

        if item:
            temp = f'04{characters[f'Item_{i+1}'][char][-6:]} {items['Offset'][item]}'
            output.append(temp)

        if uses:
            if not uses:
                uses = 0
            temp = f'00{characters[f'Item_{i+1}_Uses'][char][-6:]} 000000{hex(int(uses)).replace('0x', '').zfill(2).upper()}'
            output.append(temp)

        if blessed or forged or item:
            sts = 0
            if blessed:
                sts += int('10', 16)
            if forged:
                sts += int('20', 16)

                fname = ''
                for c in item:
                    fname += format(ord(c), "x")
                fname = fname.ljust(28, '0').upper()

                offset1 = hex(int(fname_off, 16) + 6).replace('0x', '').zfill(8).upper()
                temp1 = f'02{offset1[-6:]} 0000{fname[:4]}'
                output.append(temp1)

                offset2 = hex(int(fname_off, 16) + 8).replace('0x', '').zfill(8).upper()
                temp2 = f'04{offset2[-6:]} {fname[4:12]}'
                output.append(temp2)

                offset3 = hex(int(fname_off, 16) + 12).replace('0x', '').zfill(8).upper()
                temp3 = f'04{offset3[-6:]} {fname[12:20]}'
                output.append(temp3)

                offset4 = hex(int(fname_off, 16) + 16).replace('0x', '').zfill(8).upper()
                temp4 = f'04{offset4[-6:]} {fname[20:28]}'
                output.append(temp4)

            equip = hex(sts).replace('0x', '').zfill(2).upper()
            temp = f'00{characters[f'Item_{i+1}_Status'][char][-6:]} 000000{equip}'
            output.append(temp)

        if mt or hit or wt or crit:
            if mt == '':
                mt = 0
            if hit == '':
                hit = 0
            if wt == True:
                wt = 'E0'
            else:
                wt = '00'
            if crit == '':
                crit = 0
            temp1 = f'02{fstat_off[-6:]} 0000{hex(int(mt)).replace('0x', '').zfill(2).upper()}{hex(int(hit)).replace('0x', '').zfill(2).upper()}'
            off2 = hex(int(fstat_off, 16) + 2).replace('0x', '').zfill(8).upper()
            temp2 = f'02{off2[-6:]} 0000{hex(int(crit)).replace('0x', '').zfill(2).upper()}{wt}'
            output.append(temp1)
            output.append(temp2)
    
    output.append('E0000000 80008000')
    if len(output) == 2:
        return "No changes made!"
    else:
        return "\n".join(output)

def get_class_code(data):
    output = []
    output.append('20B54158 8070F8BC')

    cls = data['class']
    if not cls:
        return "No class selected!"

    rank_names = [
        'Sword_Rank',
        'Lance_Rank',
        'Axe_Rank',
        'Bow_Rank',
        'Knife_Rank',
        'Strike_Rank',
        'Fire_Rank',
        'Thunder_Rank',
        'Wind_Rank',
        'Light_Rank',
        'Dark_Rank',
        'Staff_Rank'
    ]

    for i, name in enumerate(rank_names):
        if data['weapon_ranks'][i]:
            if data['weapon_ranks'][i] == 'SS':
                val = '014B'
            elif data['weapon_ranks'][i] == 'S':
                val = '00FB'
            elif data['weapon_ranks'][i] == 'A':
                val = '00B5'
            elif data['weapon_ranks'][i] == 'B':
                val = '0079'
            elif data['weapon_ranks'][i] == 'C':
                val = '0047'
            elif data['weapon_ranks'][i] == 'D':
                val = '001F'
            elif data['weapon_ranks'][i] == 'E':
                val = '0001'

            temp = f'02{classes[name][cls][-6:]} 0000{val}'
            output.append(temp)
    
    stat_names = [
        'Base_WT',
        'Base_Move',
        'Skill_Capacity',
        'Max_HP',
        'Max_STR',
        'Max_MAG',
        'Max_SKL',
        'Max_SP',
        'Max_LCK',
        'Max_DEF',
        'Max_RES'
    ]

    for i, name in enumerate(stat_names):
        if data['stats'][i]:
            temp = f'00{classes[name][cls][-6:]} 000000{hex(int(data["stats"][i])).replace("0x", "").zfill(2).upper()}'
            output.append(temp)

    output.append('E0000000 80008000')
    if len(output) == 2:
        return "No changes made!"
    else:
        return "\n".join(output)

def get_item_code(data, kb):
    pass

def get_keybind_code(data):
    if data['controller'] == '':
        return '20B54158 8070F8BC'

    elif data['controller'] == 'Wiimote+Nunchuck':
        val = 0
        # Left
        if data['keys'][0]:
            val += int('1', 16)
        # Right
        if data['keys'][1]:
            val += int('2', 16)
        # Up
        if data['keys'][2]:
            val += int('8', 16)
        # Down
        if data['keys'][3]:
            val += int('4', 16)
        # A
        if data['keys'][4]:
            val += int('800', 16)
        # B
        if data['keys'][5]:
            val += int('400', 16)
        # C
        if data['keys'][6]:
            val += int('4000', 16)
        # Z
        if data['keys'][7]:
            val += int('2000', 16)
        # 1
        if data['keys'][8]:
            val += int('200', 16)
        # 2
        if data['keys'][9]:
            val += int('100', 16)
        # Plus
        if data['keys'][10]:
            val += int('10', 16)
        # Minus
        if data['keys'][11]:
            val += int('1000', 16)
        return f'UPDATE NUNCHUCK OFFSET {hex(val).replace('0x', '').zfill(8)}'

    elif data['controller'] == 'Classic Controller':
        val = 0
        # Left
        if data['keys'][0]:
            val += int('2', 16)
        # Right
        if data['keys'][1]:
            val += int('8000', 16)
        # Up
        if data['keys'][2]:
            val += int('1', 16)
        # Down
        if data['keys'][3]:
            val += int('4000', 16)
        # A
        if data['keys'][4]:
            val += int('10', 16)
        # B
        if data['keys'][5]:
            val += int('40', 16)
        # X
        if data['keys'][6]:
            val += int('8', 16)
        # Y
        if data['keys'][7]:
            val += int('20', 16)
        # ZL
        if data['keys'][8]:
            val += int('80', 16)
        # ZR
        if data['keys'][9]:
            val += int('4', 16)
        # L
        if data['keys'][10]:
            val += int('2000', 16)
        # R
        if data['keys'][11]:
            val += int('200', 16)
        # Plus
        if data['keys'][12]:
            val += int('400', 16)
        # Minus
        if data['keys'][13]:
            val += int('1000', 16)
        return f'283D79BA {hex(val).replace('0x', '').zfill(8)}'
    
    elif data['controller'] == 'GameCube Controller':
        # Left
        if data['keys'][0]:
            val += int('1', 16)
        # Right
        if data['keys'][0]:
            val += int('2', 16)
        # Up
        if data['keys'][0]:
            val += int('8', 16)
        # Down
        if data['keys'][0]:
            val += int('4', 16)
        # A
        if data['keys'][0]:
            val += int('100', 16)
        # B
        if data['keys'][0]:
            val += int('200', 16)
        # X
        if data['keys'][0]:
            val += int('400', 16)
        # Y
        if data['keys'][0]:
            val += int('800', 16)
        # Z
        if data['keys'][0]:
            val += int('2', 16)
        # L
        if data['keys'][0]:
            val += int('40', 16)
        # R
        if data['keys'][0]:
            val += int('20', 16)
        # Start
        if data['keys'][0]:
            val += int('1000', 16)
        return f'UPDATE GAMECUBE CONTROLLER OFFSET {hex(val).replace('0x', '').zfill(8)}'

class CodeGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FE:RD Code Creator")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.keybinds_tab()
        self.character_tab()
        self.class_tab()
        #self.items_tab()

    def keybinds_tab(self):
        new_tab = ttk.Frame(self.notebook)
        self.notebook.add(new_tab, text="Keybind Activation")

        self.keybinds = {
            "Wiimote+Nunchuck": [
                "Left",
                "Right",
                "Up",
                "Down",
                "A",
                "B",
                "C",
                "Z",
                "1",
                "2",
                "+",
                "-"
                
            ],
            'Classic Controller': [
                "Left",
                "Right",
                "Up",
                "Down",
                "A",
                "B",
                "X",
                "Y",
                "ZL",
                "ZR",
                "L",
                "R",
                "+",
                "-"
            ],
            'GameCube Controller': [
                "Left",
                "Right",
                "Up",
                "Down",
                "A",
                "B",
                "X",
                "Y",
                "Z",
                "L",
                "R",
                "Start"
            ]
        }

        # Dropdown Section
        ttk.Label(new_tab, text="Select Option:").grid(row=0, column=0, pady=10, padx=10)
        self.dropdown = ttk.Combobox(new_tab, values=list(self.keybinds.keys()))
        self.dropdown.grid(row=0, column=1, pady=10, padx=10)
        self.dropdown.bind("<<ComboboxSelected>>", self.update_checkboxes)

        # Separator
        ttk.Separator(new_tab, orient="horizontal").grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

        # Checkboxes Section
        ttk.Label(new_tab, text="Select Options:").grid(row=2, column=0, pady=10, padx=10)
        self.checkbox_frame = ttk.Frame(new_tab)
        self.checkbox_frame.grid(row=2, column=1, padx=10)
        self.checkboxes = []

    def update_checkboxes(self, event):
        for checkbox in self.checkbox_frame.winfo_children():
            checkbox.destroy()
        self.checkboxes.clear()

        selected_option = self.dropdown.get()
        if selected_option in self.keybinds:
            for i, option in enumerate(self.keybinds[selected_option]):
                var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(self.checkbox_frame, text=option, variable=var)
                checkbox.grid(row=i, column=0, sticky="w")
                self.checkboxes.append(var)

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()  # Clear the clipboard
        self.root.clipboard_append(text)  # Append the text to the clipboard
        messagebox.showinfo("Copied", "Character code copied to clipboard!")  # Notify the user

    def character_tab(self):
        char_tab = ttk.Frame(self.notebook)
        self.notebook.add(char_tab, text="Character")

        # Character Select Section
        ttk.Label(char_tab, text="Character Select:").grid(row=0, column=0, pady=10, padx=10)
        self.character_select = ttk.Combobox(char_tab, values=char_sel)
        self.character_select.grid(row=0, column=1, pady=10, padx=10)

        # Separator
        ttk.Separator(char_tab, orient="horizontal").grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

        # Items Section
        ttk.Label(char_tab, text="Items:").grid(row=2, column=0, pady=10, padx=10)
        self.item_entries = []
        self.item_table = ttk.Frame(char_tab)
        self.item_table.grid(row=2, column=1, padx=10)

        headers = ["Items", "Forge Name", "Uses", "Blessed", "Forged", "Might", "Hit", "Crit", "Weightless"]
        for i, header in enumerate(headers):
            ttk.Label(self.item_table, text=header).grid(row=0, column=i)

        for row in range(1, 9):
            item_row = []
            item_combobox = ttk.Combobox(self.item_table, values=item_sel, width=25)
            item_combobox.grid(row=row, column=0)
            item_row.append(item_combobox)

            for col in range(1, 9):
                if col == 3 or col == 4 or col == 8:
                    var = tk.BooleanVar(value=False)
                    if col == 3:
                        blessed_checkbox = ttk.Checkbutton(self.item_table, text="", variable=var)
                        blessed_checkbox.grid(row=row, column=2, sticky="w")
                    elif col == 4:
                        forged_checkbox = ttk.Checkbutton(self.item_table, text="", variable=var)
                        forged_checkbox.grid(row=row, column=3, sticky="w")
                    elif col == 8:
                        wt_checkbox = ttk.Checkbutton(self.item_table, text="", variable=var)
                        wt_checkbox.grid(row=row, column=7, sticky="w")
                    item_row.append(var)
                else:
                    if col == 1:
                        entry = ttk.Entry(self.item_table, width=20)
                        entry.grid(row=row, column=col)
                        item_row.append(entry)
                    else:
                        entry = ttk.Entry(self.item_table, width=5)
                        entry.grid(row=row, column=col)
                        item_row.append(entry)

            self.item_entries.append(item_row)

        # Separator
        ttk.Separator(char_tab, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)

        # Generate Button
        generate_button = ttk.Button(char_tab, text="Generate", command=self.generate_character)
        generate_button.grid(row=4, column=1, pady=10)

    def generate_character(self):
        character_data = {
            "character": self.character_select.get(),
            "items": [
                {
                    "item": row[0].get(),
                    "forge_name": row[1].get(),
                    "uses": row[2].get(),
                    "blessed": row[3].get(),
                    "forged": row[4].get(),
                    "mt": row[5].get(),
                    "hit": row[6].get(),
                    "crit": row[7].get(),
                    "wt": row[8].get(),
                } for row in self.item_entries
            ]
        }

        keybinds_data = {
            "controller": self.dropdown.get(),
            "keys": [key.get() for key in self.checkboxes]
        }

        key_code = get_keybind_code(keybinds_data)

        output = get_char_code(character_data, key_code)

        # Create a new window for the message box
        message_window = tk.Toplevel(self.root)
        message_window.title("Character Code")
        
        # Add a label to display the output
        output_label = tk.Label(message_window, text=output, justify="left")
        output_label.pack(padx=10, pady=10)

        if output != "No character selected!" and output != "No changes made!":
            # Add a button to copy to clipboard
            copy_button = ttk.Button(message_window, text="Copy to Clipboard", command=lambda: self.copy_to_clipboard(output))
            copy_button.pack(pady=5)

    def class_tab(self):
        class_tab = ttk.Frame(self.notebook)
        self.notebook.add(class_tab, text="Class")

        # Class Select Section
        ttk.Label(class_tab, text="Class Select:").grid(row=0, column=0, pady=10, padx=10)
        self.class_select = ttk.Combobox(class_tab, values=class_sel, width=40)
        self.class_select.grid(row=0, column=1, pady=10, padx=10)

        # Separator
        ttk.Separator(class_tab, orient="horizontal").grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

        # Weapon Ranks Section
        ttk.Label(class_tab, text="Weapon Ranks:").grid(row=2, column=0, pady=10, padx=10)
        weapon_ranks = ["Sword Rank", "Lance Rank", "Axe Rank", "Bow Rank", "Knife Rank", "Strike Rank",
                        "Fire Rank", "Thunder Rank", "Wind Rank", "Light Rank", "Dark Rank", "Staff Rank"]
        self.weapon_rank_comboboxes = []

        weapon_rank_frame = ttk.Frame(class_tab)
        weapon_rank_frame.grid(row=2, column=1, padx=10)
        for i, rank in enumerate(weapon_ranks):
            ttk.Label(weapon_rank_frame, text=rank).grid(row=i, column=0)
            combobox = ttk.Combobox(weapon_rank_frame, values=["SS", "S", "A", "B", "C", "D", "E"], width=5)
            combobox.grid(row=i, column=1)
            self.weapon_rank_comboboxes.append(combobox)

        # Separator
        ttk.Separator(class_tab, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)

        # Stats Section
        ttk.Label(class_tab, text="Stats:").grid(row=4, column=0, pady=10, padx=10)
        stats = ["Base WT", "Base Move", "Skill Capacity", "Max HP", "Max STR", "Max MAG", "Max SKL",
                 "Max SP", "Max LCK", "Max DEF", "Max RES"]
        self.stats_entries = []

        stats_frame = ttk.Frame(class_tab)
        stats_frame.grid(row=4, column=1, padx=10)
        for i, stat in enumerate(stats):
            ttk.Label(stats_frame, text=stat).grid(row=i, column=0)
            entry = ttk.Entry(stats_frame, width=5)
            entry.grid(row=i, column=1)
            self.stats_entries.append(entry)

        # Separator
        ttk.Separator(class_tab, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)

        # Generate Button
        generate_button = ttk.Button(class_tab, text="Generate", command=self.generate_class)
        generate_button.grid(row=6, column=1, pady=10)

    def generate_class(self):
        class_data = {
            "class": self.class_select.get(),
            "weapon_ranks": [cb.get() for cb in self.weapon_rank_comboboxes],
            "stats": [entry.get() for entry in self.stats_entries]
        }

        output = get_class_code(class_data)

        # Create a new window for the message box
        message_window = tk.Toplevel(self.root)
        message_window.title("Class Code")
        
        # Add a label to display the output
        output_label = tk.Label(message_window, text=output, justify="left")
        output_label.pack(padx=10, pady=10)

        if output != "No class selected!" and output != "No changes made!":
            # Add a button to copy to clipboard
            copy_button = ttk.Button(message_window, text="Copy to Clipboard", command=lambda: self.copy_to_clipboard(output))
            copy_button.pack(pady=5)

    def items_tab(self):
        items_tab = ttk.Frame(self.notebook)
        self.notebook.add(items_tab, text="Items")

        # Item Select Section
        ttk.Label(items_tab, text="Item Select:").grid(row=0, column=0, pady=10, padx=10)
        self.item_select = ttk.Combobox(items_tab, values=item_sel, width=25)
        self.item_select.grid(row=0, column=1, pady=10, padx=10)

        # Separator
        ttk.Separator(items_tab, orient="horizontal").grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

        # Misc Weapon Data Section
        ttk.Label(items_tab, text="Misc Weapon Data:").grid(row=2, column=0, pady=10, padx=10)
        misc_data_labels = ["Attack Type", "Weapon Rank", "EXP Gain", "Lock", "CharLock", "Infinite", "Brave", "Heal"]
        self.misc_data = {}

        misc_data_frame = ttk.Frame(items_tab)
        misc_data_frame.grid(row=2, column=1, padx=10)
        for i, label in enumerate(misc_data_labels):
            ttk.Label(misc_data_frame, text=label).grid(row=i, column=0)
            if label == "Attack Type":
                self.misc_data[label] = ttk.Combobox(misc_data_frame, values=["STR", "MAG"])
            elif label == "Weapon Rank":
                self.misc_data[label] = ttk.Combobox(misc_data_frame, values=["SS", "S", "A", "B", "C", "D", "E"])
            elif label in ["Lock", "CharLock", "Infinite", "Brave", "Heal"]:
                self.misc_data[label] = tk.BooleanVar()
                ttk.Checkbutton(misc_data_frame, variable=self.misc_data[label]).grid(row=i, column=1)
                continue
            else:
                self.misc_data[label] = ttk.Entry(misc_data_frame, width=5)

            self.misc_data[label].grid(row=i, column=1)

        # Separator
        ttk.Separator(items_tab, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)

        # Equip Bonuses Section
        ttk.Label(items_tab, text="Equip Bonuses:").grid(row=4, column=0, pady=10, padx=10)
        equip_bonus_labels = ["HP Increase", "STR Increase", "MAG Increase", "SKL Increase", "SP Increase",
                              "LCK Increase", "DEF Increase", "RES Increase", "Move Increase", "CN/WT Increase"]
        self.equip_bonus_entries = []

        equip_bonus_frame = ttk.Frame(items_tab)
        equip_bonus_frame.grid(row=4, column=1, padx=10)
        for i, label in enumerate(equip_bonus_labels):
            ttk.Label(equip_bonus_frame, text=label).grid(row=i, column=0)
            entry = ttk.Entry(equip_bonus_frame, width=5)
            entry.grid(row=i, column=1)
            self.equip_bonus_entries.append(entry)

        # Separator
        ttk.Separator(items_tab, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)

        # Generate Button
        generate_button = ttk.Button(items_tab, text="Generate", command=self.generate_item)
        generate_button.grid(row=6, column=1, pady=10)

    def generate_item(self):
        item_data = {
            "item": self.item_select.get(),
            "misc_data": {key: (var.get() if isinstance(var, tk.BooleanVar) else var.get())
                        for key, var in self.misc_data.items()},
            "equip_bonuses": [entry.get() for entry in self.equip_bonus_entries]
        }

        output = get_item_code(item_data)  # Get the output from get_char_code

        # Create a new window for the message box
        message_window = tk.Toplevel(self.root)
        message_window.title("Item Code")
        
        # Add a label to display the output
        output_label = tk.Label(message_window, text=output, justify="left")
        output_label.pack(padx=10, pady=10)

        # Add a button to copy to clipboard
        copy_button = ttk.Button(message_window, text="Copy to Clipboard", command=lambda: self.copy_to_clipboard(output))
        copy_button.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeGeneratorGUI(root)
    root.mainloop()