def handleDatabase(data, version):

    desc = data['DESC']
    code = data[version]
    
    return [desc, code]