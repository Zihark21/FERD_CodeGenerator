from .functions.globals import handleGlobals
from .functions.keybindCode import handleKeybind
from .functions.charCode import handleCharacter
from .functions.classCode import handleClass
from .functions.itemCode import handleItem
from .functions.database import handleDatabase

def code_handler(base, data, opt: str):

    handleGlobals(base['version'], base['difficulty'])

    if opt == 'character':
        code = handleCharacter(data)
        
    elif opt == 'class':
        code = handleClass(data)

    elif opt == 'item':
        code = handleItem(data)

    elif opt == 'database':
        code = handleDatabase(data)

    else:
        pass

    if 'Error:' not in code:
        key_code = handleKeybind(base)
        if opt == 'database':
            output = '\n'.join([code[0], key_code, code[1], 'E0000000 80008000'])
        else:
            output = '\n'.join([key_code, code, 'E0000000 80008000'])
        return output
    else:
        return code