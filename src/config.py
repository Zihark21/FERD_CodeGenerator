import json, sys, os

# Base offsets
base_offsets = {
    "NTSC": {
        "Character": "80884E6C",
        "Class": "80B54010",
        "Item": "80B5FE10",
        "Skill": "8070EE14",
        "Model": "808C35F0"
    },
    "PAL": {
        "Character": "808773EC",
        "Class": "80B55670",
        "Item": "808D2170",
        "Skill": "80701394",
        "Model": "?"
    },
    "RR": {
        "Character": "808774AC",
        "Class": "80B554D0",
        "Item": "808D2230",
        "Skill": "80701E00",
        "Model": "?"
    }
}

keybinds = {
            "None - Always On": "",
            "Classic": [
                "Left", "Right", "Up", "Down", "A", "B", "X", "Y", "ZL", "ZR", "L", "R", "+", "-"
            ],
            "GameCube": [
                "Left", "Right", "Up", "Down", "A", "B", "X", "Y", "Z", "L", "R", "Start"
            ],
        }

# Define the path to the icon and JSON files inside the Assets folder
icon_path = os.path.join("assets", "RD_Custom.ico")

num_entry_width = 50
text_entry_width = 100
option_width = 75

# Function to load JSON data
def load_json(file_name):
    json_path = os.path.join("assets", file_name)
    with open(json_path, "r") as file:
        return json.load(file)

# Pull json data for each section
descriptions = load_json("descriptions.json")
lists = load_json("lists.json")

character_offset = load_json("character_offset.json")
character_ntsc = load_json("character_ntsc.json")
character_pal = load_json("character_pal.json")
character_rr = load_json("character_rr.json")
character_model = load_json("character_model.json")
character_support = load_json("character_support.json")

class_offset = load_json("class_offset.json")
class_id = load_json("class.json")

item_offset = load_json("item_offset.json")
item_id = load_json('item.json')

code_database = load_json("code_database.json")

# Define lists to be used in the GUI
character_list = sorted(set(list(character_ntsc)))
character_model_list = sorted(set(list(character_model)))
class_list = list(class_id)
item_list = list(item_id)

# Define lists that will be used for GUI and code generation
difficulties = lists['difficulties']
versions = lists['versions']
character_stats = lists['character_stats']
character_ranks = lists['character_ranks']
class_stats = lists['class_stats']
item_stats = lists['item_stats']
item_data = lists['item_data']
item_bonus = lists['item_bonus']
weapon_ranks = lists['weapon_ranks']
rank_map = lists['rank_map']
character_inventory = lists['character_inventory']
support_ranks = lists['support_ranks']
attack_type = lists['attack_type']
general = descriptions['general']
help = descriptions['help']
