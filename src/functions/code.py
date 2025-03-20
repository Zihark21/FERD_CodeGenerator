def code_gen(data, off, val, all_code, code_type):
    
    if data == 'All':
        off_prefix = '08'
        if code_type == 2:
            val_prefix = '000000'
            loop_prefix = '0'
        elif code_type == 4:
            val_prefix = '0000'
            loop_prefix = '1'
        elif code_type == 8:
            val_prefix = ''
            loop_prefix = '2'
        else:
            return 'Error: Invalid code type!'

        return f'{off_prefix}{off[-6:]} {val_prefix}{val}\n{loop_prefix}{all_code}'
    
    else:
        if code_type == 2:
            off_prefix = '00'
            val_prefix = '000000'
        if code_type == 4:
            off_prefix = '02'
            val_prefix = '0000'
        if code_type == 8:
            off_prefix = '04'
            val_prefix = ''

        return f'{off_prefix}{off[-6:]} {val_prefix}{val}'