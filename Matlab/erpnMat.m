% Inputs: initial time, final time, 'max' or 'min'. Outputs a row
% vector containing a max/min amplitude value per electrode within time
% range.

function valN = erpnMat(mat,ti,tf,maxmin,EpLen)
valN = [];
L = size(mat,1)/EpLen;
for m = 1:L
    %Create data matrix
    E = mat((m-1)*EpLen+1:m*EpLen,:);
    [row,col] = size(E);
    t = linspace(-200,1000,row);
    
    %Create baseline removal number
    poststim = find(t>=0);
    base = zeros(col,1);
    for k = 1:col
        base(k) = mean(E(1:poststim(1),k));
    end
    
    %Remove baseline
    for k = 1:col
        E(:,k) = E(:,k)-base(k);
    end
    
    val = zeros(1,col);
    for k = 1:col
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
    valN = [valN,val];
end
end