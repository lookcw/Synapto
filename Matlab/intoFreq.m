% Input: 3D matrix n x m x p
% n = patients, m = epochs, p = zones
% Output: 2D matrix n x m
% n = patients, m = zones

function Freq = intoFreq(dataMat)

Freq = [];
for z = 1:size(dataMat,3)
    Fre = [];
    for p = 1:size(dataMat,1)
        pat = dataMat(p,:,z);
        num0 = length(find(pat==0));
        Fr = num0/length(pat);
        Fre = [Fre;Fr];
    end
    Freq = [Freq,Fre];
end
