import csv

feature = 'Hig'
HC_filename = f'{feature}_HC.csv'
AD_filename = f'{feature}_AD.csv'
with open(HC_filename, 'r') as r_file:
    HC_vals = list(map(float,r_file.readline().split(',')))
with open(AD_filename, 'r') as r_file:
    AD_vals = list(map(float,r_file.readline().split(',')))

diff=[]
zip_object = zip(HC_vals, AD_vals)
for HC_val, AD_val in zip_object:
    diff.append(AD_val-HC_val)

with open(f'{feature}_diff.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile)
     wr.writerow(diff)

