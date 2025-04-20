def handleDatabase(data, base):

    desc = data['DESC']
    keybind = data['KEYBIND']
    code = data[base['version']]
    header = ''

    if keybind == 'False':
        if base['version'] == 'NTSC 1.0':
            header = '203CD7F0 80CEB7E0'
        elif base['version'] == 'NTSC 1.01':
            header = '203CD870 80CEB860'
        elif base['version'] == 'PAL':
            header = '203C6210 80CE6C20'
        else:
            header = 'E0000000 80008000'

    return [desc, header, code, keybind]
