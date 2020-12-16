import pandas as pd
from csv import reader, writer


def get_col_name(arr, i, j):
    return arr[0][j]


def get_row_name(arr, i, j):
    return arr[i][0]


feature_name = 'hfd'
p_val_name = feature_name + '_p.csv'
t_val_name = feature_name + '_t.csv'
effect_val_name = feature_name + '_effect.csv'

header = ['Feature', 'p value', 't statistic', 'effect size']

final = []
final.append(header)
with open(p_val_name, 'r') as p_file,\
        open(t_val_name, 'r') as t_file,\
        open(effect_val_name, 'r') as effect_file:
    p_list = list(reader(p_file))
    t_list = list(reader(t_file))
    effect_list = list(reader(effect_file))
    for i in range(1, len(p_list)):
        for j in range(1, len(p_list[0])):
            final.append([get_row_name(p_list, i, j)+' '+get_col_name(p_list, i, j),
                        p_list[i][j],
                        t_list[i][j],
                        effect_list[i][j]])


output_filename = feature_name + '_stats.csv'

with open(output_filename, 'w') as output_file:
    csv_writer = writer(output_file)
    csv_writer.writerows(final)
