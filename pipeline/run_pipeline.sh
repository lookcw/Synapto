ds=('HC-DLB' 'DLB-AD')
ts=(160000 80000)
es=(1 2)
features=('FSL' 'Granger' 'Pearson' 'DomFreq')

for feature in ${features[@]}; do
    for d in ${!ds[@]}; do
    	echo  "python3 pipeline.py -d ${ds[$d]} -f $feature -t 23808"
	python3 pipeline.py -d ${ds[$d]} -f $feature -t 23808    
done
done
