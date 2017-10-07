% cutoff is percentage of power to the left of desired frequency
% (usually ranges from 80-90)

function SR = spec_roll(filename,EpochLength,cutoff)
data = toMat(filename);
data = data(:,2:22);

SR = [];
Fs = 250;
[row,col] = size(data);
rowS = Fs*660; % 11 mins if Fs=250Hz
newDat = zeros(Fs*EpochLength,col);
for v = 1:floor(rowS/(Fs*EpochLength))
    for l = 1:col
        newDat(1:Fs*EpochLength,l) = data((v-1)*Fs*EpochLength+1:v*Fs*EpochLength,l);
    end
    E = newDat;
    
    N = size(E,1);
    SR1 = [];
    for n = 1:size(E,2)
        xdft = fft(E(:,n));
        xdft = xdft(1:N/2+1);
        psdx = (1/(Fs*N)) * abs(xdft).^2;
        psdx(2:end-1) = 2*psdx(2:end-1);
        freq = 0:Fs/N:Fs/2;
        fftval = psdx; %10*log10(psdx);
        
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
        SR1 = [SR1,a];
    end
    SR = [SR,SR1];
end