def handleDatabase(data):

    from .globals import getGlobals
    glb = getGlobals()
    version = glb[0]

    desc = data['DESC']
    code = data[version]
    
    return [desc, code]