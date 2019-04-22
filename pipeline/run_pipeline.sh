is=( 1 2 4 )
ts=(200000 100000 50000)
features=('FSL' 'Wavelet' 'Pearson')

for feature in ${features[@]}; do
    for i in ${!is[@]}; do
    echo  "python pipeline.py -d Brazil -f $feature -i ${is[$i]} -t ${ts[$i]}"
        python pipeline.py -d "Brazil" -f $feature -i ${is[$i]} -t ${ts[$i]}
    done
done