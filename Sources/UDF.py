from Sources.Config import BASE, CHAR, CLASS, ITEM, CHAR_STATS, CHAR_RANKS, CLASS_STATS, ITEM_STATS, ITEM_DATA, ITEM_BONUS

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
    return VERSION

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

    if CHAR[VERSION].get(char) == 'Unknown':
        return f"{char} ID unknown in the {VERSION} version of the game. Please report on my discord."

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