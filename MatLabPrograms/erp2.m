% Inputs: initial time, final time, 'max' or 'min'. Outputs a row
% vector containing a max/min amplitude value per electrode within time
% range.

function val = erp(ti,tf,maxmin)

if exist('csv0','var')~=1
    csv0 = importdata('11,_024_-_2014-04-29.xlsx.csv.0');
    csv0 = csv0(:,1:8);
end

rawdata = csv0';
t = rawdata(1,:);
E1 = rawdata(2,:);
E2 = rawdata(3,:);
E3 = rawdata(4,:);
E4 = rawdata(5,:);
E5 = rawdata(6,:);
E6 = rawdata(7,:);
E7 = rawdata(8,:);

poststim = find(t>=0);
S = length(E1);
avgVal1 = zeros(S,1);
for n=10:S
    avgVal1(n-5) = (E1(n)+E1(n-1)+E1(n-2)+E1(n-3)+E1(n-4)+E1(n-5)+E1(n-6)+E1(n-7)+E1(n-8)+E1(n-9))/10;
end
base1 = mean(avgVal1(5:poststim(1)));

avgVal2 = zeros(S,1);
for n=10:S
    avgVal2(n-5) = (E2(n)+E2(n-1)+E2(n-2)+E2(n-3)+E2(n-4)+E2(n-5)+E2(n-6)+E2(n-7)+E2(n-8)+E2(n-9))/10;
end
base2 = mean(avgVal2(5:poststim(1)));

avgVal3 = zeros(S,1);
for n=10:S
    avgVal2(n-5) = (E3(n)+E3(n-1)+E3(n-2)+E3(n-3)+E3(n-4)+E3(n-5)+E3(n-6)+E3(n-7)+E3(n-8)+E3(n-9))/10;
end
base3 = mean(avgVal3(5:poststim(1)));

avgVal4 = zeros(S,1);
for n=10:S
    avgVal2(n-5) = (E4(n)+E4(n-1)+E4(n-2)+E4(n-3)+E4(n-4)+E4(n-5)+E4(n-6)+E4(n-7)+E4(n-8)+E4(n-9))/10;
end
base4 = mean(avgVal4(5:poststim(1)));

avgVal5 = zeros(S,1);
for n=10:S
    avgVal2(n-5) = (E5(n)+E5(n-1)+E5(n-2)+E5(n-3)+E5(n-4)+E5(n-5)+E5(n-6)+E5(n-7)+E5(n-8)+E5(n-9))/10;
end
base5 = mean(avgVal5(5:poststim(1)));

avgVal6 = zeros(S,1);
for n=10:S
    avgVal2(n-5) = (E6(n)+E6(n-1)+E6(n-2)+E6(n-3)+E6(n-4)+E6(n-5)+E6(n-6)+E6(n-7)+E6(n-8)+E6(n-9))/10;
end
base6 = mean(avgVal6(5:poststim(1)));

avgVal7 = zeros(S,1);
for n=10:S
    avgVal2(n-5) = (E7(n)+E7(n-1)+E7(n-2)+E7(n-3)+E7(n-4)+E7(n-5)+E7(n-6)+E7(n-7)+E7(n-8)+E7(n-9))/10;
end
base7 = mean(avgVal7(5:poststim(1)));

E = [E1-base1;E2-base2;E3-base3;E4-base4;E5-base5;E6-base6;E7-base7];
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