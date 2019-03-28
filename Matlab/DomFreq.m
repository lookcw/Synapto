% Input: file corresponding to 

function DF = DomFreq(filename,EpochLength,Length_s,Fs)

data = importdata(filename);

DF = [];
[row,col] = size(data);
rowS = Fs*Length_s;
newDat = zeros(Fs*EpochLength,col);
for v = 1:floor(rowS/(Fs*EpochLength)) % Cycle through epochs
    for l = 1:col
        newDat(1:Fs*EpochLength,l) = data((v-1)*Fs*EpochLength+1:v*Fs*EpochLength,l); % All electrodes in one epoch
    end
    E = newDat;
    
    N = size(E,1);
    df = zeros(1,size(E,2));
    for n = 1:size(E,2)
        % FFT
        xdft = fft(E(:,n));
        xdft = xdft(1:N/2+1);
        psdx = (1/(Fs*N)) * abs(xdft).^2;
        psdx(2:end-1) = 2*psdx(2:end-1);
        freq = 0:Fs/N:Fs/2;
        x = psdx;
        xN = x(freq > 1);
        df(1,n) = freq(x == max(xN));
        
    end
    
    DF = [DF,df]; % Output vector
    
end