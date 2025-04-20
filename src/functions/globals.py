from .. import config

def handleGlobals(ver, diff):

    global VERSION, OFF_MOD, CHARACTER_LIST, DIFFICULTY, DIFF_MOD

    VERSION, OFF_MOD, CHARACTER_LIST = set_version(ver)
    DIFFICULTY, DIFF_MOD = set_difficulty(diff)

def set_version(ver):

    version_map = {
        'NTSC 1.0': ('NTSC', -int('80', 16)),
        'NTSC 1.01': ('NTSC', 0),
        'PAL': ('PAL', 0),
        'Reverse Recruitment 5.3 - ViciousSal': ('RR', 0)
    }
    
    version, off_mod = version_map.get(ver, ('NTSC', 0))
    
    if version == 'NTSC':
        character_list = config.character_ntsc
    elif version == 'PAL':
        character_list = config.character_pal
    elif version == 'RR':
        character_list = config.character_rr
    else:
        return "Error"

    return version, off_mod, character_list

def set_difficulty(diff):

    diff_map = {
        'Easy': 0,
        'Medium/Hard': 1
    }
    
    diff_mod = diff_map.get(diff, 1)

    return diff, diff_mod

def int_check(num) -> bool:
    try:
        val = int(num)
        if val > 255:
            return False
        return True
    except ValueError:
        return False
    
def error_output(data, type, min, max) -> str:
    return f'Error: {data} {type}! Please enter a value between {min} and {max}.'

def getGlobals():

    return VERSION, OFF_MOD, CHARACTER_LIST, DIFFICULTY, DIFF_MOD