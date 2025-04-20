from .. import config
from .globals import error_output, int_check
from .offset import handleOffset

def handleSelected(data, version) -> str:

    sel_offset: str = ''

    if version == 'NTSC 1.0':
        sel_offset = '48000000 803C91F0'
    elif version == 'NTSC 1.01':
        sel_offset = '48000000 803C9270'
    elif version == 'PAL':
        sel_offset = '48000000 ????????'

    output = [sel_offset]

    output.extend(_class(data))
    output.extend(_stats(data))
    output.extend(_ranks(data))

    return "Error: No changes made!" if len(output) == 1 else "\n".join(output)

def _class(data) -> list[str]:

    code: list[str] = []

    if data['class']:
        offset = _offset_calc('Class', 8)
        id = handleOffset(data['class'], 'Class', 'Class')
        code.append(f'{offset} {id}')

    return code

def _stats(data) -> list[str]:

    code: list[str] = []

    for i, stat in enumerate(config.character_stats):
        input = data['stats'][i]
        if input:
            offset = _offset_calc(stat, 2)
            if int_check(input):
                id = hex(int(input)).replace("0x", "").zfill(8).upper()
                code.append(f'{offset} {id}')
            else:
                return error_output(stat.replace("_", " "), 'Stat', 0, 20 if stat == "Level" else 99 if stat == "EXP" else 255)

    return code

def _ranks(data) -> list[str]:

    code: list[str] = []

    for i, rank in enumerate(config.character_ranks):
        input = data['ranks'][i]
        if input:
            offset = _offset_calc(rank, 4)
            id = config.rank_map.get(input).zfill(8).upper()
            code.append(f'{offset} {id}')

    return code

def _offset_calc(off_type: str, size: int) -> str:

    selected = config.character_offset.get("Selected", None)

    offset = config.character_offset.get(off_type, None)

    hex_offset = hex(selected + offset).replace("0x", "").zfill(6).upper()

    if size == 2:
        hex_offset = '10' + hex_offset
    elif size == 4:
        hex_offset = '12' + hex_offset
    elif size == 8:
        hex_offset = '14' + hex_offset

    return hex_offset