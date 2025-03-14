from .config import BASE, CHAR, CLASS, ITEM, CHAR_STATS, CHAR_RANKS, CLASS_STATS, ITEM_STATS, ITEM_DATA, ITEM_EQUIP_BONUS

def set_version(ver):
    version_map = {
        'NTSC 1.0': ('NTSC', -int('80', 16)),
        'NTSC 1.01': ('NTSC', 0),
        'PAL': ('PAL', 0),
        'Reverse Recruitment 5.3 - ViciousSal': ('RR', 0)
    }
    global VERSION, OFFSET_MOD
    VERSION, OFFSET_MOD = version_map.get(ver, ('NTSC', 0))
    return VERSION

def set_difficulty(diff):
    diff_map = {
        'Easy': 0,
        'Medium/Hard': 1
    }
    global DIFFICULTY, DIFF_MOD
    DIFFICULTY = diff
    DIFF_MOD = diff_map.get(diff, 1)
    return DIFFICULTY

def code_gen(data, off, val, all_code, code_type):
    if data == 'All':
        off_prefix = '08'
        if code_type == 2:
            val_prefix = '000000'
            loop_prefix = '0'
        elif code_type == 4:
            val_prefix = '0000'
            loop_prefix = '1'
        elif code_type == 8:
            val_prefix = ''
            loop_prefix = '2'
        else:
            return 'Error: Invalid code type!'

        return f'{off_prefix}{off[-6:]} {val_prefix}{val}\n{loop_prefix}{all_code}'
    
    else:
        if code_type == 2:
            off_prefix = '00'
            val_prefix = '000000'
        if code_type == 4:
            off_prefix = '02'
            val_prefix = '0000'
        if code_type == 8:
            off_prefix = '04'
            val_prefix = ''

        return f'{off_prefix}{off[-6:]} {val_prefix}{val}'

def error_output(data, type, min, max):
    return f'Error: {data} {type}! Please enter a value between {min} and {max}.'

def int_check(num):
    try:
        val = int(num)
        if val > 255:
            return False
        return True
    except ValueError:
        return False

def get_offset(name, data, opt):
    def calculate_offset(base, offset, id, additional_offset=0):
        off = int(base, 16) + OFFSET_MOD + (offset * id) + additional_offset
        return hex(off).replace('0x', '').upper().zfill(8)

    if 'Step' in data:
        if data == 'Item_Step':
            return CHAR['OFFSET']['Item_Step']
        elif data == 'Skill_Step':
            return CHAR['OFFSET']['Skill_Step']

    id = None
    base = None
    offset = None
    additional_offset = 0

    if opt == 'Char':
        if name == 'All':
            id = 0
        else:
            if isinstance(CHAR[VERSION][name], int):
                id = CHAR[VERSION][name]
            else:
                id = CHAR[VERSION][name][DIFF_MOD]
        base = BASE[VERSION]['Character']
        offset = CHAR['OFFSET']['Character']
        if data != 'Character':
            additional_offset = CHAR['OFFSET'][data]
    elif opt == 'Class':
        if name == 'All':
            id = 0
        else:
            id = CLASS['ID'][name]
        base = BASE[VERSION]['Class']
        offset = CLASS['OFFSET']['Class']
        if data != 'Class':
            additional_offset = CLASS['OFFSET'][data]
    elif opt == 'Item':
        if name == 'All':
            id = 0
        else:
            id = ITEM['ID'][name]
        base = BASE[VERSION]['Item']
        offset = ITEM['OFFSET']['Item']
        if data != 'Item':
            additional_offset = ITEM['OFFSET'][data]

    if id is not None and base is not None and offset is not None:
        return calculate_offset(base, offset, id, additional_offset)

    return None

def get_char_code(data):

    char_all_code = '0A203F0 00000000'
    char_output = []

    char = data['character']
    if not char:
        return "Error: No character selected!"
    if CHAR[VERSION].get(char) == 'Unknown':
        return f"Error: {char} ID unknown in the {VERSION} version of the game. Please report on my discord."

    item_step = get_offset(char, 'Item_Step', 'Char')
    skill_step = get_offset(char, 'Skill_Step', 'Char')

    # Character Class

    char_class = data['class']
    if char_class:
        char_class_off = get_offset(char, 'Class', 'Char')
        class_id = get_offset(char_class, 'Class', 'Class')
        char_class_code = code_gen(char, char_class_off, class_id, char_all_code, 8)
        char_output.append(char_class_code)

    # Character Items
    items = data['items']
    if items:
        for i in range(7):
            item = items[i]['item']
            fname = items[i]['forge_name']
            uses = items[i]['uses']
            blessed = items[i]['blessed']
            forged = items[i]['forged']
            mt = items[i]['mt']
            hit = items[i]['hit']
            crit = items[i]['crit']
            wt = items[i]['wt']

            item_off = hex(int(get_offset(char, 'Item', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)
            item_uses_off = hex(int(get_offset(char, 'Item_Uses', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)
            item_status_off = hex(int(get_offset(char, 'Item_Status', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)
            item_forge_off = hex(int(get_offset(char, 'Item_Forge', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)

            if item:
                item_id = get_offset(item, 'Item', 'Item')
                char_item_code = code_gen(char, item_off, item_id, char_all_code, 8)
                char_output.append(char_item_code)

            if uses or item:
                uses = 80 if uses == '' else uses
                ucheck = int_check(uses)
                if ucheck:
                    uses = int(uses)
                    uses = hex(uses).replace('0x', '').zfill(2).upper()
                    char_item_uses_code = code_gen(char, item_uses_off, uses, char_all_code, 2)
                    char_output.append(char_item_uses_code)
                else:
                    return error_output(item, 'Uses', 0, 255)

            if blessed or forged or item:
                sts = (int('10', 16) if blessed else 0) + (int('20', 16) if forged else 0)
                status = hex(sts).replace('0x', '').zfill(2).upper()
                char_status_code = code_gen(char, item_status_off, status, char_all_code, 2)
                char_output.append(char_status_code)

                if forged:
                    if item:
                        fname_hex = ''.join([format(ord(c), "x").zfill(2) for c in (fname if fname and 0 < len(fname) <= 26 else item)]).ljust(52, '0').upper()
                        for k in range(7):
                            fname_offset = hex(int(item_off, 16) + (6 if k == 0 else 8 + (k - 1) * 4)).replace('0x', '').zfill(8).upper()
                            if k == 0:
                                char_fname_code = code_gen(char, fname_offset, fname_hex[:4], char_all_code, 4)
                            else:
                                if fname_hex[4 + (k - 1) * 8:12 + (k - 1) * 8] == '00000000':
                                    break
                                char_fname_code = code_gen(char, fname_offset, fname_hex[4 + (k - 1) * 8:12 + (k - 1) * 8], char_all_code, 8)
                            char_output.append(char_fname_code)
                    else:
                        pass

                    for stat in [mt, hit, crit]:
                        if stat:
                            scheck = int_check(stat)
                            if scheck:
                                stat = hex(int(stat)).replace("0x", "").zfill(2).upper()
                                forge_stat_code = code_gen(char, item_forge_off, stat, char_all_code, 2)
                                char_output.append(forge_stat_code)
                            else:
                                return error_output(item, 'Forge Stat', 0, 255)
                        item_forge_off = hex(int(item_forge_off, 16) + 1).replace("0x", "").zfill(8).upper()
                    
                    if wt:
                        forge_wt_code = code_gen(char, item_forge_off, 'E0', char_all_code, 2)
                        char_output.append(forge_wt_code)

    # Character Stats

    for chstat, char_stat in enumerate(CHAR_STATS):
        char_stat_input = data['stats'][chstat]
        char_stat_offset = get_offset(char, char_stat, 'Char')
        if char_stat_input:
            cscheck = int_check(char_stat_input)
            if cscheck:
                char_stat_input = hex(int(char_stat_input)).replace("0x", "").zfill(2).upper()
                char_stat_code = code_gen(char, char_stat_offset, char_stat_input, char_all_code, 2)
                char_output.append(char_stat_code)
            else:
                return error_output(char_stat.replace("_", " "), 'Stat', 0, 20 if char_stat == "Level" else 99 if char_stat == "EXP" else 255)

    # Character Ranks

    for chwr, char_rank in enumerate(CHAR_RANKS):
        char_rank_input = data['ranks'][chwr]
        char_rank_offset = get_offset(char, char_rank, 'Char')
        if char_rank_input:
            rank = {'SS': '014B', 'S': '00FB', 'A': '00B5', 'B': '0079', 'C': '0047', 'D': '001F', 'E': '0001'}.get(char_rank_input)
            char_rank_code = code_gen(char, char_rank_offset, rank, char_all_code, 4)
            char_output.append(char_rank_code)

    return "Error: No changes made!" if len(char_output) == 0 else "\n".join(char_output)

def get_class_code(data):
    class_all_code = '0AA011C 00000000'
    class_output = []

    cls = data['class']
    if not cls:
        return "Error: No class selected!"

    # Promote

    promote = data['promote']
    if promote:
        class_promote_off = get_offset(cls, 'Next_Class', 'Class')
        class_id = get_offset(promote, 'Class', 'Class')
        class_promote_code = code_gen(cls, class_promote_off, class_id, class_all_code, len(class_id))
        class_output.append(class_promote_code)

    # Class Ranks

    class_ranks = ['Min_' + i for i in CHAR_RANKS] + ['Max_' + i for i in CHAR_RANKS]
    for clwr, class_rank in enumerate(class_ranks):
        class_rank_input = data['ranks'][clwr]
        class_rank_offset = get_offset(cls, class_rank, 'Class')
        if class_rank_input:
            rank = {'SS': '014B', 'S': '00FB', 'A': '00B5', 'B': '0079', 'C': '0047', 'D': '001F', 'E': '0001'}.get(class_rank_input)
            class_rank_code = code_gen(cls, class_rank_offset, rank, class_all_code, 4)
            class_output.append(class_rank_code)

    # Class Stats

    for clstat, class_stat in enumerate(CLASS_STATS):
        class_stat_input = data['stats'][clstat]
        class_stat_offset = get_offset(cls, class_stat, 'Class')
        if class_stat_input:
            cscheck = int_check(class_stat_input)
            if cscheck:
                class_stat_input = hex(int(class_stat_input)).replace("0x", "").zfill(2).upper()
                class_stat_code = code_gen(cls, class_stat_offset, class_stat_input, class_all_code, 2)
                class_output.append(class_stat_code)
            else:
                return error_output(class_stat, 'Stat', 0, 255)

    return "Error: No changes made!" if len(class_output) == 0 else "\n".join(class_output)

def get_item_code(data):
    item_all_code = '1270050 00000000'
    item_output = []

    item = data['item']
    if not item:
        return "Error: No item selected!"

    # Item Data

    for item_data in ITEM_DATA:
        item_data_input = data['data'][item_data]
        item_data_offset = get_offset(item, item_data, 'Item')

        if item_data_input:
            if item_data == 'Attack_Type':
                str_mag = {'ATK': '00', 'MAG': '06'}.get(item_data_input)
                str_mag_code = code_gen(item, item_data_offset, str_mag, item_all_code, 2)
                item_output.append(str_mag_code)

            elif item_data == 'Weapon_Rank':
                rank = {'SS': '014B', 'S': '00FB', 'A': '00B5', 'B': '0079', 'C': '0047', 'D': '001F', 'E': '0001'}.get(item_data_input)
                rank_code = code_gen(item, item_data_offset, rank, item_all_code, 4)
                item_output.append(rank_code)

            elif item_data == 'EXP Gain':
                expcheck = int_check(item_data_input)
                if expcheck:
                    exp = hex(int(item_data_input)).replace('0x', '').zfill(2).upper()
                    exp_code = code_gen(item, item_data_offset, exp, item_all_code, 2)
                    item_output.append(exp_code)
                else:
                    return error_output(item, "EXP Gain", 0, 255)

            elif item_data == 'Unlock':
                unlock_code = code_gen(item, item_data_offset, '00', item_all_code, 2)
                item_output.append(unlock_code)

            elif item_data in ['Infinite', 'Brave']:
                inf_brave_code = code_gen(item, item_data_offset, '01', item_all_code, 2)
                item_output.append(inf_brave_code)

            elif item_data == 'Char_Unlock':
                char_unlock_code = code_gen(item, item_data_offset, '0000', item_all_code, 4)
                item_output.append(char_unlock_code)

            elif item_data == 'Heal':
                heal_code = code_gen(item, item_data_offset, '10', item_all_code, 2)
                item_output.append(heal_code)

    # Item Stats

    for istat, item_stat in enumerate(ITEM_STATS):
        item_stat_input = data['stats'][istat]
        item_stat_offset = get_offset(item, item_stat, 'Item')

        if item_stat_input:
            ischeck = int_check(item_stat_input)
            if ischeck:
                item_stat_input = hex(int(item_stat_input)).replace("0x", "").zfill(2).upper()
                item_stat_code = code_gen(item, item_stat_offset, item_stat_input, item_all_code, 2)
                item_output.append(item_stat_code)
            else:
                return error_output(item_stat, "Stat", 0, 255)

    # Item Equip Bonuses

    for ibonus, bonus in enumerate(ITEM_EQUIP_BONUS):
        item_bonus_input = data['bonuses'][ibonus]
        item_bonus_offset = get_offset(item, bonus, 'Item')

        if item_bonus_input:
            ibcheck = int_check(item_bonus_input)
            if ibcheck:
                item_bonus_input = hex(int(item_bonus_input)).replace("0x", "").zfill(2).upper()
                item_bonus_code = code_gen(item, item_bonus_offset, item_bonus_input, item_all_code, 2)
                item_output.append(item_bonus_code)
            else:
                return error_output(bonus, "Equip Bonus", 0, 255)

    if len(item_output) == 0:
        return "Error: No changes made!"
    return "\n".join(item_output)

def get_keybind_code(data):
    def calculate_val(keys, mapping):
        return sum(int(mapping[i], 16) for i, key in enumerate(keys) if key)

    if data['controller'] == 'None - Always On':
        if VERSION == 'NTSC':
            if OFFSET_MOD == 0:
                return '20B54158 8070F8BC'
            else:
                return '20B540D8 8070F83C'
        elif VERSION == 'PAL':
            return '20B58CF8 80701E3C'
        elif VERSION == 'RR':
            return '20B58B58 80701E2C'

    controller_mappings = {
        'Wiimote+Nunchuck': [
            '1', '2', '8', '4', '800', '400', '4000', '2000', '200', '100', '10', '1000'
        ],
        'Classic': [
            '2', '8000', '1', '4000', '10', '40', '8', '20', '80', '4', '2000', '200', '400', '1000'
        ],
        'GameCube': [
            '1', '2', '8', '4', '100', '200', '400', '800', '10', '40', '20', '1000'
        ]
    }

    version_mappings = {
        'Wiimote+Nunchuck': '28',
        'Classic': (
            '283D79BA' if VERSION == 'NTSC' and OFFSET_MOD == 0 else
            '283D793A' if VERSION == 'NTSC' and OFFSET_MOD != 0 else
            '283D035A'),
        'GameCube': (
            '283D7928' if VERSION == 'NTSC' and OFFSET_MOD == 0 else
            '283D78A8' if VERSION == 'NTSC' and OFFSET_MOD != 0 else
            '283D02C8')
    }

    controller = data['controller']
    val = calculate_val(data['keys'], controller_mappings[controller])
    return f"{version_mappings[controller]} {hex(val).replace('0x', '').zfill(8)}"