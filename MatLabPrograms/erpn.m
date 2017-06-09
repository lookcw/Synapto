% Inputs: initial time, final time, 'max' or 'min'. Outputs a row
% vector containing a max/min amplitude value per electrode within time
% range.

function val = erpn(filename,ti,tf,maxmin)

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

poststim = find(t>=0);
base1 = mean(E1(1:poststim(1)));
base2 = mean(E2(1:poststim(1)));
base3 = mean(E3(1:poststim(1)));
base4 = mean(E4(1:poststim(1)));
base5 = mean(E5(1:poststim(1)));
base6 = mean(E6(1:poststim(1)));
base7 = mean(E7(1:poststim(1)));

E = [E1-base1;E2-base2;E3-base3;E4-base4;E5-base5;E6-base6;E7-base7];
numrows = size(E,1);

val = zeros(1,numrows);
for k = 1:numrows
    n = E(k,:);
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