% Inputs: initial time, final time, wave type. Wave type will only accept
% 'N200' 'Slow' and 'P3b' (not case sensitive). Remember, don't use slow
% wave for standard and distractor tones. The other two could be used for
% all three since there appears to be some difference between AD and HC in
% the frame these waves exist in.

function latency = lat(ti,tf,wave)

if exist('csv0','var')~=1
    csv0 = importdata('11,_025_-_2014-04-29.xlsx.csv.1');
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

E = [E1;E2;E3;E4;E5;E6;E7];
numrows = size(E,1);

poststim = find(t>=0);
val = zeros(1,numrows);
valInd = zeros(1,numrows);
latency = zeros(1,numrows);

for k = 1:numrows
    n = E(k,:);
    index = find(t>=ti & t<=tf);
    
    if strcmpi(wave,'P3b')
        amplitude = max(n(index));
    end

    if strcmpi(wave,'N200') || strcmpi(wave,'Slow')
        amplitude = min(n(index));
    end
    
    val(k) = amplitude;
    valInd(k) = find(n==val(k))-poststim(1);
    latency(k) = valInd(k)*(t(2)-t(1));
end
end