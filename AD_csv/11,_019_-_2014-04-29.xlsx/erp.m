% Inputs: initial time, final time, 'max' or 'min'. Optional 4th input for 
% sampling frequency, otherwise Fs has a default value of 125. Outputs a
% vector containing a max/min amplitude value per electrode within time
% range.

function val = erp(ti,tf,maxmin,Fs)

if exist('csv0','var')~=1
    csv0 = importdata('11,_024_-_2014-04-29.xlsx.csv.0');
    csv0 = csv0(:,1:8);
end
  
rawdata = csv0';
E1 = rawdata(2,:);
E2 = rawdata(3,:);
E3 = rawdata(4,:);
E4 = rawdata(5,:);
E5 = rawdata(6,:);
E6 = rawdata(7,:);
E7 = rawdata(8,:);

figure
S = length(E1);
avgVal1 = zeros(S,1);
for n=10:S
    avgVal1(n-5) = (E1(n)+E1(n-1)+E1(n-2)+E1(n-3)+E1(n-4)+E1(n-5)+E1(n-6)+E1(n-7)+E1(n-8)+E1(n-9))/10;
end
plot(rawdata(1,:),avgVal1); hold on
plot(rawdata(1,:),E1)

E = [E1;E2;E3;E4;E5;E6;E7];
[numrows,numcols] = size(E);

if nargin < 4
    Fs = 125;
end

val = zeros(numrows,1);

for k = 1:numrows
    n = E(k,:);
    t = [-0.24:1/Fs:((numcols-1)/Fs)-0.24];
    figure;
    plot(t,n);
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