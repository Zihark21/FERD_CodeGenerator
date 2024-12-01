from Sources.Config import BASE, CHAR, CLASS, ITEM, CHAR_STATS, CHAR_RANKS, CLASS_STATS, ITEM_STATS, ITEM_DATA, ITEM_BONUS

def set_version(ver):
    version_map = {
        'NTSC 1.00': ('NTSC', -int('80', 16)),
        'NTSC 1.01': ('NTSC', 0),
        '': ('NTSC', 0),
        'PAL': ('PAL', 0)
    }
    global VERSION, NTSC_MOD
    VERSION, NTSC_MOD = version_map.get(ver, (None, None))
    return VERSION

def get_offset(name, data, opt):
    def calculate_offset(base, offset, id, additional_offset=0):
        off = int(base, 16) + NTSC_MOD + (offset * id) + additional_offset
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
        id = CHAR[VERSION][name]
        base = BASE[VERSION]['Character']
        offset = CHAR['OFFSET']['Character']
        if data != 'Character':
            additional_offset = CHAR['OFFSET'][data]
    elif opt == 'Class':
        id = CLASS['ID'][name]
        base = BASE[VERSION]['Class']
        offset = CLASS['OFFSET']['Class']
        if data != 'Class':
            additional_offset = CLASS['OFFSET'][data]
    elif opt == 'Item':
        id = ITEM['ID'][name]
        base = BASE[VERSION]['Item']
        offset = ITEM['OFFSET']['Item']
        if data != 'Item':
            additional_offset = ITEM['OFFSET'][data]

    if id is not None and base is not None and offset is not None:
        return calculate_offset(base, offset, id, additional_offset)

    return None

def get_char_code(data, kb):
    char_all_code = 'A203F0 00000000'
    char_output = [kb]

    char = data['character']
    if not char:
        return "No character selected!"
    if CHAR[VERSION].get(char) == 'Unknown':
        return f"{char} ID unknown in the {VERSION} version of the game. Please report on my discord."

    item_step = get_offset(char, 'Item_Step', 'Char')
    skill_step = get_offset(char, 'Skill_Step', 'Char')

    char_class = data['class']
    if char_class:
        char_class_off = get_offset(char, 'Class', 'Char')
        class_id = get_offset(char_class, 'Class', 'Class')
        char_class_code = f'08{char_class_off[-6:]} {class_id}\n20{char_all_code}' if char == 'All' else f'04{char_class_off[-6:]} {class_id}'
        char_output.append(char_class_code)

    for i in range(7):
        item = data['items'][i]['item']
        fname = data['items'][i]['forge_name']
        uses = data['items'][i]['uses']
        blessed = data['items'][i]['blessed']
        forged = data['items'][i]['forged']
        mt = data['items'][i]['mt']
        hit = data['items'][i]['hit']
        crit = data['items'][i]['crit']
        wt = data['items'][i]['wt']

        item_off = hex(int(get_offset(char, 'Item', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)
        item_uses_off = hex(int(get_offset(char, 'Item_Uses', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)
        item_status_off = hex(int(get_offset(char, 'Item_Status', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)
        item_forge_off = hex(int(get_offset(char, 'Item_Forge', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)

        if item:
            item_id = get_offset(item, 'Item', 'Item')
            char_item_code = f'08{item_off[-6:]} {item_id}\n20{char_all_code}' if char == 'All' else f'04{item_off[-6:]} {item_id}'
            char_output.append(char_item_code)

        if uses or item:
            uses = int(uses) if uses else 80
            if uses > 255:
                return f'Error: Uses for {item} is too high! Please enter a value between 0 and 255.'
            char_item_uses_code = f'08{item_uses_off[-6:]} 000000{uses}\n00{char_all_code}' if char == 'All' else f'00{item_uses_off[-6:]} 000000{hex(uses).replace("0x", "").zfill(2).upper()}'
            char_output.append(char_item_uses_code)

        if blessed or forged or item:
            sts = (int('10', 16) if blessed else 0) + (int('20', 16) if forged else 0)
            status = hex(sts).replace('0x', '').zfill(2).upper()
            char_status_code = f'08{item_status_off[-6:]} 000000{status}\n00{char_all_code}' if char == 'All' else f'00{item_status_off[-6:]} 000000{status}'
            char_output.append(char_status_code)

            if forged:
                fname_hex = ''.join([format(ord(c), "x").zfill(2) for c in (fname if fname and 0 < len(fname) <= 26 else item)]).ljust(52, '0').upper()
                for k in range(7):
                    fname_offset = hex(int(item_off, 16) + (6 if k == 0 else 8 + (k - 1) * 4)).replace('0x', '').zfill(8).upper()
                    char_fname_code = f'08{fname_offset[-6:]} 0000{fname_hex[:4]}\n10{char_all_code}' if k == 0 and char == 'All' else f'02{fname_offset[-6:]} 0000{fname_hex[:4]}' if k == 0 else f'08{fname_offset[-6:]} {fname_hex[4 + (k - 1) * 8:12 + (k - 1) * 8]}\n20{char_all_code}' if char == 'All' else f'04{fname_offset[-6:]} {fname_hex[4 + (k - 1) * 8:12 + (k - 1) * 8]}'
                    if char_fname_code[-8:] != '00000000':
                        char_output.append(char_fname_code)

                if mt or hit or wt or crit:
                    mt, hit, crit = int(mt or 0), int(hit or 0), int(crit or 0)
                    if any(stat > 255 for stat in [mt, hit, crit]):
                        return f'Error: Stat for {item} is too high! Please enter a value between 0 and 255.'
                    wt = 'E0' if wt else '00'
                    mt_hit_code = f'08{item_forge_off[-6:]} 0000{hex(mt).replace("0x", "").zfill(2).upper()}{hex(hit).replace("0x", "").zfill(2).upper()}\n10{char_all_code}' if char == 'All' else f'02{item_forge_off[-6:]} 0000{hex(mt).replace("0x", "").zfill(2).upper()}{hex(hit).replace("0x", "").zfill(2).upper()}'
                    crit_wt_off = hex(int(item_forge_off, 16) + 2).replace("0x", "").zfill(8).upper()
                    crit_wt_code = f'08{crit_wt_off[-6:]} 0000{hex(crit).replace("0x", "").zfill(2).upper()}{wt}\n10{char_all_code}' if char == 'All' else f'02{crit_wt_off[-6:]} 0000{hex(crit).replace("0x", "").zfill(2).upper()}{wt}'
                    char_output.append(mt_hit_code)
                    char_output.append(crit_wt_code)

    for chstat, char_stat in enumerate(CHAR_STATS):
        char_stat_input = data['stats'][chstat]
        char_stat_offset = get_offset(char, char_stat, 'Char')
        if char_stat_input:
            char_stat_num = int(char_stat_input)
            if (char_stat == 'Level' and char_stat_num > 20) or (char_stat == 'EXP' and char_stat_num > 99) or char_stat_num > 255:
                return f'Error: Stat for {char_stat.replace("_", " ")} is too high! Please enter a value between 0 and {20 if char_stat == "Level" else 99 if char_stat == "EXP" else 255}.'
            char_stat_code = f'08{char_stat_offset[-6:]} 000000{hex(char_stat_num).replace("0x", "").zfill(2).upper()}\n00{char_all_code}' if char == 'All' else f'00{char_stat_offset[-6:]} 000000{hex(char_stat_num).replace("0x", "").zfill(2).upper()}'
            char_output.append(char_stat_code)

    for chwr, char_rank in enumerate(CHAR_RANKS):
        char_rank_input = data['ranks'][chwr]
        char_rank_offset = get_offset(char, char_rank, 'Char')
        if char_rank_input:
            rank = {'SS': '014B', 'S': '00FB', 'A': '00B5', 'B': '0079', 'C': '0047', 'D': '001F', 'E': '0001'}.get(char_rank_input)
            if not rank:
                return f'Error: Invalid weapon rank for {char_rank.replace("_", " ")}! Please select a valid rank.'
            char_rank_code = f'08{char_rank_offset[-6:]} 0000{rank}\n10{char_all_code}' if char == 'All' else f'02{char_rank_offset[-6:]} 0000{rank}'
            char_output.append(char_rank_code)

    char_output.append('E0000000 80008000')
    return "No changes made!" if len(char_output) == 2 else "\n".join(char_output)

def get_class_code(data):
    class_all_code = 'AA011C 00000000'
    class_output = ['20B54158 8070F8BC' if VERSION == 'NTSC' else '20B58CF8 80701E3C']

    cls = data['class']
    if not cls:
        return "No class selected!"

    promote = data['promote']
    if promote:
        class_promote_off = get_offset(cls, 'Next_Class', 'Class')
        class_id = get_offset(promote, 'Class', 'Class')
        class_promote_code = f'08{class_promote_off[-6:]} {class_id}\n20{class_all_code}' if cls == 'All' else f'04{class_promote_off[-6:]} {class_id}'
        class_output.append(class_promote_code)

    class_ranks = ['Min_' + i for i in CHAR_RANKS] + ['Max_' + i for i in CHAR_RANKS]
    for clwr, class_rank in enumerate(class_ranks):
        class_rank_input = data['ranks'][clwr]
        class_rank_offset = get_offset(cls, class_rank, 'Class')
        if class_rank_input:
            rank_map = {'SS': '014B', 'S': '00FB', 'A': '00B5', 'B': '0079', 'C': '0047', 'D': '001F', 'E': '0001'}
            rank = rank_map.get(class_rank_input)
            if not rank:
                return f'Error: Invalid weapon rank for {class_rank.replace("_", " ")}! Please select a valid rank.'
            class_rank_code = f'08{class_rank_offset[-6:]} 0000{rank}\n10{class_all_code}' if cls == 'All' else f'02{class_rank_offset[-6:]} 0000{rank}'
            class_output.append(class_rank_code)

    for clstat, class_stat in enumerate(CLASS_STATS):
        class_stat_input = data['stats'][clstat]
        class_stat_offset = get_offset(cls, class_stat, 'Class')
        if class_stat_input:
            try:
                class_stat_num = int(class_stat_input)
                if class_stat_num > 255:
                    return f'Error: Stat for {class_stat.replace("_", " ")} is too high! Please enter a value between 0 and 255.'
                class_stat_code = f'08{class_stat_offset[-6:]} 000000{hex(class_stat_num).replace("0x", "").zfill(2).upper()}\n00{class_all_code}' if cls == 'All' else f'00{class_stat_offset[-6:]} 000000{hex(class_stat_num).replace("0x", "").zfill(2).upper()}'
                class_output.append(class_stat_code)
            except ValueError:
                return f'Error: Stat for {class_stat} is not a number! Please enter a value between 0 and 255.'

    class_output.append('E0000000 80008000')
    return "No changes made!" if len(class_output) == 2 else "\n".join(class_output)

def get_item_code(data):
    item_all_code = 'CA0050 00000000'
    item_output = []

    version_start_codes = {
        'NTSC': '20B54158 8070F8BC',
        'PAL': '20B58CF8 80701E3C'
    }
    item_output.append(version_start_codes.get(VERSION, ''))

    item = data['item']
    if not item:
        return "No item selected!"

    def append_code(offset, value, all_code_suffix='00'):
        if item == 'All':
            return f'08{offset[-6:]} 000000{value}\n{all_code_suffix}{item_all_code}'
        return f'00{offset[-6:]} 000000{value}'

    def append_code_2(offset, value, all_code_suffix='10'):
        if item == 'All':
            return f'08{offset[-6:]} 0000{value}\n{all_code_suffix}{item_all_code}'
        return f'02{offset[-6:]} 0000{value}'

    def get_hex_value(value, length=2):
        return hex(int(value)).replace("0x", "").zfill(length).upper()

    # Item Data
    for item_data in ITEM_DATA:
        item_data_input = data['data'][item_data]
        item_data_offset = get_offset(item, item_data, 'Item')

        if item_data_input:
            if item_data == 'Attack_Type':
                str_mag = {'STR': '00', 'MAG': '06'}.get(item_data_input)
                if not str_mag:
                    return f'Error: Invalid attack type for {item}! Please select a valid type.'
                item_output.append(append_code(item_data_offset, str_mag))

            elif item_data == 'Weapon_Rank':
                rank = {
                    'SS': '014B', 'S': '00FB', 'A': '00B5', 'B': '0079',
                    'C': '0047', 'D': '001F', 'E': '0001'
                }.get(item_data_input)
                if not rank:
                    return f'Error: Invalid weapon rank for {item}! Please select a valid rank.'
                item_output.append(append_code_2(item_data_offset, rank))

            elif item_data == 'EXP Gain':
                item_output.append(append_code(item_data_offset, get_hex_value(item_data_input)))

            elif item_data == 'Unlock' and item_data_input:
                item_output.append(append_code(item_data_offset, '00'))

            elif item_data in ['Infinite', 'Brave'] and item_data_input:
                item_output.append(append_code(item_data_offset, '01'))

            elif item_data == 'Char_Unlock' and item_data_input:
                item_output.append(append_code_2(item_data_offset, '0000'))

            elif item_data == 'Heal' and item_data_input:
                item_output.append(append_code(item_data_offset, '10'))

    # Item Stats
    for istat, item_stat in enumerate(ITEM_STATS):
        item_stat_input = data['stats'][istat]
        item_stat_offset = get_offset(item, item_stat, 'Item')

        if item_stat_input:
            try:
                item_stat_num = int(item_stat_input)
                if item_stat_num > 255:
                    return f'Error: Stat for {item_stat.replace("_", " ")} is too high! Please enter a value between 0 and 255.'
                item_output.append(append_code(item_stat_offset, get_hex_value(item_stat_num)))
            except ValueError:
                return f'Error: Stat for {item_stat} is not a number! Please enter a value between 0 and 255.'

    # Item Equip Bonuses
    for ibonus, bonus in enumerate(ITEM_BONUS):
        item_bonus_input = data['bonuses'][ibonus]
        item_bonus_offset = get_offset(item, bonus, 'Item')

        if item_bonus_input:
            try:
                bonus_num = int(item_bonus_input)
                if bonus_num > 255:
                    return f'Error: Equip Bonus for {bonus.replace("_", " ")} is too high! Please enter a value between 0 and 255.'
                item_output.append(append_code(item_bonus_offset, get_hex_value(bonus_num)))
            except ValueError:
                return f'Error: Equip Bonus for {bonus} is not a number! Please enter a value between 0 and 255.'

    item_output.append('E0000000 80008000')

    if len(item_output) == 2:
        return "No changes made!"
    return "\n".join(item_output)

def get_keybind_code(data):
    def calculate_val(keys, mapping):
        return sum(int(mapping[i], 16) for i, key in enumerate(keys) if key)

    if data['controller'] == '':
        return '20B54158 8070F8BC' if VERSION == 'NTSC' else '20B58CF8 80701E3C'

    controller_mappings = {
        'Wiimote+Nunchuck': [
            '1', '2', '8', '4', '800', '400', '4000', '2000', '200', '100', '10', '1000'
        ],
        'Classic Controller': [
            '2', '8000', '1', '4000', '10', '40', '8', '20', '80', '4', '2000', '200', '400', '1000'
        ],
        'GameCube Controller': [
            '1', '2', '8', '4', '100', '200', '400', '800', '10', '40', '20', '1000'
        ]
    }

    version_mappings = {
        'Wiimote+Nunchuck': '28',
        'Classic Controller': '283D79BA' if VERSION == 'NTSC' else '283D035A',
        'GameCube Controller': '283D7928' if VERSION == 'NTSC' else '283D02C8'
    }

    controller = data['controller']
    val = calculate_val(data['keys'], controller_mappings[controller])
    return f"{version_mappings[controller]} {hex(val).replace('0x', '').zfill(8)}"