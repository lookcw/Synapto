% Input: 
% filename = a file with the following format...
% 24 x n matrix where n >= Fs*660 (longer than 11 mins if Fs=250Hz) and the
% 2nd-22nd rows are EEG electrode data (of a single patient)
% EpochLength = length of a single epoch in seconds

% Output:
% fd = 1 x n row vector of averaged and artifact-free Higuchi Fractal 
% Dimension values

function fd = HFDwAAR(filename,EpochLength)
data = importdata(filename)';
data = data(:,2:22);

fd = [];
Fs = 250; % Sampling Frequency
[row,col] = size(data);
rowS = Fs*660; % 11 mins if Fs=250Hz
newDat = zeros(Fs*EpochLength,col);
SDM = zeros(1,floor(rowS/(Fs*EpochLength))*col);
for v = 1:floor(rowS/(Fs*EpochLength)) % Cycle through epochs
    for l = 1:col
        newDat(1:Fs*EpochLength,l) = data((v-1)*Fs*EpochLength+1:v*Fs*EpochLength,l); % All electrodes in one epoch
    end
    E = newDat;
    
    N = size(E,1);
    fd1 = zeros(1,size(E,2));
    for n = 1:size(E,2)
        % FFT
        xdft = fft(E(:,n));
        xdft = xdft(1:N/2+1);
        psdx = (1/(Fs*N)) * abs(xdft).^2;
        psdx(2:end-1) = 2*psdx(2:end-1);
        freq = 0:Fs/N:Fs/2;
        x = psdx;
        %x = E(:,n); % Used for time domain instead of frequency
        
        % in:  x   data
        % out: fd  fractal dimension estimate (using Higuchi method)
        
        kmax = 60; % HFD parameter
        M = length(x); % Length of data/signal
        Lmk = zeros(kmax,kmax);
        
        % Mean length of curve
        for k = 1:kmax
            for m = 1:k
                Lmki = 0;
                for i = 1:fix((M-m)/k)
                    Lmki = Lmki+abs(x(m+i*k)-x(m+(i-1)*k));
                end
                Ng = (M-1)/(fix((M-m)/k)*k);
                Lmk(m,k) = (Lmki*Ng)/k;
            end
        end
        
        Lk = zeros(1,kmax);
        for k = 1:kmax
            Lk(1,k) = sum(Lmk(1:k,k))/k;
        end
        
        % Logarithmic values for slope calculation (FD estimate)
        lnLk = log(Lk);
        lnk =  log(1./(1:kmax));
        
        % Slope
        b = polyfit(lnk,lnLk,1);
        a = b(1);
        fd1(n) = a;
        
    end
    
    % Set up standard deviation vector to prepare for artifact epoch removal
    for k = 1:col
        SDM(k+(v-1)*col) = std(E(:,k));
    end
    
    fd = [fd,fd1]; % Output vector before artifact removal
    
end


% ARTIFACT REMOVAL (Standard Deviation Method)
% ** Comments based on EpochLength = 8 and S = 5 **
for k = 1:col
    SDME(:,k) = SDM(k:col:length(SDM)); % (82 row)epochs x (21 column)electrodes (StDev)
    fdME(:,k) = fd(k:col:length(fd));   % (82 row)epochs x (21 column)electrodes (HigVal)
end
S = 5; % Number of grouped epochs
SDMES = zeros(S,floor(size(SDME,1)/S),col);
fdMES = zeros(S,floor(size(fdME,1)/S),col);
for p = 1:col
    y = 1;
    for k = 1:S:size(SDME,1)-S
        SDMES(:,y,p) = SDME(k:k+S-1,p); % (5 row x 16 column)epochs x (21 plane)electrodes (StDev)
        fdMES(:,y,p) = fdME(k:k+S-1,p); % (5 row x 16 column)epochs x (21 plane)electrodes (HigVal)
        y = y+1;
    end
end

for u = 1:size(SDMES,3)
    Thresh = min(SDME(:,u)) + 7; % Threshold used to reject epoch with artifact(s)
    for p = 1:size(SDMES,2)
        SDEp2Av = [];
        y = 1;
        for k = 1:size(SDMES,1)
            if SDMES(k,p,u) < Thresh % Finds epochs without artifacts
                SDEp2Av(y) = SDMES(k,p,u); % (1 row x 0-5 column)epochs (StDev)
                fdEp2Av(y) = fdMES(k,p,u); % (1 row x 0-5 column)epochs (HigVal)
                y = y+1;
            end
        end
        if length(SDEp2Av) < 1 % If all 5 epochs fail, use result from the best one
            SDEp2Av = min(SDMES(:,p,u));                  % (1 row x 1 column)epoch (least varying artifact) (StDev)
            fdEp2Av = fdMES(SDMES(:,p,u) == SDEp2Av,p,u); % (1 row x 1 column)epoch (least varying artifact) (HigVal)
        end
        % Average the kept values to keep consistency of length
        SDAvEp(p+size(SDMES,2)*(u-1)) = mean(SDEp2Av); % (1 row x 16x21 column)epochs (mean StDev)
        fdAvEp(p+size(SDMES,2)*(u-1)) = mean(fdEp2Av); % (1 row x 16x21 column)epochs (mean HigVal)
    end
end

fd = fdAvEp; % Output vector after artifact removal

end
