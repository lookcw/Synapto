function SP = spec_peak(filename,EpochLength)
%data = toMat(filename);
%data = data(:,2:22);

% Using F50
data = importdata(filename)';
data = data(:,2:22);

% Using BD_Fil
%data = importdata(filename);
%data = data(2:end,3:23);
%data = data';

SP = [];
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
    SP1 = [];
    for n = 1:size(E,2)
        xdft = fft(E(:,n));
        xdft = xdft(1:N/2+1);
        psdx = (1/(Fs*N)) * abs(xdft).^2;
        psdx(2:end-1) = 2*psdx(2:end-1);
        freq = 0:Fs/N:Fs/2;
        fftval = psdx; %10*log10(psdx);
        x = linspace(0,Fs/2,length(fftval));
        
        deltaRange = find(x>0.1 & x<4);
        maxdeltaAmp = max(fftval(deltaRange));
        for k = deltaRange
            if fftval(k) == maxdeltaAmp
                deltaIndex = x(k);
            end
        end
        
        thetaRange = find(x>4 & x<8);
        maxthetaAmp = max(fftval(thetaRange));
        for k = thetaRange
            if fftval(k) == maxthetaAmp
                thetaIndex = x(k);
            end
        end
        
        alphaRange = find(x>8 & x<12);
        maxalphaAmp = max(fftval(alphaRange));
        for k = alphaRange
            if fftval(k) == maxalphaAmp
                alphaIndex = x(k);
            end
        end
        
        betaRange = find(x>12 & x<30);
        maxbetaAmp = max(fftval(betaRange));
        for k = betaRange
            if fftval(k) == maxbetaAmp
                betaIndex = x(k);
            end
        end
        
        gammaRange = find(x>30 & x<50);
        maxgammaAmp = max(fftval(gammaRange));
        for k = gammaRange
            if fftval(k) == maxgammaAmp
                gammaIndex = x(k);
            end
        end
        
        SP1 = [SP1,deltaIndex,thetaIndex,alphaIndex,betaIndex,gammaIndex];
    end
    SP = [SP,SP1];
end