% Input: one variable containing n rows x m columns x p planes where...
% n = Fs x Epoch Length, m = # Electrodes, p = # Epochs
% and the threshold value (from min StDev of electrode)
% Output: one 3D matrix variable n x m x p where...
% n = Fs x Epoch Length, m = # Electrodes, p = # Epochs
% *this output will include columns of NaN representing rejected data

function AR = AAR_StDev(elecData,Threshold)

AR = elecData;
[row,col,pla] = size(elecData); % row = #datapoints, col = #electrodes, pla = #epochs
for k = 1:pla
    for v = 1:col
        SDM(k,v) = std(elecData(:,v,k)); % (82 row)epochs x (21 column)electrodes (StDev)
    end
end

for k = 1:col
    Thresh = min(SDM(:,k)) + Threshold;
    for v = 1:pla
        if SDM(v,k) > Thresh
            SDM(v,k) = NaN;
        end
    end
end

for k = 1:pla
    for v = 1:col
        if isnan(SDM(k,v))
            AR(:,v,k) = NaN;
        end
    end
end
