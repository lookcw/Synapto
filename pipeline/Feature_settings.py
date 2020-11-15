import numpy as np


def fsl_settings():
    ls = range(2, 10, 5)
    ps = np.arange(0.049, .4, .1)
    ms = [10]
    ss = [1]
    windows = list(zip(range(10, 300, 100), range(100, 1000, 400)))
    regions = [True, False]
    configs = []
    for l in ls:
        for p in ps:
            for m in ms:
                for s in ss:
                    for window in windows:
                        configs.append({
                            'l': l,
                            'm': m,
                            'p': p,
                            's': s,
                            'x': window[0],
                            'w': window[1],
                            'compress': False,
                            'pairwise_regionalization': 'synchrony_128'
                        })
    optimal = [{
        'l': 4,
        'm': 10,
        'p': 0.049,
        's': 1,
        'x': 200,
        'w': 2000,
        'compress': False,
        'pairwise_regionalization': 'synchrony_128'
    }
    ]
    return configs

def pearson_settings():
    PEARSON_1 = {
        'compress': False,
        'regions': False
    }
    return [PEARSON_1]

def domfreq_settings():
    lower_bounds = [2]
    upper_bounds = [10]
    configs = []
    for lower_bound in lower_bounds:
        for upper_bound in upper_bounds:
            configs.append({'lower_bound':lower_bound,'upper_bound':upper_bound})
    return configs