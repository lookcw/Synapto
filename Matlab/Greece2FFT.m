Fs = 250;

% HC ---------------------
cd HC_targ
dirs = dir(fullfile('.','*.csv'));
x = 1; HCE = []; HCTfft = [];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    HCT = importdata(filename);
    HCT = HCT(:,2:end);
    [row,col] = size(HCT);
    for k = 1:col
        HCE = HCT(:,k);
        N = length(HCE);
        xdft = fft(HCE);
        xdft = xdft(1:N/2+1);
        psdx = (1/(Fs*N)) * abs(xdft).^2;
        psdx(2:end-1) = 2*psdx(2:end-1);
        freq = 0:Fs/N:Fs/2;
        HCTfft(:,k) = psdx;
    end
    cd ..
    cd HC_targ_fft
    dlmwrite(strcat('GHTfft',num2str(x),'.csv'),HCTfft);
    cd ..
    cd HC_targ
    x = x+1;
end
cd ..

cd HC_stan
dirs = dir(fullfile('.','*.csv'));
x = 1; HCE = []; HCSfft = [];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    HCS = importdata(filename);
    HCS = HCS(:,2:end);
    [row,col] = size(HCS);
    for k = 1:col
        HCE = HCS(:,k);
        N = length(HCE);
        xdft = fft(HCE);
        xdft = xdft(1:N/2+1);
        psdx = (1/(Fs*N)) * abs(xdft).^2;
        psdx(2:end-1) = 2*psdx(2:end-1);
        freq = 0:Fs/N:Fs/2;
        HCSfft(:,k) = psdx;
    end
    cd ..
    cd HC_stan_fft
    dlmwrite(strcat('GHSfft',num2str(x),'.csv'),HCSfft);
    cd ..
    cd HC_stan
    x = x+1;
end
cd ..




% AD ---------------------
cd AD_targ
dirs = dir(fullfile('.','*.csv'));
x = 1; ADE = []; ADTfft = [];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    ADT = importdata(filename);
    ADT = ADT(:,2:end);
    [row,col] = size(ADT);
    for k = 1:col
        ADE = ADT(:,k);
        N = length(ADE);
        xdft = fft(ADE);
        xdft = xdft(1:N/2+1);
        psdx = (1/(Fs*N)) * abs(xdft).^2;
        psdx(2:end-1) = 2*psdx(2:end-1);
        freq = 0:Fs/N:Fs/2;
        ADTfft(:,k) = psdx;
    end
    cd ..
    cd AD_targ_fft
    dlmwrite(strcat('GATfft',num2str(x),'.csv'),ADTfft);
    cd ..
    cd AD_targ
    x = x+1;
end
cd ..

cd AD_stan
dirs = dir(fullfile('.','*.csv'));
x = 1; ADE = []; ADSfft = [];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    ADS = importdata(filename);
    ADS = ADS(:,2:end);
    [row,col] = size(ADS);
    for k = 1:col
        ADE = ADS(:,k);
        N = length(ADE);
        xdft = fft(ADE);
        xdft = xdft(1:N/2+1);
        psdx = (1/(Fs*N)) * abs(xdft).^2;
        psdx(2:end-1) = 2*psdx(2:end-1);
        freq = 0:Fs/N:Fs/2;
        ADSfft(:,k) = psdx;
    end
    cd ..
    cd AD_stan_fft
    dlmwrite(strcat('GASfft',num2str(x),'.csv'),ADSfft);
    cd ..
    cd AD_stan
    x = x+1;
end
cd ..




% MCI --------------------
cd MCI_targ
dirs = dir(fullfile('.','*.csv'));
x = 1; MCIE = []; MCITfft = [];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    MCIT = importdata(filename);
    MCIT = MCIT(:,2:end);
    [row,col] = size(MCIT);
    for k = 1:col
        MCIE = MCIT(:,k);
        N = length(MCIE);
        xdft = fft(MCIE);
        xdft = xdft(1:N/2+1);
        psdx = (1/(Fs*N)) * abs(xdft).^2;
        psdx(2:end-1) = 2*psdx(2:end-1);
        freq = 0:Fs/N:Fs/2;
        MCITfft(:,k) = psdx;
    end
    cd ..
    cd MCI_targ_fft
    dlmwrite(strcat('GMTfft',num2str(x),'.csv'),MCITfft);
    cd ..
    cd MCI_targ
    x = x+1;
end
cd ..

cd MCI_stan
dirs = dir(fullfile('.','*.csv'));
x = 1; MCIE = []; MCISfft = [];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    MCIS = importdata(filename);
    MCIS = MCIS(:,2:end);
    [row,col] = size(MCIS);
    for k = 1:col
        MCIE = MCIS(:,k);
        N = length(MCIE);
        xdft = fft(MCIE);
        xdft = xdft(1:N/2+1);
        psdx = (1/(Fs*N)) * abs(xdft).^2;
        psdx(2:end-1) = 2*psdx(2:end-1);
        freq = 0:Fs/N:Fs/2;
        MCISfft(:,k) = psdx;
    end
    cd ..
    cd MCI_stan_fft
    dlmwrite(strcat('GMSfft',num2str(x),'.csv'),MCISfft);
    cd ..
    cd MCI_stan
    x = x+1;
end
cd ..