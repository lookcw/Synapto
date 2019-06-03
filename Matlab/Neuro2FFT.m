Fs = 125;

% HC ---------------------
cd HC_csv
dirs = dir(fullfile('.','*.xlsx'));
x = 1;
for direc = dirs'
    delimiterIn = ',';
    baseFileName=direc.name
    
    files0 = dir(fullfile(baseFileName,'*csv.0*'));
    HCE = []; HCSfft = [];
    for file = files0'
        filename = file.name;
        stimulusTonefile=fullfile(baseFileName,filename)
        HCS = importdata(stimulusTonefile);
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
        cd HCS_fft
        dlmwrite(strcat('NHSfft',num2str(x),'.csv'),HCSfft);
        cd ..
        cd HC_csv  
    end
    
    files1 = dir(fullfile(baseFileName,'*csv.1*'));
    HCE = []; HCTfft = [];
    for file = files1'
        filename = file.name;
        targetTonefile=fullfile(baseFileName,filename)
        HCT = importdata(targetTonefile);
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
        cd HCT_fft
        dlmwrite(strcat('NHTfft',num2str(x),'.csv'),HCTfft);
        cd ..
        cd HC_csv       
    end
    
    files2 = dir(fullfile(baseFileName,'*csv.2*'));
    HCE = []; HCDfft = [];
    for file = files2'
        filename = file.name;
        distractorTonefile=fullfile(baseFileName,filename)
        HCD = importdata(distractorTonefile);
        HCD = HCD(:,2:end);
        [row,col] = size(HCD);
        for k = 1:col
            HCE = HCD(:,k);
            N = length(HCE);
            xdft = fft(HCE);
            xdft = xdft(1:N/2+1);
            psdx = (1/(Fs*N)) * abs(xdft).^2;
            psdx(2:end-1) = 2*psdx(2:end-1);
            freq = 0:Fs/N:Fs/2;
            HCDfft(:,k) = psdx;
        end
        cd ..
        cd HCD_fft
        dlmwrite(strcat('NHDfft',num2str(x),'.csv'),HCDfft);
        cd ..
        cd HC_csv      
    end
    
    x = x+1;
end
cd ..




% AD ---------------------
cd AD_csv
dirs = dir(fullfile('.','*.xlsx'));
x = 1;
for direc = dirs'
    delimiterIn = ',';
    baseFileName=direc.name
    
    files0 = dir(fullfile(baseFileName,'*csv.0*'));
    ADE = []; ADSfft = [];
    for file = files0'
        filename = file.name;
        stimulusTonefile=fullfile(baseFileName,filename)
        ADS = importdata(stimulusTonefile);
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
        cd ADS_fft
        dlmwrite(strcat('NASfft',num2str(x),'.csv'),ADSfft);
        cd ..
        cd AD_csv 
    end
    
    files1 = dir(fullfile(baseFileName,'*csv.1*'));
    ADE = []; ADTfft = [];
    for file = files1'
        filename = file.name;
        targetTonefile=fullfile(baseFileName,filename)
        ADT = importdata(targetTonefile);
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
        cd ADT_fft
        dlmwrite(strcat('NATfft',num2str(x),'.csv'),ADTfft);
        cd ..
        cd AD_csv      
    end
    
    files2 = dir(fullfile(baseFileName,'*csv.2*'));
    ADE = []; ADDfft = [];
    for file = files2'
        filename = file.name;
        distractorTonefile=fullfile(baseFileName,filename)
        ADD = importdata(distractorTonefile);
        ADD = ADD(:,2:end);
        [row,col] = size(ADD);
        for k = 1:col
            ADE = ADD(:,k);
            N = length(ADE);
            xdft = fft(ADE);
            xdft = xdft(1:N/2+1);
            psdx = (1/(Fs*N)) * abs(xdft).^2;
            psdx(2:end-1) = 2*psdx(2:end-1);
            freq = 0:Fs/N:Fs/2;
            ADDfft(:,k) = psdx;
        end
        cd ..
        cd ADD_fft
        dlmwrite(strcat('NADfft',num2str(x),'.csv'),ADDfft);
        cd ..
        cd AD_csv      
    end
    
    x = x+1;
end
cd ..