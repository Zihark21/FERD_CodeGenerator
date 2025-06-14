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

        if input:
            if header == 'Attack_Type':
                offset = handleOffset(ITEM, header, 'Item')
                code.append(code_gen(ITEM, offset, config.attack_type.get(input), ALL, 2))

            elif header == 'Rank':
                offset = handleOffset(ITEM, header, 'Item')
                code.append(code_gen(ITEM, offset, config.rank_map.get(input), ALL, 4))
            
            elif header == 'Effectiveness':
                offset = handleOffset(ITEM, header, 'Item')
                effect = 0
                for i, j in enumerate(input):
                    if j:
                        effect += int(list(config.weapon_effectiveness.values())[i], 16)
                effect = hex(effect).replace("0x", "").zfill(4).upper()
                if effect != '0000':
                    code.append(code_gen(ITEM, offset, effect, ALL, 4))

            elif header == 'Misc':
                for m, i in zip(list(config.weapon_misc), input):
                    if i:
                        offset = handleOffset(ITEM, m, 'Item')
                        _misc = config.weapon_misc.get(m)
                        code.append(code_gen(ITEM, offset, _misc, ALL, len(_misc)))

            elif header == 'Effects':
                if input != 'None':
                    offset = handleOffset(ITEM, header, 'Item')
                    code.append(code_gen(ITEM, offset, config.weapon_effects.get(input), ALL, 2))

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