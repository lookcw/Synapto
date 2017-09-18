function SE = spec_ent(filename,EpochLength)
data = toMat(filename);
data = data(:,2:22);

SE = [];
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
    SE1 = [];
    for n = 1:size(E,2)
        xdft = fft(E(:,n));
        xdft = xdft(1:N/2+1);
        psdx = (1/(Fs*N)) * abs(xdft).^2;
        psdx(2:end-1) = 2*psdx(2:end-1);
        freq = 0:Fs/N:Fs/2;
        fftval = psdx; %10*log10(psdx);
        
        bandindex = find(freq>0.5 & freq<30);
        fftband = fftval(bandindex);
        
        bins = Fs/2;
        psd = (abs(fftband).^2)/bins;
        psdnorm = psd/sum(psd);
        
        for k = 1:length(psdnorm)
            psdnorm(k) = psdnorm(k)*log(psdnorm(k));
        end
        
        a = -sum(psdnorm);
        SE1 = [SE1,a];
    end
    SE = [SE,SE1];
end