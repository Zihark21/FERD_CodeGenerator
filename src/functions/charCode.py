from .. import config
from .globals import error_output, int_check, getGlobals
from .offset import handleOffset
from .code import code_gen

def handleCharacter(data) -> list[str]:

    glb = getGlobals()
    version = glb[0]
    character_list = glb[2]
    
    global ALL, CHAR
    ALL = '0A203F0 00000000'
    CHAR = data['character']
    
    output = []

    if not CHAR:
        return "Error: No character selected!"
    if CHAR not in list(character_list) and CHAR != 'All':
        return f"Error: {CHAR} ID unknown in the {version} version of the game. Please report on my discord."

    item_step = config.character_offset['Item_Step']
    # skill_step = config.character_offset['Skill_Step']

    # output.extend(_model(data))
    output.extend(_class(data))
    output.extend(_stats(data))
    output.extend(_items(data, item_step))
    output.extend(_ranks(data))
    # output.extend(_support(data))

    return "Error: No changes made!" if len(output) == 0 else "\n".join(output)

def _class(data) -> str:

    code: list[str] = []

    if data['class']:
        offset = handleOffset(CHAR, 'Class', 'Char')
        id = handleOffset(data['class'], 'Class', 'Class')
        code.append(code_gen(CHAR, offset, id, ALL, 8))
        
    return code

def _model(data) -> list[str]:

    code: list[str] = []

    if data['model']:
        offset = handleOffset(CHAR, 'Model', 'Char')
        id = handleOffset(data['model'], 'Model', 'Model')
        code.append(code_gen(CHAR, offset, id, ALL, 8))
        
    return code

def _support(data) -> list[str]:
    
    code: list[str] = []

    return code

def _items(data, item_step) -> list[str]:

    code: list[str] = []

    items = data['items']
    headers = config.character_inventory
    if items:
        for i in range(7):
            item = items[i][headers[0]]
            uses = items[i][headers[1]]
            blessed = items[i][headers[2]]
            forged = items[i][headers[3]]
            fname = items[i][headers[4]]
            mt = items[i][headers[5]]
            hit = items[i][headers[6]]
            crit = items[i][headers[7]]
            wt = items[i][headers[8]]
            clr = items[i][headers[9]]

            if not item:
                continue

            item_off = hex(int(handleOffset(CHAR, 'Item', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)
            item_uses_off = hex(int(handleOffset(CHAR, 'Item_Uses', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)
            item_status_off = hex(int(handleOffset(CHAR, 'Item_Status', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)
            item_forge_off = hex(int(handleOffset(CHAR, 'Item_Forge', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)
            item_color_off = hex(int(handleOffset(CHAR, 'Item_Color', 'Char'), 16) + (item_step * i)).replace('0x', '').upper().zfill(8)

            if item:
                id = handleOffset(item, 'Item', 'Item')
                item_code = code_gen(CHAR, item_off, id, ALL, 8)
                code.append(item_code)

            if uses or item:
                uses = 80 if uses == '' else uses
                if int_check(uses):
                    uses = int(uses)
                    uses = hex(uses).replace('0x', '').zfill(2).upper()
                    char_item_uses_code = code_gen(CHAR, item_uses_off, uses, ALL, 2)
                    code.append(char_item_uses_code)
                else:
                    return error_output(item, 'Uses', 0, 255)

            if blessed or forged or item:
                sts = (int('10', 16) if blessed else 0) + (int('20', 16) if forged else 0)
                status = hex(sts).replace('0x', '').zfill(2).upper()
                char_status_code = code_gen(CHAR, item_status_off, status, ALL, 2)
                code.append(char_status_code)

                if forged:
                    if item:
                        fname_hex = ''.join([format(ord(c), "x").zfill(2) for c in (fname if fname and 0 < len(fname) <= 26 else item)]).ljust(52, '0').upper()
                        for k in range(7):
                            fname_offset = hex(int(item_off, 16) + (6 if k == 0 else 8 + (k - 1) * 4)).replace('0x', '').zfill(8).upper()
                            if k == 0:
                                char_fname_code = code_gen(CHAR, fname_offset, fname_hex[:4], ALL, 4)
                            else:
                                if fname_hex[4 + (k - 1) * 8:12 + (k - 1) * 8] == '00000000':
                                    break
                                char_fname_code = code_gen(CHAR, fname_offset, fname_hex[4 + (k - 1) * 8:12 + (k - 1) * 8], ALL, 8)
                            code.append(char_fname_code)
                    else:
                        pass

                    for stat in [mt, hit, crit]:
                        if stat:
                            if int_check(stat):
                                stat = hex(int(stat)).replace("0x", "").zfill(2).upper()
                                forge_stat_code = code_gen(CHAR, item_forge_off, stat, ALL, 2)
                                code.append(forge_stat_code)
                            else:
                                return error_output(item, 'Forge Stat', 0, 255)
                        item_forge_off = hex(int(item_forge_off, 16) + 1).replace("0x", "").zfill(8).upper()
                    
                    if wt:
                        forge_wt_code = code_gen(CHAR, item_forge_off, 'E0', ALL, 2)
                        code.append(forge_wt_code)

                    if clr != '#808080':
                        clr = str(clr).replace('#', '').upper()
                        off = item_color_off
                        for i in range(len(clr) // 2):
                            rgb = clr[(i*2):(i*2)+2]
                            clr_code = code_gen(CHAR, off, rgb, ALL, 2)
                            code.append(clr_code)
                            off = hex(int(off, 16) + 1).replace("0x", "").zfill(8).upper()

        return code

def _stats(data) -> list[str]:

    code: list[str] = []

    for i, stat in enumerate(config.character_stats):
        input = data['stats'][i]
        if input:
            offset = handleOffset(CHAR, stat, 'Char')
            if int_check(input):
                input = hex(int(input)).replace("0x", "").zfill(2).upper()
                code.append(code_gen(CHAR, offset, input, ALL, 2))
            else:
                return error_output(stat.replace("_", " "), 'Stat', 0, 20 if stat == "Level" else 99 if stat == "EXP" else 255)
    
    return code

def _ranks(data) -> list[str]:

    code: list[str] = []

    for i, rank in enumerate(config.character_ranks):
        input = data['ranks'][i]
        if input:
            offset = handleOffset(CHAR, rank, 'Char')
            code.append(code_gen(CHAR, offset, config.rank_map.get(input), ALL, 4))

    return code