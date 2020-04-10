

def fsl_settings():
    return [
        {
            'l': 1,
            'm': 10,
            'p': 0.3,
            's': 1,
            'x': 10,
            'w': 256,
            'compress': False,
            'regions': True
        },
        {
            'l': 1,
            'm': 5,
            'p': 0.3,
            's': 2,
            'x': 100,
            'w': 500,
            'compress': False,
            'regions': True
        },
        {
            'l': 2,
            'm': 5,
            'p': 0.049,
            's': 2,
            'x': 100,
            'w': 500,
            'compress': False,
            'regions': True
        }

    ]


def pearson_settings():
    PEARSON_1 = {
        'compress': False,
        'regions': True
    }
    return [PEARSON_1]
