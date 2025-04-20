from .functions.globals import handleGlobals
from .functions.keybindCode import handleKeybind
from .functions.charCode import handleCharacter
from .functions.classCode import handleClass
from .functions.itemCode import handleItem
from .functions.selectedCode import handleSelected
from .functions.database import handleDatabase

def code_handler(base, data, opt: str):

    handleGlobals(base['version'], base['difficulty'])

    if opt == 'character':
        code = handleCharacter(data)
        
    elif opt == 'class':
        code = handleClass(data)

    elif opt == 'item':
        code = handleItem(data)

    elif opt == 'selected':
        code = handleSelected(data, base['version'])

    elif opt == 'database':
        code = handleDatabase(data, base)

    else:
        pass

    if 'Error:' not in code:
        key_code = handleKeybind(base)
        if opt == 'database':
            if code[3] == "Embedded":
                output = '\n'.join([code[0], code[2]])
            else:
                if code[3] == 'False':
                    output = '\n'.join([code[0], code[1], code[2], 'E0000000 80008000'])
                else:
                    output = '\n'.join([code[0], key_code, code[2], 'E0000000 80008000'])
        else:
            output = '\n'.join([key_code, code, 'E0000000 80008000'])
        return output
    else:
        return code