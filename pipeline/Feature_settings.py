

def fsl_settings():
    FSL_1 = {
        'l': 1,
        'm': 10,
        'p': 0.3,
        's': 1,
        'x': 10,
        'w': 256,
        'compress':True,
        'regions': False
    }
    FSL_2 = {
        'l': 1,
        'm': 5,
        'p': 0.3,
        's': 2,
        'x': 100,
        'w': 500
    }
    return [FSL_1]

def pearson_settings():
    PEARSON_1 = {
        'compress': False,
        'regions': True
    }
    return [PEARSON_1]