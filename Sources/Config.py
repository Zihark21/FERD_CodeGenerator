import json
import sys
import os

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
    "RR": {
        "Character": "808774AC",
        "Class": "80B554D0",
        "Item": "808D2230",
        "Skill": "80701E00",
    }
}

DIFF_LIST = ['Easy', 'Medium/Hard']
VER_LIST = ["NTSC 1.0", "NTSC 1.01", "PAL", "Reverse Recruitment 5.3 - ViciousSal"]

KEYBINDS = {
            "None - Always On": "",
            "Classic": [
                "Left", "Right", "Up", "Down", "A", "B", "X", "Y", "ZL", "ZR", "L", "R", "+", "-"
            ],
            "GameCube": [
                "Left", "Right", "Up", "Down", "A", "B", "X", "Y", "Z", "L", "R", "Start"
            ],
        }

# Determine the base path
base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.abspath(".")

# Function to load JSON data
def load_json(file_name):
    with open(os.path.join(base_path, "Assets", file_name), "r") as file:
        return json.load(file)

# Pull offset data for each section
DESC = load_json("Descriptions.json")
CHAR = load_json("Characters.json")
CLASS = load_json("Classes.json")
ITEM = load_json("Items.json")
SKILL = load_json("Skills.json")
LISTS = load_json("Lists.json")
CODE_DATABASE = load_json("Code_Database.json")

# Define lists to be used in the GUI
CHAR_LIST = sorted(set(CHAR['NTSC'].keys()))
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