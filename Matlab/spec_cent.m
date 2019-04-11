function SC = spec_cent(filename,EpochLength)
%data = toMat(filename);
%data = data(:,2:22);

% Using F50
data = importdata(filename)';
data = data(:,2:22);

% Using BD_Fil
%data = importdata(filename);
%data = data(2:end,3:23);
%data = data';

SC = [];
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
    SC1 = [];
    for n = 1:size(E,2)
        xdft = fft(E(:,n));
        xdft = xdft(1:N/2+1);
        psdx = (1/(Fs*N)) * abs(xdft).^2;
        psdx(2:end-1) = 2*psdx(2:end-1);
        freq = 0:Fs/N:Fs/2;
        fftval = psdx; %10*log10(psdx);
        
        for i = 1:length(fftval)
            num(i) = sum(i*fftval(i));
        end
        
        num = sum(num);
        den = sum(fftval);
        
        index = num/den;
        
        a = index/length(fftval)*Fs/2;
        SC1 = [SC1,a];
    end
    for k = 1:col
        SDM(k+(v-1)*col) = std(E(:,k));
    end
    SC = [SC,SC1];
end

for k = 1:col
    SDME(:,k) = SDM(k:col:length(SDM)); % (82 row)epochs x (21 column)electrodes (StDev)
    SCME(:,k) = SC(k:col:length(SC)); % (82 row)epochs x (21 column)electrodes (Val)
end
S = 7; % Number of grouped epochs    **Comments based on S = 5**
SDMES = zeros(S,floor(size(SDME,1)/S),col);
SCMES = zeros(S,floor(size(SCME,1)/S),col);
for p = 1:col
    y = 1;
    for k = 1:S:size(SDME,1)-S
        SDMES(:,y,p) = SDME(k:k+S-1,p); % (5 row x 16 column)epochs x (21 plane)electrodes (StDev)
        SCMES(:,y,p) = SCME(k:k+S-1,p); % (5 row x 16 column)epochs x (21 plane)electrodes (Val)
        y = y+1;
    end
end

for u = 1:size(SDMES,3)
    Thresh(u) = min(SDME(:,u)) + 7; %prctile(SDME(:,u),25)+6; 
    for p = 1:size(SDMES,2)
        SDEp2Av = [];
        y = 1;
        for k = 1:size(SDMES,1)
            if SDMES(k,p,u) < Thresh(u)
                SDEp2Av(y) = SDMES(k,p,u); % (1 row x 0-5 column)epochs (StDev)
                SCEp2Av(y) = SCMES(k,p,u); % (1 row x 0-5 column)epochs (Val)
                y = y+1;
            end
        end
        if length(SDEp2Av) < 1
            SDEp2Av = min(SDMES(:,p,u)); % (1 row x 1 column)epoch (least varying artifact) (StDev)
            SCEp2Av = SCMES(find(SDMES(:,p,u) == SDEp2Av),p,u); % (1 row x 1 column)epoch (least varying artifact) (Val)
        end
        SDAvEp(p+size(SDMES,2)*(u-1)) = mean(SDEp2Av); % (1 row x 16x21 column)epochs (mean StDev)
        SDAvEp(p+size(SDMES,2)*(u-1)) = mean(SCEp2Av); % (1 row x 16x21 column)epochs (mean Val)
    end
end
SC = SDAvEp;
end