def handleKeybind(data):

    from .globals import getGlobals
    glb = getGlobals()
    off_mod = glb[1]
    version = glb[0]

    if data['controller'] == 'None - Always On':
        if version == 'NTSC':
            if off_mod == 0:
                return '20B54158 8070F8BC'
            else:
                return '20B540D8 8070F83C'
        elif version == 'PAL':
            return '20B58CF8 80701E3C'
        elif version == 'RR':
            return '20B58B58 80701E2C'

    controller_mappings = {
        'Wiimote+Nunchuck': [
            '1', '2', '8', '4', '800', '400', '4000', '2000', '200', '100', '10', '1000'
        ],
        'Classic': [
            '2', '8000', '1', '4000', '10', '40', '8', '20', '80', '4', '2000', '200', '400', '1000'
        ],
        'GameCube': [
            '1', '2', '8', '4', '100', '200', '400', '800', '10', '40', '20', '1000'
        ]
    }

    version_mappings = {
        'Wiimote+Nunchuck': '28',
        'Classic': (
            '283D79BA' if version == 'NTSC' and off_mod == 0 else
            '283D793A' if version == 'NTSC' and off_mod != 0 else
            '283D035A'),
        'GameCube': (
            '283D7928' if version == 'NTSC' and off_mod == 0 else
            '283D78A8' if version == 'NTSC' and off_mod != 0 else
            '283D02C8')
    }

    controller = data['controller']
    val = getKeyVal(data['keys'], controller_mappings[controller])
    return f"{version_mappings[controller]} {hex(val).replace('0x', '').zfill(8)}"

def getKeyVal(keys, mapping):
    return sum(int(mapping[i], 16) for i, key in enumerate(keys) if key)