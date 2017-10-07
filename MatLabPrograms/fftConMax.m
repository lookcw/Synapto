% Input a file name, length of epoch (in seconds), and the two electrodes
% you want to convolve (column number). The output is a descriptor vector 
% of the maximum of the convolution between the ffts of these two column 
% vectors for each epoch.

function conMax = fftConMax(filename,EpochLength,E1,E2)
data = toMat(filename);
data = data(:,2:22);

Fs = 250;
[row,col] = size(data);
rowS = Fs*660; % 11 mins if Fs=250Hz
conMax = zeros(1,floor(rowS/(Fs*EpochLength)));
newDat = zeros(Fs*EpochLength,col);
for v = 1:floor(rowS/(Fs*EpochLength))
    for l = 1:col
        newDat(1:Fs*EpochLength,l) = data((v-1)*Fs*EpochLength+1:v*Fs*EpochLength,l);
    end
    E = newDat;
    
    N = size(E,1);
    
    xdft1 = fft(E(:,E1));
    xdft1 = xdft1(1:N/2+1);
    psdx1 = (1/(Fs*N)) * abs(xdft1).^2;
    psdx1(2:end-1) = 2*psdx1(2:end-1);
    freq1 = 0:Fs/N:Fs/2;
    fftval1 = psdx1; %10*log10(psdx1);
    
    xdft2 = fft(E(:,E2));
    xdft2 = xdft2(1:N/2+1);
    psdx2 = (1/(Fs*N)) * abs(xdft2).^2;
    psdx2(2:end-1) = 2*psdx2(2:end-1);
    freq2 = 0:Fs/N:Fs/2;
    fftval2 = psdx2; %10*log10(psdx2);
    
    conMax(v) = max(conv(fftval1,fftval2));
end