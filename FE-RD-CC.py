# %%
# Imports

import tkinter as tk, ctypes, os, sys, re
from tkinter import ttk

dpi = ctypes.windll.shcore.SetProcessDpiAwareness(True)

# %%
# Lists and Variables

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
        "All": 0,
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
        "All": 0,
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
        "Weight": 57,
        "Move": 58,
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
        "All": 0,
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
        "All": 0,
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
        "Weapon_Rank": 24,
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
CLASS_LIST = list(CLASS["ID"])[1:]
ITEM_LIST = list(ITEM["ID"])[1:]
SECTION_HEADER = ("TkDefaultFont", 10, "bold")

CHAR_STATS = [
    'Level',
    'EXP',
    'Current_HP',
    'Weight',
    'Move',
    'HP',
    'STR',
    'MAG',
    'SKL',
    'SP',
    'LCK',
    'DEF',
    'RES',
]

CHAR_RANKS = [
    "Sword_Rank",
    "Lance_Rank",
    "Axe_Rank",
    "Bow_Rank",
    "Knife_Rank",
    "Strike_Rank",
    "Fire_Rank",
    "Thunder_Rank",
    "Wind_Rank",
    "Light_Rank",
    "Dark_Rank",
    "Staff_Rank",
]

CLASS_STATS = [
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

ITEM_STATS = [
    "Weapon_Uses",
    "Might",
    "Hit",
    "Weight",
    "Crit",
    "Min_Range",
    "Max_Range"
    ]

ITEM_DATA = [
    "Attack_Type",
    "Weapon_Rank",
    "EXP_Gain",
    "Unlock",
    "Char_Unlock",
    "Infinite",
    "Brave",
    "Heal"
]

ITEM_BONUS = [
    "HP_Increase",
    "STR_Increase",
    "MAG_Increase",
    "SKL_Increase",
    "SP_Increase",
    "LCK_Increase",
    "DEF_Increase",
    "RES_Increase",
    "Move_Increase",
    "CN-WT_Increase"
]

CODE_DATABASE = {
    'Game Clear Count': {
        'DESC': 'Info:\nReplace XX below with (number desired + 1) and convert to hex.\n\nCode:',
        'NTSC': '023CABD6 000000XX',
        'PAL': '003C3577 000000XX'
    },
    'Infinite Money': {
        'DESC': 'Info:\nGold set to 50,000\n\nCode:',
        'NTSC': '083CAB50 0000C350\n20020004 00000000',
        'PAL': ''
    },
    'Infinite BEXP': {
        'DESC': 'Info:\nBEXP is set to 50,000\n\nCode:\n',
        'NTSC': '083CAB5C 47435000\n20020004 00000000',
        'PAL': ''
    },
    'BEXP Level Cap': {
        'DESC': 'Info:\nReplace XX with cap. 03 is default.\nUse 08 for all stats possible.\nUse 01 for a challenge. (:\n\nCode:',
        'NTSC': '0006D8EB 000000XX\n0006DAB7 000000XX\n0006DCD7 000000XX',
        'PAL': '000520AF 000000XX\n0005227B 000000XX\n0005249B 000000XX'
    },
    'Perfect Level Up': {
        'DESC': 'Info:\nMakes all units get all stat every level up. If used with Uncapped BEXP Level up, you can get all 8 in base as well.\n\nCode:',
        'NTSC': '088C361A 64646464\n216500FC 00000000\n088C361E 64646464\n216500FC 00000000',
        'PAL': '088B5B9A 64646464\n216500FC 00000000\n088B5B9E 64646464\n216500FC 00000000'
    },
    'Stat Gain Modifier': {
        'DESC': 'Info:\nReplace XX with the gain you want. 02 means each stat that you get in a level up will get +2.\n\nCode:',
        'NTSC': '0006D303 000000XX\n0006D35F 000000XX',
        'PAL': 'Code unknown for PAL. Please request it.'
    },
    'Special Items': {
        'DESC': 'Info:\nFlorete - Uses Magic & Infinite\nEttard - Infinite\nCaladbolg - Infinite\nTarvos - Infinite\nLughnasadh - Infinite\nCymbeline - Infinite\nThani - Infinite\nCreiddylad - Infinite\n\nCode:',
        'NTSC': '00B603C3 00000006\n00B603E9 00000001\n00B60439 00000001\n00B60259 00000001\n00B60ED9 00000001\n00B61339 00000001\n00B61C49 00000001\n00B622D9 00000001\n00B62329 00000001',
        'PAL': 'Code unknown for PAL. Please request it.'
    },
    'Item Mods': {
        'DESC': 'Info:\nAll unlocked, infinite, usable by anyone and no weapon ranks.\nFlorete does magic damage.\n\nCode:',
        'NTSC': '08B5FE28 00000000\n10CB0050 00000000\n08B5FE48 00010000\n21270050 00000000\n08B5FE4C 00000000\n11270050 00000000\n00B603C3 00000006',
        'PAL': 'Code unknown for PAL. Please request it.'
    },
    'All Convoy': {
        'DESC': 'Info:\nAll items in convoy. All items 50 uses.\n\nCode:',
        'NTSC': '083E92A0 80B5FE10\n21270028 00000050\n083E92A4 00000032\n01270028 00000000\n083E92A5 00000000\n01270028 00000000',
        'PAL': 'Code unknown for PAL. Please request it.'
    },
    'Blessed Convoy': {
        'DESC': 'Info:\nAll items in convoy. All items are blessed. Use with Clear Convoy to remove all items.\n\nCode:',
        'NTSC': '083E92A0 80B5FE10\n21270028 00000050\n083E92A4 00000050\n01270028 00000000\n083E92A5 00000010\n01270028 00000000',
        'PAL': 'Code unknown for PAL. Please request it.'
    },
    'Clear Convoy': {
        'DESC': 'Info:\nClears all items in convoy. Use with Blessed Convoy to remove all items.\n\nCode:',
        'NTSC': '083E92A0 00000000\n2BC10004 00000000',
        'PAL': 'Code unknown for PAL. Please request it.'
    },
    'Convoy 300': {
        'DESC': 'Info:\nEnables max convoy capacity for all teams and chapters to allow use for all items codes.\n\nCode:',
        'NTSC': '024CB75A 0000012C\n024CB762 0000012C\n024CB766 000092A0\n024CB76A 0000012C\n024CB76E 000092A0\n024CB772 0000012C\n024CB776 000092A0',
        'PAL': 'Code unknown for PAL. Please request it.'
    },
    'All Skills': {
        'DESC': 'Info:\nCan assign all skills in the game.\n\nCode:',
        'NTSC': '2050002C 00000000\n0870F8B0 00000002\n0023002C 00000000\n0870F8B4 80710B04',
        'PAL': 'Code unknown for PAL. Please request it.'
    },
    'Free Skills': {
        'DESC': 'Info:\nAll skills cost 0.\n\nCode:',
        'NTSC': '0870F8AE 00000000\n0050002C 00000000',
        'PAL': 'Code unknown for PAL. Please request it.'
    },
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

    char_all_code = 'A203F0 00000000'

    # Create code output and start with Keybind
    char_output = []
    char_output.append(kb)

    # Character Select Validation
    char = data['character']
    if not char:
        return "No character selected!"

    if VERSION == 'PAL' and char == 'Oliver':
        return "Oliver ID unknown in the PAL version of the game. Please report on my discord."

    # Define Step Counts
    item_step = get_offset(char, 'Item_Step', 'Char')
    skill_step = get_offset(char, 'Skill_Step', 'Char')

    #region Class

    char_class = data['class']
    if char_class:

        # Get offsets
        char_class_off = get_offset(char, 'Class', 'Char')
        class_id = get_offset(char_class, 'Class', 'Class')
    
        if char == 'All':
            char_class_code = f'08{char_class_off[-6:]} {class_id}\n20{char_all_code}'
        else:
            char_class_code = f'04{char_class_off[-6:]} {class_id}'
        char_output.append(char_class_code)
    
    #endregion

    #region Items
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
            item_id = get_offset(item, 'Item', 'Item')

            # Create item code and add to output
            if char == 'All':
                char_item_code = f'08{item_off[-6:]} {item_id}\n20{char_all_code}'
            else:
                char_item_code = f'04{item_off[-6:]} {item_id}'
            char_output.append(char_item_code)

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

                if char == 'All':
                    char_item_uses_code = f'08{item_uses_off[-6:]} 000000{uses}\n00{char_all_code}'
                else:
                    char_item_uses_code = f'00{item_uses_off[-6:]} 000000{hex(uses).replace('0x', '').zfill(2).upper()}'
                char_output.append(char_item_uses_code)

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
            status = hex(sts).replace('0x', '').zfill(2).upper()
            if char == 'All':
                char_status_code = f'08{item_status_off[-6:]} 000000{status}\n00{char_all_code}'
            else:
                char_status_code = f'00{item_status_off[-6:]} 000000{status}'
            char_output.append(char_status_code)

            # If forged = True
            if forged:
                # Create variable for forge name
                fname_hex = ''

                # Error handling for forge name
                if len(fname) > 26:
                        return f'Error: Forge Name for {item} is too long! Please enter a name with 26 characters or less.'
                elif fname and 0 < len(fname) <= 26:
                    # If forge name is populated, convert to hex
                    for c in fname:
                        fname_hex += format(ord(c), "x").zfill(2)
                else:
                    # If forge name does not meet requirements, default forge name to item name
                    for c in item:
                        fname_hex += format(ord(c), "x").zfill(2)
                
                # Pad forge name to 60 digits (26 characters in hex)
                fname_hex = fname_hex.ljust(52, '0').upper()

                # Create forge name code and add to output
                j = 0

                # Loop through forge name and add to output
                for k in range(0, 7):
                    # First set is 16 bytes, so it needs to be handled differently
                    if k == 0:
                        fname_offset = hex(int(item_off, 16) + 6).replace('0x', '').zfill(8).upper()
                        if char == 'All':
                            char_fname_code = f'08{fname_offset[-6:]} 0000{fname_hex[:4]}\n10{char_all_code}'
                        else:
                            char_fname_code = f'02{fname_offset[-6:]} 0000{fname_hex[:4]}'
                        char_output.append(char_fname_code)

                    # The rest of the sets are 32 bytes
                    else:
                        fname_offset = hex(int(item_off, 16) + 8 + j).replace('0x', '').zfill(8).upper()
                        if char == 'All':
                            char_fname_code = f'08{fname_offset[-6:]} {fname_hex[4+(j*2):12+(j*2)]}\n20{char_all_code}'
                            if fname_hex[4+(j*2):12+(j*2)] != '00000000':
                                char_output.append(char_fname_code)
                        else:
                            char_fname_code = f'04{fname_offset[-6:]} {fname_hex[4+(j*2):12+(j*2)]}'
                            if char_fname_code[-8:] != '00000000':
                                char_output.append(char_fname_code)

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
                        if char == 'All':
                            mt_hit_code = f'08{item_forge_off[-6:]} 0000{hex(mt).replace("0x", "").zfill(2).upper()}{hex(hit).replace("0x", "").zfill(2).upper()}\n10{char_all_code}'
                            crit_wt_off = hex(int(item_forge_off, 16) + 2).replace("0x", "").zfill(8).upper()
                            crit_wt_code = f'08{crit_wt_off[-6:]} 0000{hex(crit).replace("0x", "").zfill(2).upper()}{wt}\n10{char_all_code}'

                        else:
                            mt_hit_code = f'02{item_forge_off[-6:]} 0000{hex(mt).replace('0x', '').zfill(2).upper()}{hex(hit).replace('0x', '').zfill(2).upper()}'
                            crit_wt_off = hex(int(item_forge_off, 16) + 2).replace('0x', '').zfill(8).upper()
                            crit_wt_code = f'02{crit_wt_off[-6:]} 0000{hex(crit).replace('0x', '').zfill(2).upper()}{wt}'

                        char_output.append(mt_hit_code)
                        char_output.append(crit_wt_code)
                    
                    # Error handling for mt, hit, wt, and crit
                    except ValueError:
                        return f'Error: Stat for {item} is not a number! Please enter a value between 0 and 255.'
    
    #endregion

    #region Stats

    for chstat, char_stat in enumerate(CHAR_STATS):

            # Get data input
            char_stat_input = data['stats'][chstat]
            char_stat_offset = get_offset(char, char_stat, 'Char')

            if char_stat_input:
                try:
                    char_stat_num = int(char_stat_input)
                    if char_stat == 'Level' and char_stat_num > 20:
                        return f'Error: Stat for {char_stat.replace("_", " ")} is too high! Please enter a value between 0 and 20.'
                    elif char_stat == 'EXP' and char_stat_num > 99:
                        return f'Error: Stat for {char_stat.replace("_", " ")} is too high! Please enter a value between 0 and 99.'
                    if char_stat_num > 255:
                        return f'Error: Stat for {char_stat.replace("_", " ")} is too high! Please enter a value between 0 and 255.'
                    
                    if char == 'All':
                        char_stat_code = f'08{char_stat_offset[-6:]} 000000{hex(char_stat_num).replace("0x", "").zfill(2).upper()}\n00{char_all_code}'

                    else:
                        char_stat_code = f'00{char_stat_offset[-6:]} 000000{hex(char_stat_num).replace("0x", "").zfill(2).upper()}'

                    char_output.append(char_stat_code)
                
                except ValueError:
                    return f'Error: Stat for {char_stat} is not a number! Please enter a value between 0 and 255.'

    #endregion

    #region Weapon Ranks

    for chwr, char_rank in enumerate(CHAR_RANKS):

        # Get data input
        char_rank_input = data['ranks'][chwr]
        char_rank_offset = get_offset(char, char_rank, 'Char')

        # If data is populated
        if char_rank_input:
            if char_rank_input == 'SS':
                rank = '014B'
            elif char_rank_input == 'S':
                rank = '00FB'
            elif char_rank_input == 'A':
                rank = '00B5'
            elif char_rank_input == 'B':
                rank = '0079'
            elif char_rank_input == 'C':
                rank = '0047'
            elif char_rank_input == 'D':
                rank = '001F'
            elif char_rank_input == 'E':
                rank = '0001'
            else:
                return f'Error: Invalid weapon rank for {char_rank.replace('_', ' ')}! Please select a valid rank.'

            if char == 'All':
                char_rank_code = f'08{char_rank_offset[-6:]} 0000{rank}\n10{char_all_code}'

            else:
                char_rank_code = f'02{char_rank_offset[-6:]} 0000{rank}'

            char_output.append(char_rank_code)

    #endregion

    # Add end code to output
    char_output.append('E0000000 80008000')

    # If only kb and end code, return no changes made
    if len(char_output) == 2:
        return "No changes made!"
    else:
        return "\n".join(char_output)

def get_class_code(data):

    class_all_code = 'AA011C 00000000'

    # Create code output and append start code
    class_output = []

    if VERSION == 'NTSC':
        class_output.append('20B54158 8070F8BC')
    elif VERSION == 'PAL':
        class_output.append('20B58CF8 80701E3C')

    # Class Select Validation
    cls = data['class']
    if not cls:
        return "No class selected!"

    #region Promote

    promote = data['promote']
    if promote:
        class_promote_off = get_offset(cls, 'Next_Class', 'Class')
        class_id = get_offset(promote, 'Class', 'Class')

        if cls == 'All':
            class_promote_code = f'08{class_promote_off[-6:]} {class_id}\n20{class_all_code}'
        else:
            class_promote_code = f'04{class_promote_off[-6:]} {class_id}'
        class_output.append(class_promote_code)

    #endregion

    #region Weapon Ranks

    min_ranks = ['Min_' + i for i in CHAR_RANKS]
    max_ranks = ['Max_' + i for i in CHAR_RANKS]
    class_ranks = min_ranks + max_ranks

    for clwr, class_rank in enumerate(class_ranks):

        # Get data input
        class_rank_input = data['ranks'][clwr]
        class_rank_offset = get_offset(cls, class_rank, 'Class')

        # If data is populated
        if class_rank_input:
            if class_rank_input == 'SS':
                rank = '014B'
            elif class_rank_input == 'S':
                rank = '00FB'
            elif class_rank_input == 'A':
                rank = '00B5'
            elif class_rank_input == 'B':
                rank = '0079'
            elif class_rank_input == 'C':
                rank = '0047'
            elif class_rank_input == 'D':
                rank = '001F'
            elif class_rank_input == 'E':
                rank = '0001'
            else:
                return f'Error: Invalid weapon rank for {class_rank.replace('_', ' ')}! Please select a valid rank.'

            if cls == 'All':
                class_rank_code = f'08{class_rank_offset[-6:]} 0000{rank}\n10{class_all_code}'
            else:
                class_rank_code = f'02{class_rank_offset[-6:]} 0000{rank}'
            class_output.append(class_rank_code)
    
    #endregion

    #region Stats

    for clstat, class_stat in enumerate(CLASS_STATS):

        class_stat_input = data['stats'][clstat]
        class_stat_offset = get_offset(cls, class_stat, 'Class')

        if class_stat_input:

            try:

                class_stat_num = int(class_stat_input)
                if class_stat_num > 255:
                    return f'Error: Stat for {class_stat.replace('_', ' ')} is too high! Please enter a value between 0 and 255.'
                
                if cls == 'All':
                    class_stat_code = f'08{class_stat_offset[-6:]} 000000{hex(class_stat_num).replace("0x", "").zfill(2).upper()}\n00{class_all_code}'
                else:
                    class_stat_code = f'00{class_stat_offset[-6:]} 000000{hex(class_stat_num).replace("0x", "").zfill(2).upper()}'
                class_output.append(class_stat_code)
            
            # Error handling for stats
            except ValueError:
                return f'Error: Stat for {class_stat} is not a number! Please enter a value between 0 and 255.'

    #endregion

    # Add end code to output
    class_output.append('E0000000 80008000')

    # If only start and end code, return no changes made
    if len(class_output) == 2:
        return "No changes made!"
    else:
        return "\n".join(class_output)

def get_item_code(data):

    item_all_code = 'CA0050 00000000'

    # Create code output and append start code
    item_output = []
    
    if VERSION == 'NTSC':
        item_output.append('20B54158 8070F8BC')
    elif VERSION == 'PAL':
        item_output.append('20B58CF8 80701E3C')

    # Item Select Validation
    item = data['item']
    if not item:
        return "No item selected!"

    #region Item Data

    for item_data in ITEM_DATA:

        # Get data input
        item_data_input = data['data'][item_data]
        item_data_offset = get_offset(item, item_data, 'Item')

        # If data is populated
        if item_data_input:
            # Determine attack type
            if item_data == 'Attack_Type':
                if item_data_input == 'STR':
                    str_mag = '00'
                elif item_data_input == 'MAG':
                    str_mag = '06'
                else:
                    return f'Error: Invalid attack type for {item}! Please select a valid type.'
                
                if item == 'All':
                    item_data_code = f'08{item_data_offset[-6:]} 000000{str_mag}\n00{item_all_code}'
                else:
                    item_data_code = f'00{item_data_offset[-6:]} 000000{str_mag}'
                item_output.append(item_data_code)

            # Determine weapon rank
            elif item_data == 'Weapon_Rank':
                if item_data_input == 'SS':
                    rank = '014B'
                elif item_data_input == 'S':
                    rank = '00FB'
                elif item_data_input == 'A':
                    rank = '00B5'
                elif item_data_input == 'B':
                    rank = '0079'
                elif item_data_input == 'C':
                    rank = '0047'
                elif item_data_input == 'D':
                    rank = '001F'
                elif item_data_input == 'E':
                    rank = '0001'
                else:
                    return f'Error: Invalid weapon rank for {item}! Please select a valid rank.'
                
                if item == 'All':
                    item_data_code = f'08{item_data_offset[-6:]} 0000{rank}\n10{item_all_code}'
                else:
                    item_data_code = f'02{item_data_offset[-6:]} 0000{rank}'
                item_output.append(item_data_code)

            # Determine EXP gain
            elif item_data == 'EXP Gain':
                if item == 'All':
                    item_data_code = f'08{item_data_offset[-6:]} 000000{hex(int(item_data_input)).replace("0x", "").zfill(2).upper()}\n00{item_all_code}'
                else:
                    item_data_code = f'00{item_data_offset[-6:]} 000000{hex(int(item_data_input)).replace("0x", "").zfill(2).upper()}'
                item_output.append(item_data_code)

            # Determine Unlock
            elif item_data == 'Unlock':
                if item_data_input:
                    unlock = '00'
                    if item == 'All':
                        item_data_code = f'08{item_data_offset[-6:]} 000000{unlock}\n00{item_all_code}'
                    else:
                        item_data_code = f'00{item_data_offset[-6:]} 000000{unlock}'
                    item_output.append(item_data_code)

            # Determine Infinite and Brave
            elif item_data in ['Infinite', 'Brave']:
                if item_data_input:
                    inf_brave = '01'
                    if item == 'All':
                        item_data_code = f'08{item_data_offset[-6:]} 000000{inf_brave}\n00{item_all_code}'
                    else:
                        item_data_code = f'00{item_data_offset[-6:]} 000000{inf_brave}'
                    item_output.append(item_data_code)

            # Determine Char Unlock
            elif item_data == 'Char_Unlock':
                if item_data_input:
                    c_unlock = '0000'
                    if item == 'All':
                        item_data_code = f'08{item_data_offset[-6:]} 0000{c_unlock}\n10{item_all_code}'
                    else:
                        item_data_code = f'02{item_data_offset[-6:]} 0000{c_unlock}'
                    item_output.append(item_data_code)

            # Determine Heal
            elif item_data == 'Heal':
                if item_data_input:
                    heal = '10'
                    if item == 'All':
                        item_data_code = f'08{item_data_offset[-6:]} 000000{heal}\n00{item_all_code}'
                    else:
                        item_data_code = f'00{item_data_offset[-6:]} 000000{heal}'
                    item_output.append(item_data_code)
    
    #endregion

    #region Item Stats

    for istat, item_stat in enumerate(ITEM_STATS):

        # Get data input and offset for item stat
        item_stat_input = data['stats'][istat]
        item_stat_offset = get_offset(item, item_stat, 'Item')

        # If data is populated
        if item_stat_input:
            try:
                # Validation
                item_stat_num = int(item_stat_input)
                if item_stat_num > 255:
                    return f'Error: Stat for {item_stat.replace("_", " ")} is too high! Please enter a value between 0 and 255.'
                
                if item == 'All':
                    item_stat_code = f'08{item_stat_offset[-6:]} 000000{hex(item_stat_num).replace("0x", "").zfill(2).upper()}\n00{item_all_code}'
                else:
                    item_stat_code = f'00{item_stat_offset[-6:]} 000000{hex(item_stat_num).replace("0x", "").zfill(2).upper()}'
                item_output.append(item_stat_code)

            # Error handling for item stats
            except ValueError:
                return f'Error: Stat for {item_stat} is not a number! Please enter a value between 0 and 255.'

    #endregion

    #region Item Equip Bonuses

    for ibonus, bonus in enumerate(ITEM_BONUS):

        # Get data input and offset for equip bonus
        item_bonus_input = data['bonuses'][ibonus]
        item_bonus_offset = get_offset(item, bonus, 'Item')

        # If data is populated
        if item_bonus_input:
            try:
                # Validation
                bonus_num = int(item_bonus_input)
                if bonus_num > 255:
                    return f'Error: Equip Bonus for {bonus.replace("_", " ")} is too high! Please enter a value between 0 and 255.'
                
                if item == 'All':
                    item_bonus_code = f'08{item_bonus_offset[-6:]} 000000{hex(bonus_num).replace("0x", "").zfill(2).upper()}\n00{item_all_code}'
                else:
                    item_bonus_code = f'00{item_bonus_offset[-6:]} 000000{hex(int(item_bonus_input)).replace("0x", "").zfill(2).upper()}'
                item_output.append(item_bonus_code)

            # Error handling for equip bonuses
            except ValueError:
                return f'Error: Equip Bonus for {bonus} is not a number! Please enter a value between 0 and 255.'
    
    #endregion

    # Add end code to output
    item_output.append('E0000000 80008000')

    # If only start and end code, return no changes made
    if len(item_output) == 2:
        return "No changes made!"
    else:
        return "\n".join(item_output)

def get_keybind_code(data):
    val = 0
    if data['controller'] == '':
        if VERSION == 'NTSC':
            return '20B54158 8070F8BC'
        elif VERSION == 'PAL':
            return '20B58CF8 80701E3C'
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
        
        if VERSION == 'NTSC':
            return f'283D79BA {hex(val).replace('0x', '').zfill(8)}'
        elif VERSION == 'PAL':
            return f'283D035A {hex(val).replace('0x', '').zfill(8)}'
    
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
        if VERSION == 'NTSC':
            return f'283D7928 {hex(val).replace('0x', '').zfill(8)}'
        elif VERSION == 'PAL':
            return f'283D02C8 {hex(val).replace('0x', '').zfill(8)}'

# %%
# GUI

class CodeGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FE:RD Code Creator")

        # Set no resize
        self.root.resizable(False, False)

        if hasattr(sys, "_MEIPASS"):
            icon_path = os.path.join(sys._MEIPASS, "FE-RD.ico")
        else:
            icon_path = "FE-RD.ico"

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
        style.map("TCombobox",fieldbackground=[("readonly", "#ffffff")],foreground=[("readonly", "#000000")],)
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
        if match:
            code_part = match.group(1).strip()
        else:
            code_part = code

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

    def options_tab(self):
        options_tab = ttk.Frame(self.notebook)
        self.notebook.add(options_tab, text="Options")

        #region Separators
        ttk.Separator(options_tab, orient="horizontal").grid(row=1, column=0, columnspan=99, sticky="ew")
        ttk.Separator(options_tab, orient="vertical").grid(row=0, column=2, rowspan=4, sticky="ns")
        ttk.Separator(options_tab, orient="vertical").grid(row=0, column=4, rowspan=4, sticky="ns")
        ttk.Separator(options_tab, orient="horizontal").grid(row=3, column=0, columnspan=99, sticky="ew")
        #endregion

        #region Controller

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
            "Classic Controller": [
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
                "-",
            ],
            "GameCube Controller": [
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
                "Start",
            ],
        }

        controller_frame = ttk.Frame(options_tab)
        controller_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(controller_frame, text="Controller:", font=SECTION_HEADER).grid(row=0, column=0, padx=5)
        self.controller = ttk.Combobox(controller_frame, values=list(self.keybinds.keys()))
        self.controller.grid(row=0, column=1)
        self.controller.bind("<<ComboboxSelected>>", self.update_checkboxes)

        # Checkboxes Section
        self.checkboxes = []
        self.checkbox_frame = ttk.Frame(options_tab)
        self.checkbox_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        #endregion

        #region Version

        version_frame = ttk.Frame(options_tab)
        version_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        ttk.Label(version_frame, text="Version:", font=SECTION_HEADER).grid(row=0, column=0, padx=5)
        self.version = ttk.Combobox(version_frame, values=["NTSC 1.00", "NTSC 1.01", "PAL"])
        self.version.grid(row=0, column=1)

        #endregion

        #region Options Info

        options_info = ttk.Frame(options_tab)
        options_info.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

        desc = 'Welcome to the Fire Emblem: Radiant Dawn Code Creator!\n\nThis tool allows you to generate codes for characters, classes and items. Fill in the desired information and click the "Generate Code" button to create the code.\n\nOptions Tab:\n- Controller Activation codes will only apply to the Character Tab. Codes generated from the Class and Item tabs are codes that will need to be always on for the game to function properly.\n- Version will determine which region the creator will make the code for. Leaving this section blank will have the creator default to NTSC-U 1.01.\n\nOther Notes:\n- Forged Name has a character cap of 26.\n- Number Input fields have a cap of 255 unless specified otherwise in the respective tab.'

        ttk.Label(options_info, text=desc, wraplength=1000, justify="left").grid(row=0, column=0)

        #endregion

    def update_checkboxes(self, event):
        for checkbox in self.checkbox_frame.winfo_children():
            checkbox.destroy()
        self.checkboxes = []

        selected_option = self.controller.get()
        if selected_option == "":
            pass
        elif selected_option in self.keybinds:
            length = len(self.keybinds[selected_option])
            ttk.Label(self.checkbox_frame, text="Buttons", font=SECTION_HEADER).grid(row=0, column=0, rowspan=length, padx=5)
            ttk.Separator(self.checkbox_frame, orient="vertical").grid(row=0, column=1, rowspan=length, sticky="ns")
            for i, option in enumerate(self.keybinds[selected_option]):
                ttk.Label(self.checkbox_frame, text=option).grid(row=i, column=3, padx=5, sticky="e")
                var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(self.checkbox_frame, variable=var)
                checkbox.grid(row=i, column=4)
                self.checkboxes.append(var)

    def character_tab(self):

        char_tab = ttk.Frame(self.notebook)
        self.notebook.add(char_tab, text="Character")

        #region Separators
        ttk.Separator(char_tab, orient="vertical").grid(row=0, column=3, sticky="ns")
        ttk.Separator(char_tab, orient="horizontal").grid(row=1, column=0, columnspan=99, sticky="ew")
        ttk.Separator(char_tab, orient="vertical").grid(row=2, column=1, sticky="ns")
        ttk.Separator(char_tab, orient="vertical").grid(row=2, column=3, sticky="ns")
        ttk.Separator(char_tab, orient="horizontal").grid(row=3, column=0, columnspan=99, sticky="ew")
        #endregion

        #region Character and Class

        # Character Select Frame
        char_frame = ttk.Frame(char_tab)
        char_frame.grid(row=0, column=0, sticky="nsew", columnspan=3, padx=10, pady=10)

        ttk.Label(char_frame, text="Character:", font=SECTION_HEADER).grid(row=0, column=0)
        self.char_select = ttk.Combobox(char_frame, values=CHAR_LIST)
        self.char_select.grid(row=0, column=1, padx=10)

        # Class Select Frame
        char_class_frame = ttk.Frame(char_tab)
        char_class_frame.grid(row=0, column=4, sticky="nsew", columnspan=4, padx=10, pady=10)

        ttk.Label(char_class_frame, text="Class:", font=SECTION_HEADER).grid(row=0, column=0)
        self.char_class = ttk.Combobox(char_class_frame, values=CLASS_LIST, width=40)
        self.char_class.grid(row=0, column=1, padx=10)

        # endregion

        #region Items Section
        self.char_items = []
        char_items_frame = ttk.Frame(char_tab)
        char_items_frame.grid(row=2, column=5, padx=10, pady=10, sticky='nsew')

        # Item table
        char_item_table = ttk.Frame(char_items_frame)
        char_item_table.grid(row=0, column=0, sticky='n')

        headers = [
            "Items",
            "Uses",
            "Forged Name",
            "Mt",
            "Hit",
            "Crit",
            "Weightless",
            "Forged",
            "Blessed"
        ]
        for i, header in enumerate(headers):
            if header in ['Blessed', 'Forged', 'Weightless']:
                ttk.Label(char_item_table, text=header, font=SECTION_HEADER).grid(row=0, column=i, padx=5, pady=5)
            else:
                ttk.Label(char_item_table, text=header, font=SECTION_HEADER).grid(row=0, column=i, pady=5)

        for row in range(1, 8):
            char_item_row = []
            char_item_combobox = ttk.Combobox(char_item_table, values=ITEM_LIST, width=25)
            char_item_combobox.grid(row=row, column=0, padx=1, pady=1)
            char_item_row.append(char_item_combobox)

            for col in range(1, 9):
                if col == 6 or col == 7 or col == 8:
                    char_item_var = tk.BooleanVar(value=False)
                    if col == 8:
                        blessed_checkbox = ttk.Checkbutton(char_item_table, text="", variable=char_item_var)
                        blessed_checkbox.grid(row=row, column=col)
                    elif col == 7:
                        forged_checkbox = ttk.Checkbutton(char_item_table, text="", variable=char_item_var)
                        forged_checkbox.grid(row=row, column=col)
                    elif col == 6:
                        wt_checkbox = ttk.Checkbutton(char_item_table, text="", variable=char_item_var)
                        wt_checkbox.grid(row=row, column=col)
                    char_item_row.append(char_item_var)
                else:
                    if col == 2:
                        char_item_entry = ttk.Entry(char_item_table, width=20)
                        char_item_entry.grid(row=row, column=col, padx=1, pady=1)
                        char_item_row.append(char_item_entry)
                    else:
                        char_item_entry = ttk.Entry(char_item_table, width=5)
                        char_item_entry.grid(row=row, column=col, padx=1, pady=1)
                        char_item_row.append(char_item_entry)

            self.char_items.append(char_item_row)

        # Item Description
        char_desc_frame = ttk.Frame(char_items_frame)
        char_desc_frame.grid(row=1, column=0, sticky='nsew')

        desc = 'Stats:\n- Level, EXP and Current HP get set to input number: Level Max = 20 - EXP max = 99\n- Other stat fields are increases of the base class stats. Putting in 25 will add 25 to the base stat, not set the stat to 25.\n\nItem Table:\n- For Forged Name, Mt, Hit, Crit and Weightless to take effect, Forged must be checked.\n\nMake sure to pair with a keybind in the options tab!'
        ttk.Label(char_desc_frame, text=desc, wraplength=1000, justify='left').grid(row=0, column=0, padx=5, pady=5)

        # endregion

        #region Character Stats

        char_stat_frame = ttk.Frame(char_tab)
        char_stat_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        ttk.Label(char_stat_frame, text="Stats", font=SECTION_HEADER).grid(row=0, column=0, columnspan=2, pady=5)
        self.char_stats = []

        for i, stat in enumerate(CHAR_STATS):
            ttk.Label(char_stat_frame, text=stat).grid(row=i+1, column=0, padx=5, sticky="e")
            char_stat_entry = ttk.Entry(char_stat_frame, width=5)
            char_stat_entry.grid(row=i+1, column=1, pady=1)
            self.char_stats.append(char_stat_entry)

        #endregion

        #region Character Weapon Ranks

        char_rank_frame = ttk.Frame(char_tab)
        char_rank_frame.grid(row=2, column=2, padx=10, pady=10, sticky='nsew')

        ttk.Label(char_rank_frame, text="Weapon Ranks", font=SECTION_HEADER).grid(row=0, column=3, columnspan=2, pady=5)
        self.char_ranks = []

        for i, rank in enumerate(CHAR_RANKS):
            ttk.Label(char_rank_frame, text=rank.replace('_', ' ')).grid(row=i + 1, column=3, padx=5, sticky="e")
            char_ranks_combobox = ttk.Combobox(char_rank_frame, values=["SS", "S", "A", "B", "C", "D", "E"], width=5)
            char_ranks_combobox.grid(row=i + 1, column=4, pady=1)
            self.char_ranks.append(char_ranks_combobox)
        
        # endregion

        # Generate Button
        char_button = ttk.Button(char_tab, text="Generate", command=self.generate_character)
        char_button.grid(row=4, column=0, columnspan=99, sticky="nsew")

    def generate_character(self):
        character_data = {
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

        keybinds_data = {
            "controller": self.controller.get(),
            "keys": [key.get() for key in self.checkboxes],
        }

        version = self.version.get()
        set_version(version)

        key_code = get_keybind_code(keybinds_data)
        output = get_char_code(character_data, key_code)
        self.output_code(output)

    def class_tab(self):
        class_tab = ttk.Frame(self.notebook)
        self.notebook.add(class_tab, text="Class")

        #region Separators
        ttk.Separator(class_tab, orient="vertical").grid(row=0, column=5, sticky="ns")
        ttk.Separator(class_tab, orient="horizontal").grid(row=1, column=0, columnspan=99, sticky="ew")
        ttk.Separator(class_tab, orient="horizontal").grid(row=3, column=0, columnspan=99, sticky="ew")
        ttk.Separator(class_tab, orient="vertical").grid(row=2, column=1, rowspan=99, sticky="ns")
        ttk.Separator(class_tab, orient="vertical").grid(row=2, column=3, rowspan=99, sticky="ns")
        ttk.Separator(class_tab, orient="vertical").grid(row=2, column=5, rowspan=99, sticky="ns")
        #endregion

        #region Class and Promote section

        # Class Select Section
        class_frame = ttk.Frame(class_tab)
        class_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=5, sticky="nsew")

        ttk.Label(class_frame, text="Class:", font=SECTION_HEADER).grid(row=0, column=0)
        self.class_select = ttk.Combobox(class_frame, values=['All'] + CLASS_LIST, width=40)
        self.class_select.grid(row=0, column=1, padx=10)

        # Promotion Section
        class_promote_frame = ttk.Frame(class_tab)
        class_promote_frame.grid(row=0, column=6, padx=10, pady=10, columnspan=99, sticky="nsew")

        ttk.Label(class_promote_frame, text="Next Class:", font=SECTION_HEADER).grid(row=0, column=3)
        self.class_promote = ttk.Combobox(class_promote_frame, values=CLASS_LIST, width=40)
        self.class_promote.grid(row=0, column=4, padx=10)

        # endregion

        #region Min Weapon Ranks

        # Create frame for weapon ranks and stats

        class_min_rank_frame = ttk.Frame(class_tab)
        class_min_rank_frame.grid(row=2, column=0, padx=10, pady=10, sticky='n')

        # Min Weapon Ranks Section
        ttk.Label(class_min_rank_frame, text="Min Weapon Ranks", font=SECTION_HEADER).grid(row=0, column=0, pady=5, columnspan=2)

        min_weapon_ranks = ['Min_' + i for i in CHAR_RANKS]
        self.class_min_ranks = []

        for i, rank in enumerate(min_weapon_ranks):
            ttk.Label(class_min_rank_frame, text=rank.replace('_', ' ')).grid(row=i + 1, column=0, padx=5, sticky="e")
            class_min_rank_combobox = ttk.Combobox(class_min_rank_frame, values=["SS", "S", "A", "B", "C", "D", "E"], width=5)
            class_min_rank_combobox.grid(row=i + 1, column=1, pady=1)
            self.class_min_ranks.append(class_min_rank_combobox)

        #endregion

        #region Max Weapon Ranks

        class_max_rank_frame = ttk.Frame(class_tab)
        class_max_rank_frame.grid(row=2, column=2, padx=10, pady=10, sticky='n')

        ttk.Label(class_max_rank_frame, text="Max Weapon Ranks", font=SECTION_HEADER).grid(row=0, column=0, pady=5, columnspan=2)

        max_weapon_ranks = ['Max_' + i for i in CHAR_RANKS]
        self.class_max_ranks = []

        for i, rank in enumerate(max_weapon_ranks):
            ttk.Label(class_max_rank_frame, text=rank.replace('_', ' ')).grid(row=i + 1, column=0, padx=5, sticky="e")
            class_max_rank_combobox = ttk.Combobox(class_max_rank_frame, values=["SS", "S", "A", "B", "C", "D", "E"], width=5)
            class_max_rank_combobox.grid(row=i + 1, column=1, pady=1)
            self.class_max_ranks.append(class_max_rank_combobox)

        #endregion

        #region Stats

        class_stats_frame = ttk.Frame(class_tab)
        class_stats_frame.grid(row=2, column=4, padx=10, pady=10, sticky='n')

        ttk.Label(class_stats_frame, text="Stats", font=SECTION_HEADER).grid(row=0, column=0, pady=5, columnspan=2)

        self.class_stats = []

        for i, stat in enumerate(CLASS_STATS):
            ttk.Label(class_stats_frame, text=stat.replace('_', ' ')).grid(row=i + 1, column=0, padx=5, sticky="e")
            class_stats_entry = ttk.Entry(class_stats_frame, width=5)
            class_stats_entry.grid(row=i + 1, column=1, pady=1)
            self.class_stats.append(class_stats_entry)

        # endregion

        #region Class Description

        class_desc_frame = ttk.Frame(class_tab)
        class_desc_frame.grid(row=2, column=6, padx=10, pady=10, sticky='n')

        desc = 'Notes:\n- Min Ranks only get applied on class promotion. Changing these to SS will not change the characters current rank.\n- Next Class will be the class that the selected class will promote to.'

        ttk.Label(class_desc_frame, text=desc, wraplength=650, justify='left').grid(row=0, column=0)

        #endregion

        # Generate Button
        class_button = ttk.Button(class_tab, text="Generate", command=self.generate_class)
        class_button.grid(row=4, column=0, columnspan=99, sticky="nsew")

    def generate_class(self):
        class_data = {
            "class": self.class_select.get(),
            "promote": self.class_promote.get(),
            "ranks": [min.get() for min in self.class_min_ranks]
            + [max.get() for max in self.class_max_ranks],
            "stats": [stat.get() for stat in self.class_stats]
        }

        version = self.version.get()
        set_version(version)

        output = get_class_code(class_data)

        self.output_code(output)

    def items_tab(self):

        items_tab = ttk.Frame(self.notebook)
        self.notebook.add(items_tab, text="Items")

        #region Separators
        ttk.Separator(items_tab, orient="horizontal").grid(row=1, column=0, columnspan=99, sticky="ew")
        ttk.Separator(items_tab, orient="horizontal").grid(row=3, column=0, columnspan=99, sticky="ew")
        ttk.Separator(items_tab, orient="vertical").grid(row=2, column=1, rowspan=99, sticky="ns")
        ttk.Separator(items_tab, orient="vertical").grid(row=2, column=3, rowspan=99, sticky="ns")
        #endregion

        #region Item

        item_frame = ttk.Frame(items_tab)
        item_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=99, sticky="nsew")

        ttk.Label(item_frame, text="Item:", font=SECTION_HEADER).grid(row=0, column=0)
        self.item_select = ttk.Combobox(item_frame, values=['All'] + ITEM_LIST, width=25)
        self.item_select.grid(row=0, column=1, padx=10)

        # endregion

        #region Item Data

        item_data_frame = ttk.Frame(items_tab)
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

        #endregion

        #region Item Stats

        item_stats_frame = ttk.Frame(items_tab)
        item_stats_frame.grid(row=2, column=2, padx=10, pady=10, sticky="n")

        ttk.Label(item_stats_frame, text="Weapon Stats", font=SECTION_HEADER).grid(row=0, column=0, columnspan=2, pady=5)
        self.item_stats = []

        for i, stat in enumerate(ITEM_STATS):
            ttk.Label(item_stats_frame, text=stat.replace('_', ' ')).grid(row=i+1, column=0, padx=5, sticky="e")
            item_stats_entry = ttk.Entry(item_stats_frame, width=5)
            item_stats_entry.grid(row=i+1, column=1, pady=1)
            self.item_stats.append(item_stats_entry)

        #endregion

        #region Item Equip Bonuses

        item_bonus_frame = ttk.Frame(items_tab)
        item_bonus_frame.grid(row=2, column=4, padx=10, pady=10, sticky="n")

        ttk.Label(item_bonus_frame, text="Equip Bonuses", font=SECTION_HEADER).grid(row=0, column=0, columnspan=2, pady=5)

        self.item_bonuses = []

        for i, label in enumerate(ITEM_BONUS):
            ttk.Label(item_bonus_frame, text=label.replace('_', ' ')).grid(row=i + 1, column=0, padx=5, sticky="e")
            item_bonus_entry = ttk.Entry(item_bonus_frame, width=5)
            item_bonus_entry.grid(row=i + 1, column=1, pady=1)
            self.item_bonuses.append(item_bonus_entry)

        # endregion

        # Generate Button
        item_button = ttk.Button(items_tab, text="Generate", command=self.generate_item)
        item_button.grid(row=4, column=0, columnspan=99, sticky="nsew")

    def generate_item(self):
        item_data = {
            "item": self.item_select.get(),
            "data": {
                key: (var.get() if isinstance(var, tk.BooleanVar) else var.get())
                for key, var in self.item_data.items()
            },
            "stats": [stat.get() for stat in self.item_stats],
            "bonuses": [bonus.get() for bonus in self.item_bonuses]
        }

        version = self.version.get()
        set_version(version)

        output = get_item_code(item_data)  # Get the output from get_char_code

        self.output_code(output)

    def database_tab(self):
        database_tab = ttk.Frame(self.notebook)
        self.notebook.add(database_tab, text="Database")
    
        r=0
        c=0
        for cdb, code_id in enumerate(list(CODE_DATABASE)):
            code_id_button = ttk.Button(database_tab, text=code_id, command=lambda cid=code_id: self.generate_database_code(cid), width=15)
            code_id_button.grid(row=r, column=c, padx=5, pady=5)
            if c == 7:
                c = 0
                r += 1
            else:
                c += 1

    def generate_database_code(self, sel_code):
        version = self.version.get()
        set_version(version)
    
        keybinds_data = {
            "controller": self.controller.get(),
            "keys": [key.get() for key in self.checkboxes],
        }
    
        key_code = get_keybind_code(keybinds_data)

        desc = CODE_DATABASE[sel_code]['DESC']
    
        code = CODE_DATABASE[sel_code][VERSION]
    
        if 'unknown' in code:
            output = code
        else:
            output = '\n'.join([desc, key_code, code, 'E0000000 80008000'])
    
        self.output_code(output)

    def generate_all(self):
        pass

# %%
# Main

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeGeneratorGUI(root)
    root.mainloop()


