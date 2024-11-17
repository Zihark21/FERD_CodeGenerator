import tkinter as tk
from tkinter import ttk
import json

characters = json.load(open('Character_Offsets.json', 'r'))
classes = json.load(open('Class_Offsets.json', 'r'))
items = json.load(open('Item_Offsets.json', 'r'))

char_sel = list(characters['Name'])
class_sel = list(classes['Name'])
item_sel = list(items['Name'])


class CodeGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Generator")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.character_tab()
        self.class_tab()
        self.items_tab()

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

        headers = ["Items", "Uses", "Equip", "MT", "Hit", "WT", "Crit"]
        for i, header in enumerate(headers):
            ttk.Label(self.item_table, text=header).grid(row=0, column=i)

        for row in range(1, 8):
            item_row = []
            item_combobox = ttk.Combobox(self.item_table, values=item_sel, width=25)
            item_combobox.grid(row=row, column=0)
            item_row.append(item_combobox)

            for col in range(1, 7):
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
                    "uses": row[1].get(),
                    "equip": row[2].get(),
                    "mt": row[3].get(),
                    "hit": row[4].get(),
                    "wt": row[5].get(),
                    "crit": row[6].get()
                } for row in self.item_entries
            ]
        }
        print(json.dumps(character_data, indent=4))

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
        print(json.dumps(class_data, indent=4))

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
        print(json.dumps(item_data, indent=4))

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeGeneratorGUI(root)
    root.mainloop()
