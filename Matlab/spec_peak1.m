function SP = spec_peak1(filename,EpochLength)

dat = importdata(filename);
for k = 1:size(dat,2)/21
    data(:,:,k) = dat(:,(k-1)*21+1:k*21); % (data)row x (electrode)column x (patient)plane
    data(:,:,k) = eegfilt(data(:,:,k)',250,4,0)';
end

[row,col,pla] = size(data);
SP = [];
Fs = 250;
for k = 1:pla
    ep = intoEpochs(data(:,:,k),EpochLength,Fs,660); % (data)row x (electrode)column x (epoch)plane
    SP2 = [];
    for v = 1:size(ep,3)
        
        E = ep(:,:,v);
        
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
        SP2 = [SP2,SP1];
    end
    SP = [SP;SP2];
end