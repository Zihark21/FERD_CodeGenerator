from .. import config
from .globals import error_output, int_check
from .offset import handleOffset
from .code import code_gen

def handleClass(data) -> str:

    global ALL, CLS
    ALL = '0AA011C 00000000'
    CLS = data['class']

    output: list[str] = []

    if not CLS:
        return "Error: No class selected!"
    
    output.extend(_promote(data))
    output.extend(_stats(data))
    output.extend(_ranks(data))
    
    return "Error: No changes made!" if len(output) == 0 else "\n".join(output)

def _promote(data) -> str:

    code: list[str] = []

    if data['promote']:
        offset = handleOffset(CLS, 'Next_Class', 'Class')
        id = handleOffset(data['promote'], 'Class', 'Class')
        code.append(code_gen(CLS, offset, id, ALL, 8))

    return code

def _ranks(data) -> list[str]:

    code: list[str] = []

    ranks = ['Min_' + i for i in config.character_ranks] + ['Max_' + i for i in config.character_ranks]

    for i, rank in enumerate(ranks):
        input = data['ranks'][i]
        offset = handleOffset(CLS, rank, 'Class')
        if input:
            code.append(code_gen(CLS, offset, config.rank_map.get(input), ALL, 4))

    return code

def _stats(data) -> list[str]:

    code: list[str] = []

    for i, stat in enumerate(config.class_stats):
        input = data['stats'][i]
        offset = handleOffset(CLS, stat, 'Class')
        if input:
            if int_check(input):
                input = hex(int(input)).replace("0x", "").zfill(2).upper()
                code.append(code_gen(CLS, offset, input, ALL, 2))
            else:
                return error_output(stat, 'Stat', 0, 255)

    return code