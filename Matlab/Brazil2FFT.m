% Must start in a folder containing 'HC_BD_Fil', 'AD_BD_Fil', 'HC_fft', 'AD_fft'

Fs = 250;

% HC ---------------------
cd HC_BD_Fil
dirs = dir(fullfile('.','*.txt'));
x = 1; HCE = []; HCfft = [];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    HC = importdata(filename);
    HC = HC(2:end,3:23);
    [row,col] = size(HC);
    for k = 1:col
        HCE = HC(1:Fs*660,k);
        N = length(HCE);
        xdft = fft(HCE);
        xdft = xdft(1:N/2+1);
        psdx = (1/(Fs*N)) * abs(xdft).^2;
        psdx(2:end-1) = 2*psdx(2:end-1);
        freq = 0:Fs/N:Fs/2;
        HCfft(:,k) = psdx;
    end
    cd ..
    cd HC_fft
    dlmwrite(strcat('BHfft',num2str(x),'.csv'),HCfft);
    cd ..
    cd HC_BD_Fil
    x = x+1;
end
cd ..


% AD ---------------------
cd AD_BD_Fil
dirs = dir(fullfile('.','*.txt'));
x = 1; ADE = []; ADfft = [];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    AD = importdata(filename);
    AD = AD(2:end,3:23);
    [row,col] = size(AD);
    for k = 1:col
        ADE = AD(1:Fs*660,k);
        N = length(ADE);
        xdft = fft(ADE);
        xdft = xdft(1:N/2+1);
        psdx = (1/(Fs*N)) * abs(xdft).^2;
        psdx(2:end-1) = 2*psdx(2:end-1);
        freq = 0:Fs/N:Fs/2;
        ADfft(:,k) = psdx;
    end
    cd ..
    cd AD_fft
    dlmwrite(strcat('BAfft',num2str(x),'.csv'),ADfft);
    cd ..
    cd AD_BD_Fil
    x = x+1;
end
cd ..

