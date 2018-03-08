% Input: Data Matrix, Epoch Length, Sampling Frequency, Length of Interest
% Columns of data matrix should be Electrodes
% Output: one variable containing n rows x m columns x p planes where
% n = Fs x Epoch Length, m = # Electrodes, p = # Epochs

function Ep = intoEpochs(dataMat,EpochLength,Fs,Length_sec)

if Length_sec > size(dataMat,1)/Fs
    disp('Input length is too long for the data matrix provided.')
    return
end

Ep = [];
[row,col] = size(dataMat);
rowS = Fs*Length_sec;
newDat = zeros(Fs*EpochLength,col);
for v = 1:floor(rowS/(Fs*EpochLength))
    for k = 1:col
        newDat(1:Fs*EpochLength,k) = dataMat((v-1)*Fs*EpochLength+1:v*Fs*EpochLength,k);
    end
    Ep(:,:,v) = newDat;
end

