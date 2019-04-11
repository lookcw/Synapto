% Input a file name, length of epoch (in seconds), and the two electrodes
% you want to convolve (column number). The output is a descriptor vector
% of the maximum of the convolution between the ffts of these two column
% vectors for each epoch.

function conMax = fftConMax(filename,EpochLength)
%data = toMat(filename);
%data = data(:,2:22);

% Using F50
data = importdata(filename)';
data = data(:,2:22);

% Using BD_Fil
%data = importdata(filename);
%data = data(2:end,3:23);
%data = data';

conMax = [];
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
    
    for k = 1:21
        for q = 1:21
            
            xdft1 = fft(E(:,k));
            xdft1 = xdft1(1:N/2+1);
            psdx1 = (1/(Fs*N)) * abs(xdft1).^2;
            psdx1(2:end-1) = 2*psdx1(2:end-1);
            freq1 = 0:Fs/N:Fs/2;
            fftval1 = psdx1(1:280); %10*log10(psdx1);
            
            xdft2 = fft(E(:,q));
            xdft2 = xdft2(1:N/2+1);
            psdx2 = (1/(Fs*N)) * abs(xdft2).^2;
            psdx2(2:end-1) = 2*psdx2(2:end-1);
            freq2 = 0:Fs/N:Fs/2;
            fftval2 = psdx2(1:280); %10*log10(psdx2);
            
            conMaxk(q) = max(conv(fftval1,fftval2));
        end
        conMax = [conMax,conMaxk];
    end
end