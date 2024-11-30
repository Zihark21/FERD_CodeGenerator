import json, sys, os

# Base offsets
BASE = {
    "NTSC": {
        "Character": "80884E6C",
        "Class": "80B54010",
        "Item": "80B5FE10",
        "Skill": "8070EE14",
    },
    "PAL": {
        "Character": "808773EC",
        "Class": "80B55670",
        "Item": "808D2170",
        "Skill": "80701394",
    },
}

# Determine the base path
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

# Pull offset data for each section
DESC = json.load(open(os.path.join(base_path, "Assets", "Descriptions.json"), "r"))
CHAR = json.load(open(os.path.join(base_path, "Assets", "Characters.json"), "r"))
CLASS = json.load(open(os.path.join(base_path, "Assets", "Classes.json"), "r"))
ITEM = json.load(open(os.path.join(base_path, "Assets", "Items.json"), "r"))
SKILL = json.load(open(os.path.join(base_path, "Assets", "Skills.json"), "r"))
LISTS = json.load(open(os.path.join(base_path, "Assets", "Lists.json"), "r"))
CODE_DATABASE = json.load(open(os.path.join(base_path, "Assets", "Code_Database.json"), "r"))

# Define lists to be used in the GUI
CHAR_LIST = sorted(set(list(CHAR["NTSC"].keys()) + list(CHAR["PAL"].keys())))
CLASS_LIST = list(CLASS["ID"])[1:]
ITEM_LIST = list(ITEM["ID"])[1:]
SECTION_HEADER = ("TkDefaultFont", 10, "bold")

# Define lists that will be used for GUI and code generation
CHAR_STATS = LISTS["CHAR_STATS"]
CHAR_RANKS = LISTS["CHAR_RANKS"]
CLASS_STATS = LISTS["CLASS_STATS"]
ITEM_STATS = LISTS["ITEM_STATS"]
ITEM_DATA = LISTS["ITEM_DATA"]
ITEM_BONUS = LISTS["ITEM_BONUS"]