import numpy as np

def get_region_indices(schema, electrode_list):
    d = {}

    for electrode in schema:
        region = schema[electrode]
        index = electrode_list.index(electrode)
        if region not in d:
            d[region] = [index]
        else:
            d[region].append(index)

    return d


electrode_list = ['Fp1','Fpz','Fp2','F7','F3','Fz','F4','F8','FC5','FC1','FC2','FC6','M1','T7','C3','Cz','C4','T8','M2',
    'CP5','CP1','CP2','CP6','P7','P3','Pz','P4','P8','POz','O1','Oz','O2','AF7','AF3','AF4','AF8','F5','F1','F2','F6',
    'FC3','FCz','FC4','C5','C1','C2','C6','CP3','CPz','CP4','P5','P1','P2','P6','PO5','PO3','PO4','PO6','FT7','FT8',
    'TP7','TP8','PO7','PO8','FT9','FT10','TPP9h','TPP10h','PO9','PO10','P9','P10','AFF1','AFz','AFF2','FFC5h','FFC3h',
    'FFC4h','FFC6h','FCC5h','FCC3h','FCC4h','FCC6h','CCP5h','CCP3h','CCP4h','CCP6h','CPP5h','CPP3h','CPP4h','CPP6h',
    'PPO1','PPO2','I1','Iz','I2','AFp3h','AFp4h','AFF5h','AFF6h','FFT7h','FFC1h','FFC2h','FFT8h','FTT9h','FTT7h','FCC1h',
    'FCC2h','FTT8h','FTT10h','TTP7h','CCP1h','CCP2h','TTP8h','TPP7h','CPP1h','CPP2h','TPP8h','PPO9h','PPO5h','PPO6h',
    'PPO10h','POO9h','POO3h','POO4h','POO10h','OI1h','OI2h']

# F C P O LT RT


schema = {
    'Fp1': 'F', 'Fpz': 'F', 'Fp2': 'F', 'F7': 'F', 'F3': 'F', 'Fz': 'F', 'F4': 'F',
    'F8': 'F', 'FC5': 'LT', 'FC1': 'C', 'FC2': 'C', 'FC6': 'RT', 'M1': 'LT',
    'T7': 'LT', 'C3': 'C', 'Cz': 'C', 'C4': 'C', 'T8': 'RT', 'M2': 'RT',
    'CP5': 'LT', 'CP1': 'P', 'CP2': 'P', 'CP6': 'RT', 'P7': 'P', 'P3': 'P',
    'Pz': 'P', 'P4': 'P', 'P8': 'P', 'POz': 'P', 'O1': 'O', 'Oz': 'O',
    'O2': 'O', 'AF7': 'F', 'AF3': 'F', 'AF4': 'F', 'AF8': 'F', 'F5': 'F',
    'F1': 'F', 'F2': 'F', 'F6': 'F', 'FC3': 'C', 'FCz': 'C', 'FC4': 'C',
    'C5': 'LT', 'C1': 'C', 'C2': 'C', 'C6': 'RT', 'CP3': 'P', 'CPz': 'P',
    'CP4': 'P', 'P5': 'P', 'P1': 'P', 'P2': 'P', 'P6': 'P', 'PO5': 'P',
    'PO3': 'P', 'PO4': 'P', 'PO6': 'P', 'FT7': 'LT', 'FT8': 'RT', 'TP7': 'LT',
    'TP8': 'RT', 'PO7': 'P', 'PO8': 'P', 'FT9': 'LT', 'FT10': 'RT', 'TPP9h': 'LT',
    'TPP10h': 'RT', 'PO9': 'O', 'PO10': 'O', 'P9': 'P', 'P10': 'P', 'AFF1': 'F',
    'AFz': 'F', 'AFF2': 'F', 'FFC5h': 'C', 'FFC3h': 'C', 'FFC4h': 'C',
    'FFC6h': 'RT', 'FCC5h': 'LT', 'FCC3h': 'C', 'FCC4h': 'C', 'FCC6h': 'RT',
    'CCP5h': 'LT', 'CCP3h': 'P', 'CCP4h': 'P', 'CCP6h': 'RT', 'CPP5h': 'P',
    'CPP3h': 'P', 'CPP4h': 'P', 'CPP6h': 'P', 'PPO1': 'P', 'PPO2': 'P',
    'I1': 'O', 'Iz': 'O', 'I2': 'O', 'AFp3h': 'F', 'AFp4h': 'F', 'AFF5h': 'F',
    'AFF6h': 'F', 'FFT7h': 'LT', 'FFC1h': 'C', 'FFC2h': 'C', 'FFT8h': 'RT',
    'FTT9h': 'LT', 'FTT7h': 'LT', 'FCC1h': 'C', 'FCC2h': 'C', 'FTT8h': 'RT',
    'FTT10h': 'RT', 'TTP7h': 'LT', 'CCP1h': 'P', 'CCP2h': 'P', 'TTP8h': 'RT',
    'TPP7h': 'LT', 'CPP1h': 'P', 'CPP2h': 'P', 'TPP8h': 'RT', 'PPO9h': 'P', 
    'PPO5h': 'P', 'PPO6h': 'P', 'PPO10h': 'P', 'POO9h': 'O', 'POO3h': 'P',
    'POO4h': 'P', 'POO10h': 'O', 'OI1h': 'O', 'OI2h': 'O'
}

region_indices = get_region_indices(schema, electrode_list)
print(region_indices)