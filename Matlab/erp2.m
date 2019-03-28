% Inputs: initial time, final time, 'max' or 'min'. Outputs a row
% vector containing a max/min amplitude value per electrode within time
% range.

function val = erp2(filename,ti,tf,maxmin)

if exist('csv0','var')~=1
    csv0 = importdata(filename);
    csv0 = csv0(:,1:8);
end

rawdata = csv0';
t  = rawdata(1,:);
E1 = rawdata(2,:);
E2 = rawdata(3,:);
E3 = rawdata(4,:);
E4 = rawdata(5,:);
E5 = rawdata(6,:);
E6 = rawdata(7,:);
E7 = rawdata(8,:);

E = [E1;E2;E3;E4;E5;E6;E7];
numrows = size(E,1);

base = zeros(1,numrows);
val = zeros(1,numrows);

for k = 1:numrows
    n = E(k,:);
    ERPrange = find(t>=ti & t<=tf);
    
    base(k) = n(t==0);
    
    if strcmpi(maxmin,'max')
        amplitude = max(n(ERPrange));
    end

    if strcmpi(maxmin,'min')
        amplitude = min(n(ERPrange));
    end

    val(k) = amplitude-base(k);
end

end