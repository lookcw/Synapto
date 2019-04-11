df = importdata('DomFreq_ins25_lp50_ep8.csv');
DF = df.data;

DF3 = [];
for k = 1:82
    DF3(:,:,k) = DF(:,21*(k-1)+1:21*k);
end

DFm = mean(DF3,3);

dlmwrite('DomFreq_avgOverEpochs.csv',DFm);