% Inputs: initial time, final time, wave type ('min' or 'max')

function latency = lat(filename,ti,tf,maxormin)

if exist('tandDat','var')~=1
    tandDat = importdata(filename);
end

[~,col] = size(tandDat);
for k = 2:col
    E(:,k-1) = tandDat(:,k);
end
t = tandDat(:,1);

poststim = find(t>=0);
val = zeros(1,col-1);
valInd = zeros(1,col-1);
latency = zeros(1,col-1);

for k = 1:col-1
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
end