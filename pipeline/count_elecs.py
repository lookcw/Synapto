from regions import regions

for region in regions:
    print('=================='+region+"=======================")
    for reg in regions[region]:
        print(reg + ":"+ str(len(regions[region][reg])))

