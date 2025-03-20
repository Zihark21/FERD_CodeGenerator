from .. import config

def handleOffset(name, data, opt):

    from .globals import getGlobals
    glb = getGlobals()
    character_list = glb[2]
    off_mod = glb[1]
    diff_mod = glb[4]
    version = glb[0]

    def calculate_offset(base, offset, id, additional_offset):

        off = int(base, 16) + off_mod + (offset * id) + additional_offset
        return hex(off).replace('0x', '').upper().zfill(8)

    def get_data(name, data, opt_list, opt_type, opt_offset):

        if name == 'All':
            id = 0
        elif isinstance(opt_list[name], int):
            id = opt_list[name]
        else:
            id = opt_list[name][diff_mod]
        base = config.base_offsets[version][opt_type]
        offset = opt_offset[opt_type]
        if data != opt_type:
            additional_offset = opt_offset[data]
        else:
            additional_offset = 0

        return id, base, offset, additional_offset

    if opt == 'Char':
        id, base, offset, additional_offset = get_data(name, data, character_list, 'Character', config.character_offset)

    elif opt == 'Class':
        id, base, offset, additional_offset = get_data(name, data, config.class_id, 'Class', config.class_offset)

    elif opt == 'Item':
        id, base, offset, additional_offset = get_data(name, data, config.item_id, 'Item', config.item_offset)

    elif opt == 'Model':
        id, base, offset, additional_offset = get_data(name, data, config.character_model, 'Model', config.character_offset)
        offset = 1

    else:
        id = None
        base = None
        offset = None
        additional_offset = None

    if id is not None and base is not None and offset is not None:
        return calculate_offset(base, offset, id, additional_offset)

    return None

