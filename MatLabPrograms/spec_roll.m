% cutoff is percentage of power to the left of desired frequency
% (usually ranges from 80-90)

function SR = spec_roll(filename,cutoff)

if exist('data','var')~=1
    data = importdata(filename);
    data = data(:,2:8);
    %data = data(1:4000,2:8);
end

rawdata = data';
E1 = rawdata(1,:);
E2 = rawdata(2,:);
E3 = rawdata(3,:);
E4 = rawdata(4,:);
E5 = rawdata(5,:);
E6 = rawdata(6,:);
E7 = rawdata(7,:);
%E8 = rawdata(8,:);
E = [E1;E2;E3;E4;E5;E6;E7];
siz = size(E);

Fs = 250;
N = siz(2);

for n = 1:siz(1)
xdft = fft(E(n,:));
xdft = xdft(1:N/2+1);
psdx = (1/(Fs*N)) * abs(xdft).^2;
psdx(2:end-1) = 2*psdx(2:end-1);
freq = 0:Fs/N:Fs/2;
fftval = 10*log10(psdx);

target = cutoff/100*sum(fftval);
bool = false;
for k = 1:length(fftval)
    tot = sum(fftval(1:k));
    if tot > target && ~bool
        bool = true;
        index = k;
end
end
SR = index/length(fftval)*Fs/2
end
