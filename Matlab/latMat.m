% Inputs: initial time, final time, wave type ('min' or 'max')

function latencyN = latMat(mat,ti,tf,maxormin,EpLen)

latencyN = [];
L = size(mat,1)/EpLen;
for m = 1:L
    E = mat((m-1)*EpLen+1:m*EpLen,:);
    [row,col] = size(E);
    t = linspace(-200,1000,row);
    
    poststim = find(t>=0);
    val = zeros(1,col);
    valInd = zeros(1,col);
    latency = zeros(1,col);
    
    for k = 1:col
        n = E(:,k);
        index = find(t>=ti & t<=tf);
        
        if strcmpi(maxormin,'max')
            amplitude = max(n(index));
        end
        
        if strcmpi(maxormin,'min')
            amplitude = min(n(index));
        end
        
        val(k) = amplitude;
        Nn = find(n(index)==val(k));
        Nn = Nn(1) + index(1)-1;
        valInd(k) = Nn-poststim(1);
        latency(k) = valInd(k)*(t(2)-t(1));
    end
    latencyN = [latencyN,latency];
end
end