% cutoff is percentage of power to the left of desired frequency
% (usually ranges from 80-90)

%function SR = spec_roll2(filename,cutoff)

%if exist('data','var')~=1
%    data = importdata(filename);
%    data = data(:,2:8);
%end
   data = b; %TestAnalysis;
   data = data(:,2:8);
   cutoff = 85;

Fs = 250;
E = data;
N = size(E,1);

SR = [];
for n = 1:size(E,2)
    xdft = fft(E(:,n));
    xdft = xdft(1:N/2+1);
    psdx = (1/(Fs*N)) * abs(xdft).^2;
    psdx(2:end-1) = 2*psdx(2:end-1);
    freq = 0:Fs/N:Fs/2;
    fftval = psdx;
    %fftval = 10*log10(psdx);
    
    target = cutoff/100*sum(fftval);
    bool = false;
    for k = 1:length(fftval)
        tot = sum(fftval(1:k));
        if tot > target && ~bool
            bool = true;
            index = k;
        end
    end
    a = index/length(fftval)*Fs/2;
    SR = [SR,a];
end
