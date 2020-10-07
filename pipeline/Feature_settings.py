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
                            'regions': False
                        })
    optimal = [{
        'l': 4,
        'm': 10,
        'p': 0.049,
        's': 1,
        'x': 200,
        'w': 2000,
        'compress': False,
        'pairwise_regionalization': 'synchrony'
    }
    ]
    return optimal

# FSL-None_NCFN50_1_instances_23808_epochs_1_timepoints_l:2,m:10,p:0.049,s:1,x:110,w:500,compress:False,regions:True.csv

    # return [
    #     {
    #         'l': 1,
    #         'm': 10,
    #         'p': 0.3,
    #         's': 1,
    #         'x': 10,
    #         'w': 256,
    #         'compress': False,
    #         'regions': True
    #     },
    #     {
    #         'l': 1,
    #         'm': 5,
    #         'p': 0.3,
    #         's': 2,
    #         'x': 100,
    #         'w': 500,
    #         'compress': False,
    #         'regions': True
    #     },
    #     {
    #         'l': 2,
    #         'm': 5,
    #         'p': 0.049,
    #         's': 2,
    #         'x': 100,
    #         'w': 500,
    #         'compress': False,
    #         'regions': True
    #     },
    #             {
    #         'l': 2,
    #         'm': 5,
    #         'p': 0.049,
    #         's': 3,
    #         'x': 100,
    #         'w': 2000,
    #         'compress': False,
    #         'regions': True
    #     },

    # ]


def pearson_settings():
    PEARSON_1 = {
        'compress': False,
        'regions': False
    }
    return [PEARSON_1]
