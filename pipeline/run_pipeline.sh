is=(1 1)
ts=(160000 80000)
es=(1 2)
features=('FSL' 'Wavelet' 'Pearson' 'DomFreq')

for feature in ${features[@]}; do
    for i in ${!is[@]}; do
    echo  "python pipeline.py -d Brazil -f $feature -i ${is[$i]} -t ${ts[$i]} -e ${es[$i]}"
        python pipeline.py -d "Brazil" -f $feature -i ${is[$i]} -t ${ts[$i]} -e ${es[$i]}
    done
done