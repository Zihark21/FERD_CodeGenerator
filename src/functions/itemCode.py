from .. import config
from .globals import error_output, int_check
from .offset import handleOffset
from .code import code_gen

def handleItem(data) -> str:

    global ALL, ITEM

    ALL = '1270050 00000000'
    ITEM = data['item']

    item_output = []

    if not ITEM:
        return "Error: No item selected!"
    
    item_output.extend(_data(data))
    item_output.extend(_stats(data))
    item_output.extend(_bonuses(data))
    
    return "Error: No changes made!" if len(item_output) == 0 else "\n".join(item_output)

def _data(data) -> list[str]:

    code: list[str] = []

    for header in config.item_data:
        input = data['data'][header]
        offset = handleOffset(ITEM, header, 'Item')

        if input:
            if header == 'Attack_Type':
                str_mag = config.attack_type.get(input)
                code.append(code_gen(ITEM, offset, str_mag, ALL, 2))

            elif header == 'Weapon_Rank':
                code.append(code_gen(ITEM, offset, config.rank_map.get(input), ALL, 4))

            elif header == 'EXP Gain':
                expcheck = int_check(input)
                if expcheck:
                    exp = hex(int(input)).replace('0x', '').zfill(2).upper()
                    code.append(code_gen(ITEM, offset, exp, ALL, 2))
                else:
                    return error_output(ITEM, "EXP Gain", 0, 255)

            elif header == 'Unlock':
                code.append(code_gen(ITEM, offset, '00', ALL, 2))

            elif header in ['Infinite', 'Brave']:
                code.append(code_gen(ITEM, offset, '01', ALL, 2))

            elif header == 'Char_Unlock':
                code.append(code_gen(ITEM, offset, '0000', ALL, 4))

            elif header == 'Heal':
                code.append(code_gen(ITEM, offset, '10', ALL, 2))

    return code

def _stats(data) -> list[str]:

    code: list[str] = []

    for i, stat in enumerate(config.item_stats):
        input = data['stats'][i]
        offset = handleOffset(ITEM, stat, 'Item')

        if input:
            if int_check(input):
                input = hex(int(input)).replace("0x", "").zfill(2).upper()
                code.append(code_gen(ITEM, offset, input, ALL, 2))
            else:
                return error_output(stat, "Stat", 0, 255)
            
    return code

def _bonuses(data) -> list[str]:

    code: list[str] = []

    for i, bonus in enumerate(config.item_bonus):
        input = data['bonuses'][i]
        offset = handleOffset(ITEM, bonus, 'Item')

        if input:
            if int_check(input):
                input = hex(int(input)).replace("0x", "").zfill(2).upper()
                code.append(code_gen(ITEM, offset, input, ALL, 2))
            else:
                return error_output(bonus, "Equip Bonus", 0, 255)
            
    return code