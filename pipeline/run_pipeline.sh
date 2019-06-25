is=(1 1 1)
ts=(16000 10666 8000)
es=(10 15 20)
features=('FSL' 'Wavelet' 'Pearson' 'DomFreq')

for feature in ${features[@]}; do
    for i in ${!is[@]}; do
    echo  "python pipeline.py -d Brazil -f $feature -i ${is[$i]} -t ${ts[$i]} -e ${es[$i]}"
        python pipeline.py -d "Brazil" -f $feature -i ${is[$i]} -t ${ts[$i]} -e ${es[$i]}
    done
done