% Inputs: initial time, final time, 'max' or 'min'. Outputs a row
% vector containing a max/min amplitude value per electrode within time
% range.

function val = erpn(filename,ti,tf,maxmin)

if exist('tandDat','var')~=1
    tandDat = importdata(filename);
end

%Create data matrix (exclude time)
col = size(tandDat,2);
for k = 2:col
    E(:,k-1) = tandDat(:,k);
end
t = tandDat(:,1);

%Create baseline removal number
poststim = find(t>=0);
base = zeros(col-1,1);
for k = 1:col-1
    base(k) = mean(E(1:poststim(1),k));
end

%Remove baseline
for k = 1:col-1
    E(:,k) = E(:,k)-base(k);
end

val = zeros(1,col-1);
for k = 1:col-1
    n = E(:,k);
    ERPrange = find(t>=ti & t<=tf);
    
    if strcmpi(maxmin,'max')
        amplitude = max(n(ERPrange));
    end
    
    if strcmpi(maxmin,'min')
        amplitude = min(n(ERPrange));
    end
    
    val(k) = amplitude;
end
end