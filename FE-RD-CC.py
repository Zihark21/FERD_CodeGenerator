# %%
# Imports

import tkinter as tk, ctypes, os, sys
from tkinter import ttk

dpi = ctypes.windll.shcore.SetProcessDpiAwareness(True)

# %%
# Lists

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

CHAR = {
    "NTSC": {
        "Nolan": 0,
        "Laura": 1,
        "Meg": 2,
        "Volug": 3,
        "Tauroneo": 4,
        "Jill": 5,
        "Zihark": 6,
        "Fiona": 7,
        "Micaiah": 8,
        "Edward": 9,
        "Leonardo": 10,
        "Rafael": 11,
        "Nailah": 12,
        "Elincia": 13,
        "Marcia": 14,
        "Brom": 15,
        "Black Knight": 16,
        "Nephenee": 17,
        "Lucia": 18,
        "Lethe": 19,
        "Mordecai": 20,
        "Sothe": 21,
        "Calill": 22,
        "Ike": 23,
        "Titania": 24,
        "Soren": 25,
        "Mist": 26,
        "Rolf": 27,
        "Nealuchi": 28,
        "Leanne": 29,
        "Ilyana": 30,
        "Haar": 31,
        "Boyd": 32,
        "Oscar": 33,
        "Shinon": 34,
        "Aran": 35,
        "Gatrie": 36,
        "Rhys": 37,
        "Heather": 38,
        "Mia": 39,
        "Lyre": 40,
        "Ranulf": 41,
        "Kyza": 42,
        "Reyson": 43,
        "Tormod": 44,
        "Muarim": 45,
        "Vika": 46,
        "Sigrun": 47,
        "Tanith": 48,
        "Sanaki": 49,
        "Naesala": 50,
        "Bastian": 51,
        "Oliver": 52,
        "Volke": 53,
        "Caineghis": 54,
        "Giffca": 55,
        "Kurthnaga": 56,
        "Ena": 57,
        "Renning": 58,
        "Geoffrey": 59,
        "Kieran": 60,
        "Astrid": 61,
        "Makalov": 62,
        "Danved": 63,
        "Janaff": 88,
        "Ulki": 89,
        "Pelleas": 119,
        "Skrimir": 125,
        "Tibarn": 126,
        "Stefan": 135,
    },
    "PAL": {
        "Nolan": 0,
        "Laura": 1,
        "Meg": 2,
        "Volug": 3,
        "Micaiah": 4,
        "Edward": 5,
        "Leonardo": 6,
        "Tauroneo": 7,
        "Jill": 8,
        "Zihark": 9,
        "Rafiel": 10,
        "Nailah": 11,
        "Elincia": 12,
        "Marcia": 13,
        "Brom": 14,
        "Nephenee": 16,
        "Lucia": 17,
        "Sothe": 18,
        "Lethe": 19,
        "Mordecai": 20,
        "Calill": 21,
        "Ike": 22,
        "Titania": 23,
        "Ilyana": 24,
        "Soren": 25,
        "Nealuchi": 26,
        "Leanne": 27,
        "Aran": 28,
        "Haar": 29,
        "Mist": 30,
        "Rolf": 31,
        "Boyd": 32,
        "Oscar": 33,
        "Fiona": 34,
        "Shinon": 35,
        "Gatrie": 36,
        "Heather": 37,
        "Tormod": 38,
        "Muarim": 39,
        "Vika": 40,
        "Rhys": 41,
        "Mia": 42,
        "Lyre": 43,
        "Ranulf": 44,
        "Kysha": 45,
        "Reyson": 46,
        "Sigrun": 47,
        "Tanith": 48,
        "Sanaki": 49,
        "Geoffrey": 50,
        "Kieran": 51,
        "Astrid": 52,
        "Makalov": 53,
        "Danved": 54,
        "Naesala": 55,
        "Bastian": 56,
        "Volke": 57,
        "Caineghis": 58,
        "Giffca": 59,
        "Kurthnaga": 60,
        "Ena": 61,
        "Renning": 62,
        "Janaff": 86,
        "Ulki": 87,
        "Skrimir": 107,
        "Tibarn": 108,
        "Stefan": 126,
        "Pelleas": 144,
        "Oliver": 'Unknown',
    },
    "OFFSET": {
        "Character": 1008,
        "Class": 20,
        "Control": 24,
        "Affiliation": 32,
        "Level": 34,
        "EXP": 35,
        "Commander": 50,
        "Move_Status": 51,
        "Current_HP": 56,
        "CN-WT": 57,
        "Move-Boots": 58,
        "Affinity": 60,
        "HP": 61,
        "STR": 62,
        "MAG": 63,
        "SKL": 64,
        "SP": 65,
        "LCK": 66,
        "DEF": 67,
        "RES": 68,
        "Skill": 80,
        "Skill_Status": 84,
        "Skill_Step": 8,
        "Item": 224,
        "Item_Uses": 228,
        "Item_Status": 229,
        "Item_Forge": 254,
        "Item_Step": 40,
        "Sword_Rank": 504,
        "Lance_Rank": 506,
        "Axe_Rank": 508,
        "Bow_Rank": 510,
        "Knife_Rank": 512,
        "Strike_Rank": 514,
        "Fire_Rank": 516,
        "Thunder_Rank": 518,
        "Wind_Rank": 520,
        "Light_Rank": 522,
        "Dark_Rank": 524,
        "Staff_Rank": 526,
        "Biorhythm": 670,
    },
}

CLASS = {
    "ID": {
        "Hero (Ike)": 0,
        "Vanguard (Ike)": 1,
        "Myrmidon (Edward)": 2,
        "Swordmaster male (Zihark - Edward)": 3,
        "Swordmaster female (Mia)": 4,
        "Swordmaster disciples of order": 5,
        "Trueblade male (Stefan - Zihark - Edward)": 6,
        "Trueblade female (Mia)": 7,
        "Soldier (Aran)": 8,
        "Halberdier male (Danved - Aran)": 9,
        "Halberdier female (Nephenee)": 10,
        "Halberdier disciples of order": 11,
        "Sentinel male (Danved - Aran)": 12,
        "Sentinel female (Nephenee)": 13,
        "Fighter (Nolan)": 14,
        "Warrior (Boyd - Nolan)": 15,
        "Warrior disciples of order": 16,
        "Reaver (Boyd - Nolan)": 17,
        "Archer (Leonardo)": 18,
        "Sniper (Shinon - Rolf - Leonardo)": 19,
        "Sniper disciples of order": 20,
        "Marksman (Shinon - Rolf - Leonardo)": 21,
        "Armor lance": 22,
        "Armor axe": 23,
        "Armor sword male": 24,
        "Armor sword female (Meg)": 25,
        "Lance general (Tauroneo - Gatrie)": 26,
        "Axe general (Brom)": 27,
        "Sword general male": 28,
        "Sword general female (Meg)": 29,
        "Lance general disciples of order": 30,
        "Axe general disciples of order": 31,
        "Sword general disciples of order": 32,
        "Marshal lance (Tauroneo - Gatrie)": 33,
        "Marshal axe (Brom)": 34,
        "Marshal sword (Meg)": 35,
        "Marshal zelgius": 36,
        "Black knight": 37,
        "Thief": 38,
        "Rogue male (Sothe)": 39,
        "Rogue female (Heather)": 40,
        "Whisper male (Sothe)": 41,
        "Whisper female (Heather)": 42,
        "Assassin (Volke)": 43,
        "Bandit": 44,
        "Fire mage": 45,
        "Thunder mage male": 46,
        "Thunder mage female (Ilyana)": 47,
        "Wind mage": 48,
        "Light mage (Micaiah)": 49,
        "Fire sage male (Tormod)": 50,
        "Fire sage female (Calill)": 51,
        "Thunder sage male": 52,
        "Thunder sage female (Ilyana)": 53,
        "Wind sage (Soren)": 54,
        "Light sage (Micaiah)": 55,
        "Dark sage (Pelleas)": 56,
        "Fire sage disciples of order": 57,
        "Thunder sage disciples of order": 58,
        "Wind sage disciples of order": 59,
        "Arch sage fire male (Tormod)": 60,
        "Arch sage fire female (Calill)": 61,
        "Arch sage dark (Pelleas)": 62,
        "Arch sage thunder (Ilyana)": 63,
        "Arch sage wind (Bastian - Soren)": 64,
        "Light priestess (Micaiah)": 65,
        "Empress (Sanaki)": 66,
        "Chancellor (Sephiran\\/Lehran)": 67,
        "Druid": 68,
        "Druid disciples of order": 69,
        "Summoner": 70,
        "Priest male": 71,
        "Priest female": 72,
        "Bishop male": 73,
        "Bishop female": 74,
        "Bishop valtome\\/numida\\/disciples of order": 75,
        "Saint male": 76,
        "Saint female": 77,
        "Saint lekain": 78,
        "Cleric": 79,
        "Valkyrie": 80,
        "Sword knight": 81,
        "Lance knight male": 82,
        "Lance knight female": 83,
        "Axe knight": 84,
        "Bow knight": 85,
        "Blade paladin": 86,
        "Lance paladin male": 87,
        "Lance paladin female": 88,
        "Axe paladin male": 89,
        "Axe paladin female": 90,
        "Bow paladin male": 91,
        "Bow paladin female": 92,
        "Blade paladin disciples of order": 93,
        "Lance paladin disciples of order": 94,
        "Axe paladin disciples of order": 95,
        "Bow paladin disciples of order": 96,
        "Gold knight sword": 97,
        "Gold knight axe male": 98,
        "Gold knight axe female": 99,
        "Silver knight lance male": 100,
        "Silver knight lance female": 101,
        "Silver knight bow": 102,
        "Pegasus knight": 103,
        "Falcon knight": 104,
        "Falcon knight disciples of order": 105,
        "Seraph knight": 106,
        "Queen": 107,
        "Draco knight male": 108,
        "Draco knight female": 109,
        "Dragonmaster male": 110,
        "Dragonmaster female": 111,
        "Dragonmaster disciples of order": 112,
        "Dragon lord male": 113,
        "Dragon lord female": 114,
        "Lion red untransformed": 115,
        "Lion red transformed": 116,
        "Lion black untransformed": 117,
        "Lion black transformed": 118,
        "Lion king untransformed": 119,
        "Lion king transformed": 120,
        "Tiger untransformed": 121,
        "Tiger transformed": 122,
        "Cat male untransformed": 123,
        "Cat male transformed": 124,
        "Cat female untransformed": 125,
        "Cat female transformed": 126,
        "Wolf untransformed": 127,
        "Wolf transformed": 128,
        "Wolf queen untransformed": 129,
        "Wolf queen transformed": 130,
        "Hawk untransformed": 131,
        "Hawk transformed": 132,
        "Hawk king untransformed": 133,
        "Hawk king transformed": 134,
        "Raven male untransformed": 135,
        "Raven male transformed": 136,
        "Raven female untransformed": 137,
        "Raven female transformed": 138,
        "Raven king untransformed": 139,
        "Raven king transformed": 140,
        "Heron reyson untransformed": 141,
        "Heron reyson transformed": 142,
        "Heron rafiel untransformed": 143,
        "Heron rafiel transformed": 144,
        "Heron leanne untransformed": 145,
        "Heron leanne transformed": 146,
        "Red dragon male untransformed": 147,
        "Red dragon male transformed": 148,
        "Red dragon female untransformed": 149,
        "Red dragon female transformed": 150,
        "White dragon untransformed": 151,
        "White dragon transformed": 152,
        "Dragon king untransformed": 153,
        "Dragon king transformed": 154,
        "Dragon prince untransformed": 155,
        "Dragon prince transformed": 156,
        "Spirit fire": 157,
        "Spirit thunder": 158,
        "Spirit wind": 159,
        "Order incarnate aura": 160,
        "Order incarnate ashera": 161,
        "Pilgrim": 162,
        "Vendor": 163,
        "Citizen old man": 164,
        "Citizen male": 165,
        "Citizen female": 166,
        "Citizen child male": 167,
        "Citizen child female": 168,
        "Horse": 169,
        "Hero can have an ss rank in all types": 170,
    },
    "OFFSET": {
        "Class": 284,
        "Previous_Class": 16,
        "Next_Class": 20,
        "Skill_1": 36,
        "Skill_1_Status": 40,
        "Skill_Step": 8,
        "Min_Sword_Rank": 184,
        "Min_Lance_Rank": 186,
        "Min_Axe_Rank": 188,
        "Min_Bow_Rank": 190,
        "Min_Knife_Rank": 192,
        "Min_Strike_Rank": 194,
        "Min_Fire_Rank": 196,
        "Min_Thunder_Rank": 198,
        "Min_Wind_Rank": 200,
        "Min_Light_Rank": 202,
        "Min_Dark_Rank": 204,
        "Min_Staff_Rank": 206,
        "Max_Sword_Rank": 208,
        "Max_Lance_Rank": 210,
        "Max_Axe_Rank": 212,
        "Max_Bow_Rank": 214,
        "Max_Knife_Rank": 216,
        "Max_Strike_Rank": 218,
        "Max_Fire_Rank": 220,
        "Max_Thunder_Rank": 222,
        "Max_Wind_Rank": 224,
        "Max_Light_Rank": 226,
        "Max_Dark_Rank": 228,
        "Max_Staff_Rank": 230,
        "Base_WT": 244,
        "Base_Move": 245,
        "Skill_Capacity": 247,
        "Max_HP": 260,
        "Max_STR": 261,
        "Max_MAG": 262,
        "Max_SKL": 263,
        "Max_SP": 264,
        "Max_LCK": 265,
        "Max_DEF": 266,
        "Max_RES": 267,
    },
}

ITEM = {
    "ID": {
        "Slim Sword": 0,
        "Bronze Sword": 1,
        "Iron Sword": 2,
        "Steel Sword": 3,
        "Silver Sword": 4,
        "Iron Blade": 5,
        "Steel Blade": 6,
        "Silver Blade": 7,
        "Venin Edge": 8,
        "Brave Sword": 9,
        "Killing Edge": 10,
        "Wyrmslayer": 11,
        "Wo Dao": 12,
        "Caladbolg": 13,
        "Wind Edge": 14,
        "Storm Sword": 15,
        "Tempest Blade": 16,
        "Vague katti": 17,
        "Florete": 18,
        "Ettard": 19,
        "Ragnell": 20,
        "Alondite": 21,
        "Amiti": 22,
        "Slim Lance": 23,
        "Bronze Lance": 24,
        "Iron Lance": 25,
        "Steel Lance": 26,
        "Silver Lance": 27,
        "Iron Greatlance": 28,
        "Stl Greatlance": 29,
        "Slvr Greatlance": 30,
        "Venin Lance": 31,
        "Brave Lance": 32,
        "Killer Lance": 33,
        "Horseslayer": 34,
        "Javelin": 35,
        "Short spear": 36,
        "Spear": 37,
        "Wishblade": 38,
        "Bronze Axe": 39,
        "Iron Axe": 40,
        "Steel Axe": 41,
        "Silver Axe": 42,
        "Iron Poleaxe": 43,
        "Steel Poleaxe": 44,
        "Silver Poleaxe": 45,
        "Venin Axe": 46,
        "Brave Axe": 47,
        "Killer Axe": 48,
        "Hammer": 49,
        "Hand Axe": 50,
        "Short Axe": 51,
        "Tomahawk": 52,
        "Tarvos": 53,
        "Urvan": 54,
        "Bronze Bow": 55,
        "Iron Bow": 56,
        "Steel Bow": 57,
        "Silver Bow": 58,
        "Iron Longbow": 59,
        "Steel Longbow": 60,
        "Silver Longbow": 61,
        "Venin Bow": 62,
        "Killer Bow": 63,
        "Brave Bow": 64,
        "Rolf's Bow": 65,
        "Silencer": 66,
        "Lughnasadh": 67,
        "Double Bow": 68,
        "Bowgun": 69,
        "Crossbow": 70,
        "Taksh": 71,
        "Aqqar": 72,
        "Arbalest": 73,
        "Ballista": 74,
        "Iron Ballista": 75,
        "Killer Ballista": 76,
        "Onager": 77,
        "Bronze Knife": 78,
        "Iron Knife": 79,
        "Steel Knife": 80,
        "Silver Knife": 81,
        "Bronze dagger": 82,
        "Iron dagger": 83,
        "Steel dagger": 84,
        "Silver dagger": 85,
        "Kard": 86,
        "Stiletto": 87,
        "Beast Killer": 88,
        "Peshkatz": 89,
        "Baselard": 90,
        "Fire": 91,
        "Elfire": 92,
        "Arcfire": 93,
        "Bolganone": 94,
        "Rexflame": 95,
        "Cymbeline": 96,
        "Meteor": 97,
        "Thunder": 98,
        "Elthunder": 99,
        "Arcthunder": 100,
        "Thoron": 101,
        "Rexbolt": 102,
        "Bolting": 103,
        "Wind": 104,
        "Eliwind": 105,
        "Arcwind": 106,
        "Tornado": 107,
        "Rexcaliber": 108,
        "Blizzard": 109,
        "Light": 110,
        "Ellight": 111,
        "Shine": 112,
        "Nosferatu": 113,
        "Valaura": 114,
        "Rexaura": 115,
        "Purge": 116,
        "Thani": 117,
        "Creiddylad": 118,
        "Worm": 119,
        "Carreau": 120,
        "Verrine": 121,
        "Balberith": 122,
        "Fenrir": 123,
        "Fang-lion-a": 124,
        "Fang-lion-s": 125,
        "Fang-lion-ss": 126,
        "Great Fang-lion-a": 127,
        "Great Fang-lion-s": 128,
        "Great Fang-lion-ss": 129,
        "Fang-tiger-a": 130,
        "Fang-tiger-s": 131,
        "Fang-tiger-ss": 132,
        "Claw-cat-a": 133,
        "Claw-cat-s": 134,
        "Claw-cat-ss": 135,
        "Fang-wolf-a": 136,
        "Fang-wolf-s": 137,
        "Fang-wolf-ss": 138,
        "Great Fang-wolf-a": 139,
        "Great Fang-wolf-s": 140,
        "Great Fang-wolf-ss": 141,
        "Talon-hawk-a": 142,
        "Talon-hawk-s": 143,
        "Talon-hawk-ss": 144,
        "Great Talon-hawk-a": 145,
        "Great Talon-hawk-s": 146,
        "Great Talon-hawk-ss": 147,
        "Beak-raven-a": 148,
        "Beak-raven-s": 149,
        "Beak-raven-ss": 150,
        "Great Beak-raven-a": 151,
        "Great Beak-raven-s": 152,
        "Great Beak-raven-ss": 153,
        "Breath-red dragon-a": 154,
        "Breath-red dragon-s": 155,
        "Breath-red dragon-ss": 156,
        "Breath-white dragon-a": 157,
        "Breath-white dragon-s": 158,
        "Breath-white dragon-ss": 159,
        "Breath-dragon prince-a": 160,
        "Breath-dragon prince-s": 161,
        "Breath-dragon prince-ss": 162,
        "Breath-dragon king-a": 163,
        "Breath-dragon king-s": 164,
        "Breath-dragon king-ss": 165,
        "Fire Tail": 166,
        "Thunder Tail": 167,
        "Wind Tail": 168,
        "Judge Staff": 180,
        "Judge-25 (Usable)": 182,
        "Judge-5 (Usable)": 183,
        "Vortex-bug": 184,
        "Heal": 185,
        "Mend": 186,
        "Recover": 187,
        "Physic": 188,
        "Fortify": 189,
        "Restore": 190,
        "Silence": 191,
        "Elsilence": 192,
        "Sleep": 193,
        "Elsleep": 194,
        "Rescue": 195,
        "Rewarp": 196,
        "Torch": 197,
        "Hammerne": 198,
        "Unlock": 199,
        "Ward": 200,
        "Matrona": 201,
        "Ashera Staff": 202,
        "Seraph Robe": 203,
        "Energy Drop": 204,
        "Spirit Dust": 205,
        "Secret Book": 206,
        "Speedwing": 207,
        "Ashera Icon": 208,
        "Dracoshield": 209,
        "Talisman": 210,
        "Boots": 211,
        "Statue Frag": 212,
        "Master Seal": 213,
        "Master Crown": 214,
        "Holy crown": 215,
        "Satori Sign": 216,
        "Chest Key": 217,
        "Door Key": 218,
        "Herb": 219,
        "Vulnerary": 220,
        "Concoction": 221,
        "Elixer": 222,
        "Olivi Grass": 223,
        "Pure Water": 224,
        "Antitoxin": 225,
        "Panacea": 226,
        "Torch (Item)": 227,
        "Arms scroll": 228,
        "Silver card": 229,
        "White gem": 230,
        "Blue gem": 231,
        "Red gem": 232,
        "Spectre Card": 234,
        "Reaper Card": 235,
        "Daemon Card": 236,
        "Frey Bomb(Un)": 237,
        "Shine Barrier": 238,
        "Howl": 239,
        "Shriek": 240,
        "Quickclaw": 241,
        "Maelstrom": 242,
        "Wildheart": 243,
        "Blessing": 244,
        "Boon": 245,
        "Blood Gide": 246,
        "White Pool": 247,
        "Night Gide": 248,
        "Shade": 249,
        "Stillness": 250,
        "Corrosion": 251,
        "Disarm": 252,
        "Discipline": 253,
        "Miracle": 254,
        "Resolve": 255,
        "Wrath": 256,
        "Cancel": 257,
        "Adept": 258,
        "Counter": 259,
        "Vantage": 260,
        "Flourish": 261,
        "Mercy": 262,
        "Pass": 263,
        "Nihil": 264,
        "Fortune": 265,
        "Nullify": 266,
        "Provoke": 267,
        "Daunt": 268,
        "Paragon": 269,
        "Renewal": 270,
        "Imbue": 271,
        "Blossom": 272,
        "Tempest": 273,
        "Serenity": 274,
        "Celerity": 275,
        "Savior": 276,
        "Guard": 277,
        "Pavise": 278,
        "Beastfoe": 279,
        "Birdfoe": 280,
        "Dragonfoe": 281,
        "Parity": 282,
        "Gamble": 283,
        "Smite": 284,
        "Laguz Stone": 290,
        "Laguz Stone blue": 291,
        "Wild Stone": 292,
        "Laguz Gem": 293,
        "Coin": 294,
        "Rudol Gem": 295,
    },
    "OFFSET": {
        "Item": 80,
        "Weapon_Type": 18,
        "Attack_Type": 19,
        "Weapon_Rank": 25,
        "EXP_Gain": 26,
        "Weapon_Uses": 27,
        "Might": 28,
        "Hit": 29,
        "Weight": 30,
        "Crit": 31,
        "Min_Range": 32,
        "Max_Range": 33,
        "HP_Increase": 34,
        "STR_Increase": 35,
        "MAG_Increase": 36,
        "SKL_Increase": 37,
        "SP_Increase": 38,
        "LCK_Increase": 39,
        "DEF_Increase": 40,
        "RES_Increase": 41,
        "Move_Increase": 42,
        "CN-WT_Increase": 43,
        "Unlock": 56,
        "Infinite": 57,
        "Heal": 58,
        "Char_Unlock": 59,
        "Brave": 62,
    },
}

SKILL = {
    "ID": {
        "Canto": 0,
        "Shove": 1,
        "Steal": 2,
        "Galdrar": 3,
        "Crit +5": 4,
        "Crit +10": 5,
        "Crit +15": 6,
        "Crit +20": 7,
        "Crit +25": 8,
        "Aurora": 9,
        "Formshift": 10,
        "Aether": 11,
        "Astra": 12,
        "Impale": 13,
        "Colossus": 14,
        "Deadeye": 15,
        "Luna": 16,
        "Eclipse": 17,
        "Bane": 18,
        "Lethality": 19,
        "Flare": 20,
        "Corona": 21,
        "Sol": 22,
        "Stun": 23,
        "Roar": 24,
        "Rend": 25,
        "Savage": 26,
        "Tear": 27,
        "Ire": 28,
        "Sacrifice": 29,
        "Glare": 30,
        "Insight": 31,
        "Vigilance": 32,
        "Mantle": 33,
        "Wildheart1": 34,
        "Howl": 35,
        "Shriek": 36,
        "Quickclaw": 37,
        "Maelstrom": 38,
        "Wildheart2": 39,
        "Blessing": 40,
        "Boon": 41,
        "Blood tide": 42,
        "White pool": 43,
        "Night tide": 44,
        "Shade": 45,
        "Stillness": 46,
        "Corrosion": 47,
        "Disarm": 48,
        "Discipline": 49,
        "Miracle": 50,
        "Resolve": 51,
        "Wrath": 52,
        "Cancel": 53,
        "Adept": 54,
        "Counter": 55,
        "Vantage": 56,
        "Flourish": 57,
        "Mercy": 58,
        "Pass": 59,
        "Nihil": 60,
        "Fortune": 61,
        "Nullify": 62,
        "Provoke": 63,
        "Daunt": 64,
        "Paragon": 65,
        "Renewal": 66,
        "Imbue": 67,
        "Blossom": 68,
        "Tempest": 69,
        "Serenity": 70,
        "Celerity": 71,
        "Savior": 72,
        "Guard": 73,
        "Pavise": 74,
        "Beastfoe": 75,
        "Birdfoe": 76,
        "Dragonfoe": 77,
        "Parity": 78,
        "Gamble": 79,
        "Smite": 80,
    },
    "OFFSET": {
        "Skill": 80,
        "Learnable": 27,
        "Cost": 30,
    },
}

CHAR_LIST = sorted(set(list(CHAR["NTSC"].keys()) + list(CHAR["PAL"].keys())))
CLASS_LIST = list(CLASS["ID"])
ITEM_LIST = list(ITEM["ID"])

# %%
# Description for info tab

desc = {
    "intro": "Welcome to the Fire Emblem Radiant Dawn Code Creator! This tool will allow you to easily create Gecko Codes to change and add a variety of data to your game. Please see each section below for more details.",
    "Misc Information": "Text Input Fields - Forge Name has a max character count of 26. All other input fields are for numeric input with a max value of 255.\nDropdowns - All dropdowns are pre-populated and can only take values from the list provided. You can type in the name of the character, class or item, but it needs to be exact or the code will not find it.",
    "Keybind Activation Tab": "Allows users to select a controller type and configure keybindings required to activate the code. This tab only works in conjunction with the character tab. The codes generated from Class and Items are codes that need to be always on.",
    "Character Tab": "Lets users select a character and configure their items, including forge names, uses, and various attributes. Make sure to pair with input in the keybinds tab to activate based on custom button pairing! If no keybinds are selected, the code defaults to an always on status and will repeatedly write to your character.",
    "Class Tab": "Allows users to select a class and configure max weapon ranks and stats.",
    "Items Tab": "Allows users to select an item and configure its miscellaneous data and equip bonuses."
}

# %%
# UDF

def set_version(ver):
    global VERSION, NTSC_MOD
    if ver == 'NTSC 1.00':
        VERSION = 'NTSC'
        NTSC_MOD = -int('80', 16)
    elif ver == 'NTSC 1.01' or ver == '':
        VERSION = 'NTSC'
        NTSC_MOD = 0
    elif ver == 'PAL':
        VERSION = 'PAL'
        NTSC_MOD = 0

def get_offset(name, data, opt):

    # Check data for Step
    if 'Step' in data:
        if data == 'Item_Step':
            return CHAR['OFFSET']['Item_Step']
        elif data == 'Skill_Step':
            return CHAR['OFFSET']['Skill_Step']

    # Check if the option is 'Char'
    elif opt == 'Char':

        # Get the ID for the character name
        id = CHAR[VERSION][name]

        if data == 'Character':
            # Calculate the offset for the character
            off = int(BASE[VERSION]['Character'], 16) + NTSC_MOD + (CHAR['OFFSET']['Character'] * id)

        else:
            # Calculate the offset for the specific data type
            off = int(BASE[VERSION]['Character'], 16) + NTSC_MOD + (CHAR['OFFSET']['Character'] * id) + CHAR['OFFSET'][data]

        # Convert the offset to a hexadecimal string, remove '0x', convert to uppercase, and pad with zeros
        off = hex(off).replace('0x', '').upper().zfill(8)
        return off
    
    # Check if the option is 'Class'
    elif opt == 'Class':
        # Get the ID for the class name
        id = CLASS['ID'][name]

        if data == 'Class':
            # Calculate the offset for the class
            off = int(BASE[VERSION]['Class'], 16) + NTSC_MOD + (CLASS['OFFSET']['Class'] * id)

        else:
            # Calculate the offset for the specific data type
            off = int(BASE[VERSION]['Class'], 16) + NTSC_MOD + (CLASS['OFFSET']['Class'] * id) + CLASS['OFFSET'][data]

        # Convert the offset to a hexadecimal string, remove '0x', convert to uppercase, and pad with zeros
        off = hex(off).replace('0x', '').upper().zfill(8)
        return off
    
    # Check if the option is 'Item'
    elif opt == 'Item':
        # Get the ID for the item name
        id = ITEM['ID'][name]

        if data == 'Item':
            # Calculate the offset for the item
            off = int(BASE[VERSION]['Item'], 16) + NTSC_MOD + (ITEM['OFFSET']['Item'] * id)

        else:
            # Calculate the offset for the specific data type
            off = int(BASE[VERSION]['Item'], 16) + NTSC_MOD + (ITEM['OFFSET']['Item'] * id) + ITEM['OFFSET'][data]

        # Convert the offset to a hexadecimal string, remove '0x', convert to uppercase, and pad with zeros
        off = hex(off).replace('0x', '').upper().zfill(8)
        return off

def get_char_code(data, kb):

    # Create code output and start with Keybind
    output = []
    output.append(kb)

    # Character Select Validation
    char = data['character']
    if not char:
        return "No character selected!"
    
    if VERSION == 'PAL' and char == 'Oliver':
        return "Oliver ID unknown in the PAL version of the game. Please report on my discord."

    # Define Step Counts
    item_step = get_offset(char, 'Item_Step', 'Char')
    skill_step = get_offset(char, 'Skill_Step', 'Char')
    
    # Loop through all 7 rows of input
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

        # Get item offsets
        item_off = hex(int(get_offset(char, 'Item', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)
        item_uses_off = hex(int(get_offset(char, 'Item_Uses', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)
        item_status_off = hex(int(get_offset(char, 'Item_Status', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)
        item_forge_off = hex(int(get_offset(char, 'Item_Forge', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)

        # If item is populated
        if item:
            # Get item ID
            item_code = get_offset(item, 'Item', 'Item')

            # Create item code and add to output
            temp = f'04{item_off[-6:]} {item_code}'
            output.append(temp)

        # If uses or item is populated
        if uses or item:
            if uses == '':
                uses = 0

            # Error handling for uses
            try:
                uses = int(uses)

                # Check if uses is within range
                if uses > 255:
                    return f'Error: Uses for {item} is too high! Please enter a value between 0 and 255.'

                # Default to 80 uses if not populated
                if uses == 0:
                    uses = 80

                # Create uses code and add to output
                temp = f'00{item_uses_off[-6:]} 000000{hex(uses).replace('0x', '').zfill(2).upper()}'
                output.append(temp)

            # Error handling for uses
            except ValueError:
                return f'Error: Uses for {item} is not a number! Please enter a value between 0 and 255.'
        
        # If blessed = True or forged = True or item is populated
        if blessed or forged or item:

            # Determine equip status
            sts = 0

            if blessed:
                sts += int('10', 16)

            if forged:
                sts += int('20', 16)
            
            # Create status code and add to output
            equip = hex(sts).replace('0x', '').zfill(2).upper()
            temp = f'00{item_status_off[-6:]} 000000{equip}'
            output.append(temp)

            # If forged = True
            if forged:
                # Create variable for forge name
                fnamecode = ''

                # Error handling for forge name
                if len(fname) > 26:
                        return f'Error: Forge Name for {item} is too long! Please enter a name with 26 characters or less.'
                elif fname and 0 < len(fname) <= 26:
                    # If forge name is populated, convert to hex
                    for c in fname:
                        fnamecode += format(ord(c), "x").zfill(2)
                else:
                    # If forge name does not meet requirements, default forge name to item name
                    for c in item:
                        fnamecode += format(ord(c), "x").zfill(2)
                
                # Pad forge name to 60 digits (26 characters in hex)
                fnamecode = fnamecode.ljust(52, '0').upper()

                # Create forge name code and add to output
                j = 0

                # Loop through forge name and add to output
                for k in range(0, 7):
                    # First set is 16 bytes, so it needs to be handled differently
                    if k == 0:
                        offset = hex(int(item_off, 16) + 6).replace('0x', '').zfill(8).upper()
                        temp = f'02{offset[-6:]} 0000{fnamecode[:4]}'

                    # The rest of the sets are 32 bytes
                    else:
                        offset = hex(int(item_off, 16) + 8 + j).replace('0x', '').zfill(8).upper()
                        temp = f'04{offset[-6:]} {fnamecode[4+(j*2):12+(j*2)]}'

                        # Checks for when name stops and removes empty lines
                        if temp[-8:] != '00000000':
                            output.append(temp)
                        j += 4

                # If mt, hit, wt, or crit is populated
                if mt or hit or wt or crit:

                    # Default values if not populated
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

                    # Error handling for mt, hit, wt, and crit
                    try:
                        # Validation
                        mt = int(mt)
                        hit = int(hit)
                        crit = int(crit)
                        if mt > 255 or hit > 255 or crit > 255:
                            return f'Error: Stat for {item} is too high! Please enter a value between 0 and 255.'
                        
                        # Create stat codes and add to output, 16 bytes each
                        temp1 = f'02{item_forge_off[-6:]} 0000{hex(mt).replace('0x', '').zfill(2).upper()}{hex(hit).replace('0x', '').zfill(2).upper()}'
                        off2 = hex(int(item_forge_off, 16) + 2).replace('0x', '').zfill(8).upper()
                        temp2 = f'02{off2[-6:]} 0000{hex(crit).replace('0x', '').zfill(2).upper()}{wt}'
                        output.append(temp1)
                        output.append(temp2)
                    
                    # Error handling for mt, hit, wt, and crit
                    except ValueError:
                        return f'Error: Stat for {item} is not a number! Please enter a value between 0 and 255.'
    
    # Add end code to output
    output.append('E0000000 80008000')

    # If only kb and end code, return no changes made
    if len(output) == 2:
        return "No changes made!"
    else:
        return "\n".join(output)

def get_class_code(data):

    # Create code output and append start code
    output = []
    output.append('20B54158 8070F8BC')

    # Class Select Validation
    cls = data['class']
    if not cls:
        return "No class selected!"

    # Define rank names
    rank_names = [
        'Max_Sword_Rank',
        'Max_Lance_Rank',
        'Max_Axe_Rank',
        'Max_Bow_Rank',
        'Max_Knife_Rank',
        'Max_Strike_Rank',
        'Max_Fire_Rank',
        'Max_Thunder_Rank',
        'Max_Wind_Rank',
        'Max_Light_Rank',
        'Max_Dark_Rank',
        'Max_Staff_Rank'
    ]

    # Loop through all 12 rank names and determine input level
    for i, name in enumerate(rank_names):

        # Get data input
        input = data['weapon_ranks'][i]
        offset = get_offset(cls, name, 'Class')

        # If data is populated
        if input:
            if input == 'SS':
                val = '014B'
            elif input == 'S':
                val = '00FB'
            elif input == 'A':
                val = '00B5'
            elif input == 'B':
                val = '0079'
            elif input == 'C':
                val = '0047'
            elif input == 'D':
                val = '001F'
            elif input == 'E':
                val = '0001'
            else:
                return f'Error: Invalid weapon rank for {name.replace('_', ' ')}! Please select a valid rank.'

            # Create weapon rank code and add to output
            temp = f'02{offset[-6:]} 0000{val}'
            output.append(temp)
    
    # Define stat names
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

    # Loop through all 11 stat names and determine input
    for i, name in enumerate(stat_names):

        # Get data input
        input = data['stats'][i]
        offset = get_offset(cls, name, 'Class')

        if input:
            # Error handling for stats
            try:
                # Validation
                num = int(input)
                if num > 255:
                    return f'Error: Stat for {name.replace('_', ' ')} is too high! Please enter a value between 0 and 255.'
                
                # Get offset for stat name and create code
                temp = f'00{offset[-6:]} 000000{hex(num).replace("0x", "").zfill(2).upper()}'
                output.append(temp)
            
            # Error handling for stats
            except ValueError:
                return f'Error: Stat for {name} is not a number! Please enter a value between 0 and 255.'

    # Add end code to output
    output.append('E0000000 80008000')

    # If only start and end code, return no changes made
    if len(output) == 2:
        return "No changes made!"
    else:
        return "\n".join(output)

def get_item_code(data):

    # Create code output and append start code
    output = []
    output.append('20B54158 8070F8BC')

    # Item Select Validation
    item = data['item']
    if not item:
        return "No item selected!"
    
    # Define item names
    w_opts = ['Attack_Type', 'Weapon_Rank', 'EXP_Gain', 'Unlock', 'Char_Unlock', 'Infinite', 'Brave', 'Heal']
    d_opts = ['Attack Type', 'Weapon Rank', 'EXP Gain', 'Unlock', 'CharUnlock', 'Infinite', 'Brave', 'Heal']

    # Loop through all 8 item names and determine input
    for w, d in zip(w_opts, d_opts):

        # Get data input
        input = data['misc_data'][d]

        # Get offset for item name
        offset = get_offset(item, w, 'Item')

        # If data is populated
        if input:
            # Determine attack type
            if d == 'Attack Type':
                if input == 'STR':
                    val = '00'
                elif input == 'MAG':
                    val = '06'
                else:
                    return f'Error: Invalid attack type for {item}! Please select a valid type.'
                
                # Create attack type code and add to output
                temp = f'00{offset[-6:]} 000000{val}'
                output.append(temp)

            # Determine weapon rank
            elif d == 'Weapon Rank':
                if input == 'SS':
                    val = '014B'
                elif input == 'S':
                    val = '00FB'
                elif input == 'A':
                    val = '00B5'
                elif input == 'B':
                    val = '0079'
                elif input == 'C':
                    val = '0047'
                elif input == 'D':
                    val = '001F'
                elif input == 'E':
                    val = '0001'
                else:
                    return f'Error: Invalid weapon rank for {item}! Please select a valid rank.'
                
                # Create weapon rank code and add to output
                temp = f'02{offset[-6:]} 0000{val}'
                output.append(temp)

            # Determine EXP gain
            elif d == 'EXP Gain':
                temp = f'00{offset[-6:]} 000000{hex(int(data["misc_data"][d])).replace("0x", "").zfill(2).upper()}'
                output.append(temp)

            # Determine Unlock
            elif d == 'Unlock':
                if input:
                    val = '00'
                    temp = f'00{offset[-6:]} 000000{val}'
                    output.append(temp)

            # Determine Infinite and Brave
            elif d in ['Infinite', 'Brave']:
                if input:
                    val = '01'
                    temp = f'00{offset[-6:]} 000000{val}'
                    output.append(temp)

            # Determine Char Unlock
            elif d == 'CharUnlock':
                if input:
                    val = '0000'
                    temp = f'02{offset[-6:]} 0000{val}'
                    output.append(temp)

            # Determine Heal
            elif d == 'Heal':
                if input:
                    val = '10'
                    temp = f'00{offset[-6:]} 000000{val}'
                    output.append(temp)

    # Define equip bonuses
    eq_bonus = ['HP_Increase', 'STR_Increase', 'MAG_Increase', 'SKL_Increase', 'SP_Increase', 'LCK_Increase', 'DEF_Increase', 'RES_Increase', 'Move_Increase', 'CN-WT_Increase']

    # Loop through all 10 equip bonuses and determine input
    for i, bonus in enumerate(eq_bonus):

        # Get data input and offset for equip bonus
        input = data['equip_bonuses'][i]
        offset = get_offset(item, bonus, 'Item')

        # If data is populated
        if input:
            try:
                # Validation
                num = int(input)
                if num > 255:
                    return f'Error: Equip Bonus for {bonus.replace("_", " ")} is too high! Please enter a value between 0 and 255.'
                
                # Create equip bonus code and add to output
                temp = f'00{offset[-6:]} 000000{hex(int(input)).replace("0x", "").zfill(2).upper()}'
                output.append(temp)

            # Error handling for equip bonuses
            except ValueError:
                return f'Error: Equip Bonus for {bonus} is not a number! Please enter a value between 0 and 255.'

    # Add end code to output
    output.append('E0000000 80008000')

    # If only start and end code, return no changes made
    if len(output) == 2:
        return "No changes made!"
    else:
        return "\n".join(output)

def get_keybind_code(data):
    val = 0
    if data['controller'] == '':
        return '20B54158 8070F8BC'
    elif data['controller'] == 'Wiimote+Nunchuck':
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
        return f'28 {hex(val).replace('0x', '').zfill(8)}'

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
            val += int('100', 16)
        # B
        if data['keys'][5]:
            val += int('200', 16)
        # X
        if data['keys'][6]:
            val += int('400', 16)
        # Y
        if data['keys'][7]:
            val += int('800', 16)
        # Z
        if data['keys'][8]:
            val += int('10', 16)
        # L
        if data['keys'][9]:
            val += int('40', 16)
        # R
        if data['keys'][10]:
            val += int('20', 16)
        # Start
        if data['keys'][11]:
            val += int('1000', 16)
        return f'283D7928 {hex(val).replace('0x', '').zfill(8)}'

# %%
# GUI

class CodeGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FE:RD Code Creator")

        # Set no resize
        self.root.resizable(False, False)
        
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, 'FE-RD.ico')
        else:
            icon_path = 'FE-RD.ico'
        
        self.root.iconbitmap(icon_path)

        # Set dark mode colors
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#000000', foreground='#ffffff')
        style.configure('TNotebook.Tab', background='#000000', foreground='#ffffff')
        style.map('TNotebook.Tab', background=[('selected', '#2e2e2e')])
        
        # Configure text color for various widgets
        style.configure('TFrame', background='#2e2e2e')
        style.configure('TLabel', background='#2e2e2e', foreground='#ffffff')
        style.configure('TEntry', fieldbackground='#ffffff', foreground='#000000')
        style.configure('TCombobox', fieldbackground='#ffffff', foreground='#000000')
        style.map('TCombobox', fieldbackground=[('readonly', '#ffffff')], foreground=[('readonly', '#000000')])
        style.configure('TCheckbutton', background='#2e2e2e', foreground='#000000')

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.info_tab()
        self.options_tab()
        self.character_tab()
        self.class_tab()
        self.items_tab()

    def copy_and_close(self, code, message_window):
        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        message_window.destroy()

    def output_code(self, code):
        # Create a new window for the message box
        message_window = tk.Toplevel(self.root)
        message_window.title("Code")
        message_window.configure(bg='#2e2e2e')
        
        # Add a label to display the output
        output_label = ttk.Label(message_window, text=code, justify="left")
        output_label.pack(padx=10, pady=10)

        if code not in ["No character selected!", "No class selected!", "No item selected!", "No changes made!"] and 'Error:' not in code:
            # Add a button to copy to clipboard
            copy_button = ttk.Button(message_window, text="Copy to Clipboard", command=lambda: self.copy_and_close(code, message_window))
            copy_button.pack(pady=5)

    def info_tab(self):
        info_tab = ttk.Frame(self.notebook)
        self.notebook.add(info_tab, text="Info")

        desc_frame = ttk.Frame(info_tab)
        desc_frame.pack(fill="both", expand=True)

        i = 3
        for tab in list(desc):
            if tab == "intro":
                label = ttk.Label(desc_frame, text=desc[tab], wraplength=950, justify="center")
                label.grid(row=0, column=0, pady=10, columnspan=3)
                ttk.Separator(desc_frame, orient="horizontal").grid(row=1, column=0, columnspan=3, sticky="ew")
            else:
                label = ttk.Label(desc_frame, text=tab, wraplength=150)
                label.grid(row=i, column=0, pady=10, sticky="w")
                ttk.Separator(desc_frame, orient="vertical").grid(row=i, column=1, padx=5, rowspan=1, sticky="ns")
                label = ttk.Label(desc_frame, text=desc[tab], wraplength=800, justify="left")
                label.grid(row=i, column=2, pady=10, sticky="w")
                ttk.Separator(desc_frame, orient="horizontal").grid(row=i+1, column=0, columnspan=3, sticky="ew")
            i += 2

    def options_tab(self):
        options_tab = ttk.Frame(self.notebook)
        self.notebook.add(options_tab, text="Options")

        self.keybinds = {
            "": "",
            # "Wiimote+Nunchuck": [
            #     "Left",
            #     "Right",
            #     "Up",
            #     "Down",
            #     "A",
            #     "B",
            #     "C",
            #     "Z",
            #     "1",
            #     "2",
            #     "+",
            #     "-"
                
            # ],
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

        # Controller Section
        controller_frame = ttk.Frame(options_tab)
        controller_frame.grid(row=0, column=0, pady=10, sticky="nsew")

        # Create controller label and combobox
        ttk.Label(controller_frame, text="Controller:").grid(row=0, column=0, padx=5)
        self.controller = ttk.Combobox(controller_frame, values=list(self.keybinds.keys()))
        self.controller.grid(row=0, column=1, padx=10, pady=10)
        self.controller.bind("<<ComboboxSelected>>", self.update_checkboxes)

        # Separator
        ttk.Separator(controller_frame, orient="horizontal").grid(row=1, column=0, columnspan=2, sticky="ew")

        # Checkboxes Section
        self.checkboxes = []
        self.checkbox_frame = ttk.Frame(controller_frame)
        self.checkbox_frame.grid(row=2, column=0, columnspan=2)

        # Controller and Version Separator
        ttk.Separator(options_tab, orient="vertical").grid(row=0, column=2, rowspan=99, sticky="ns")

        # Create version section
        version_frame = ttk.Frame(options_tab)
        version_frame.grid(row=0, column=3, pady=10, sticky="nsew")

        # Create version label
        ttk.Label(version_frame, text="Version:").grid(row=0, column=0, padx=5)
        self.version = ttk.Combobox(version_frame, values=['NTSC 1.00', 'NTSC 1.01', 'PAL'])
        self.version.grid(row=0, column=1, padx=10, pady=10)

    def update_checkboxes(self, event):
        for checkbox in self.checkbox_frame.winfo_children():
            checkbox.destroy()
        self.checkboxes = []
        
        selected_option = self.controller.get()
        if selected_option == "":
            pass
        elif selected_option in self.keybinds:
            ttk.Label(self.checkbox_frame, text="Buttons").grid(row=0, column=0, rowspan=len(self.keybinds[selected_option]), padx=10)
            ttk.Separator(self.checkbox_frame, orient="vertical").grid(row=0, column=1, rowspan=len(self.keybinds[selected_option]), sticky="ns", pady=5)
            for i, option in enumerate(self.keybinds[selected_option]):
                ttk.Label(self.checkbox_frame, text=option).grid(row=i, column=3, padx=5, sticky="e")
                var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(self.checkbox_frame, variable=var)
                checkbox.grid(row=i, column=4)
                self.checkboxes.append(var)

    def character_tab(self):
        char_tab = ttk.Frame(self.notebook)
        self.notebook.add(char_tab, text="Character")

        #region Row 0

        # Character Select Section
        char_frame = ttk.Frame(char_tab)
        char_frame.grid(row=0, column=0, pady=10, sticky="nsew")
        
        ttk.Label(char_frame, text="Character Select:").grid(row=0, column=0, padx=5)
        self.character_select = ttk.Combobox(char_frame, values=CHAR_LIST)
        self.character_select.grid(row=0, column=1)

        #endregion

        # Row 1 Separator
        ttk.Separator(char_tab, orient="horizontal").grid(row=1, column=0, columnspan=2, sticky="ew")

        #region Row 2

        # Items Section
        self.item_entries = []
        self.item_table = ttk.Frame(char_tab)
        self.item_table.grid(row=2, column=0)

        headers = ["Items", "Forge Name", "Uses", "Blessed", "Forged", "Might", "Hit", "Crit", "Weightless"]
        for i, header in enumerate(headers):
            ttk.Label(self.item_table, text=header).grid(row=0, column=i)

        for row in range(1, 8):
            item_row = []
            item_combobox = ttk.Combobox(self.item_table, values=ITEM_LIST, width=25)
            item_combobox.grid(row=row, column=0, padx=1, pady=1)
            item_row.append(item_combobox)

            for col in range(1, 9):
                if col == 3 or col == 4 or col == 8:
                    var = tk.BooleanVar(value=False)
                    if col == 3:
                        blessed_checkbox = ttk.Checkbutton(self.item_table, text="", variable=var)
                        blessed_checkbox.grid(row=row, column=col)
                    elif col == 4:
                        forged_checkbox = ttk.Checkbutton(self.item_table, text="", variable=var)
                        forged_checkbox.grid(row=row, column=col)
                    elif col == 8:
                        wt_checkbox = ttk.Checkbutton(self.item_table, text="", variable=var)
                        wt_checkbox.grid(row=row, column=col)
                    item_row.append(var)
                else:
                    if col == 1:
                        entry = ttk.Entry(self.item_table, width=20)
                        entry.grid(row=row, column=col, padx=1)
                        item_row.append(entry)
                    else:
                        entry = ttk.Entry(self.item_table, width=5)
                        entry.grid(row=row, column=col, padx=1)
                        item_row.append(entry)

            self.item_entries.append(item_row)

        #endregion

        # Row 3 Separator
        ttk.Separator(char_tab, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew")

        # Row 4 Generate Button
        generate_button = ttk.Button(char_tab, text="Generate", command=self.generate_character)
        generate_button.grid(row=4, column=0, sticky="nsew")

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
            "controller": self.controller.get(),
            "keys": [key.get() for key in self.checkboxes]
        }
        
        version = self.version.get()
        set_version(version)

        key_code = get_keybind_code(keybinds_data)
        output = get_char_code(character_data, key_code)
        self.output_code(output)

    def class_tab(self):
        class_tab = ttk.Frame(self.notebook)
        self.notebook.add(class_tab, text="Class")

        #region Row 0

        # Class Select Section
        class_frame = ttk.Frame(class_tab)
        class_frame.grid(row=0, column=0, pady=10, sticky="nsew")
        
        ttk.Label(class_frame, text="Class Select:").grid(row=0, column=0, padx=5)
        self.class_select = ttk.Combobox(class_frame, values=CLASS_LIST, width=40)
        self.class_select.grid(row=0, column=1)

        #endregion

        # Row 1 Separator
        ttk.Separator(class_tab, orient="horizontal").grid(row=1, column=0, columnspan=1, sticky="ew")

        #region Row 2

        # Create frame for weapon ranks and stats
        ranks_stats = ttk.Frame(class_tab)
        ranks_stats.grid(row=2, column=0)

        # Weapon Ranks Section
        ttk.Label(ranks_stats, text="Weapon Ranks").grid(row=0, column=0, pady=5, columnspan=2)
        weapon_ranks = ["Sword Rank", "Lance Rank", "Axe Rank", "Bow Rank", "Knife Rank", "Strike Rank",
                        "Fire Rank", "Thunder Rank", "Wind Rank", "Light Rank", "Dark Rank", "Staff Rank"]
        self.weapon_rank_comboboxes = []

        for i, rank in enumerate(weapon_ranks):
            ttk.Label(ranks_stats, text=rank).grid(row=i+1, column=0, padx=5, sticky="e")
            combobox = ttk.Combobox(ranks_stats, values=["SS", "S", "A", "B", "C", "D", "E"], width=5)
            combobox.grid(row=i+1, column=1, padx=5, pady=1)
            self.weapon_rank_comboboxes.append(combobox)
        
        # Separator
        ttk.Separator(ranks_stats, orient="vertical").grid(row=0, column=2, rowspan=13, sticky="ns")

        # Stats Section
        ttk.Label(ranks_stats, text="Stats").grid(row=0, column=3, pady=5, columnspan=2)
        stats = ["Base WT", "Base Move", "Skill Capacity", "Max HP", "Max STR", "Max MAG", "Max SKL",
                "Max SP", "Max LCK", "Max DEF", "Max RES"]
        self.stats_entries = []

        for i, stat in enumerate(stats):
            ttk.Label(ranks_stats, text=stat).grid(row=i+1, column=3, padx=5, sticky="e")
            entry = ttk.Entry(ranks_stats, width=5)
            entry.grid(row=i+1, column=4, pady=1)
            self.stats_entries.append(entry)

        #endregion

        # Row 3 Separator
        ttk.Separator(class_tab, orient="horizontal").grid(row=3, column=0, columnspan=1, sticky="ew")

        # Row 4 Generate Button
        generate_button = ttk.Button(class_tab, text="Generate", command=self.generate_class)
        generate_button.grid(row=4, column=0, sticky="nsew")

    def generate_class(self):
        class_data = {
            "class": self.class_select.get(),
            "weapon_ranks": [cb.get() for cb in self.weapon_rank_comboboxes],
            "stats": [entry.get() for entry in self.stats_entries]
        }

        version = self.version.get()
        set_version(version)

        output = get_class_code(class_data)

        self.output_code(output)

    def items_tab(self):
        items_tab = ttk.Frame(self.notebook)
        self.notebook.add(items_tab, text="Items")

        #region Row 0

        # Item Select Section
        item_frame = ttk.Frame(items_tab)
        item_frame.grid(row=0, column=0, pady=10, sticky="nsew")
        
        ttk.Label(item_frame, text="Item Select:").grid(row=0, column=0, padx=5)
        self.item_select = ttk.Combobox(item_frame, values=ITEM_LIST, width=25)
        self.item_select.grid(row=0, column=1)

        #endregion

        # Row 1 Separator
        ttk.Separator(items_tab, orient="horizontal").grid(row=1, column=0, columnspan=5, sticky="ew")

        #region Row 2

        data_bonus = ttk.Frame(items_tab)
        data_bonus.grid(row=2, column=0)

        # Misc Weapon Data Section
        ttk.Label(data_bonus, text="Misc Weapon Data").grid(row=0, column=0, columnspan=2, pady=5)
        misc_data_labels = ["Attack Type", "Weapon Rank", "EXP Gain", "Unlock", "CharUnlock", "Infinite", "Brave", "Heal"]
        self.misc_data = {}

        for i, label in enumerate(misc_data_labels):
            ttk.Label(data_bonus, text=label).grid(row=i+1, column=0, padx=5, sticky="e")
            if label == "Attack Type":
                self.misc_data[label] = ttk.Combobox(data_bonus, values=["STR", "MAG"], width=5)
            elif label == "Weapon Rank":
                self.misc_data[label] = ttk.Combobox(data_bonus, values=["SS", "S", "A", "B", "C", "D", "E"], width=5)
            elif label in ["Unlock", "CharUnlock", "Infinite", "Brave", "Heal"]:
                self.misc_data[label] = tk.BooleanVar()
                ttk.Checkbutton(data_bonus, variable=self.misc_data[label]).grid(row=i+1, column=1)
                continue
            else:
                self.misc_data[label] = ttk.Entry(data_bonus, width=5)

            self.misc_data[label].grid(row=i+1, column=1, padx=5, pady=1)

        # Separator
        ttk.Separator(data_bonus, orient="vertical").grid(row=0, column=2, rowspan=11, sticky="ns", pady=5)

        # Equip Bonuses Section
        ttk.Label(data_bonus, text="Equip Bonuses").grid(row=0, column=3, columnspan=2, pady=5)
        equip_bonus_labels = ["HP Increase", "STR Increase", "MAG Increase", "SKL Increase", "SP Increase",
                                "LCK Increase", "DEF Increase", "RES Increase", "Move Increase", "CN/WT Increase"]
        self.equip_bonus_entries = []

        for i, label in enumerate(equip_bonus_labels):
            ttk.Label(data_bonus, text=label).grid(row=i+1, column=3, padx=5, sticky="e")
            entry = ttk.Entry(data_bonus, width=5)
            entry.grid(row=i+1, column=4, padx=0, pady=1)
            self.equip_bonus_entries.append(entry)

        #endregion

        # Row 3 Separator
        ttk.Separator(items_tab, orient="horizontal").grid(row=3, column=0, columnspan=5, sticky="ew")

        # Row 4 Generate Button
        generate_button = ttk.Button(items_tab, text="Generate", command=self.generate_item)
        generate_button.grid(row=4, column=0, sticky="nsew")

    def generate_item(self):
        item_data = {
            "item": self.item_select.get(),
            "misc_data": {key: (var.get() if isinstance(var, tk.BooleanVar) else var.get())
                        for key, var in self.misc_data.items()},
            "equip_bonuses": [entry.get() for entry in self.equip_bonus_entries]
        }

        version = self.version.get()
        set_version(version)

        output = get_item_code(item_data)  # Get the output from get_char_code

        self.output_code(output)

    def other_tab(self):
        pass

# %%
# Main

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeGeneratorGUI(root)
    root.mainloop()


