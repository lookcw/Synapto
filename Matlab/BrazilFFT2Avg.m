% Must start in a folder containing 'HC_fft_B', 'AD_fft_B', 'HC_fft', 'AD_fft'

Fs = 250;

% HC ---------------------
cd HC_fft
dirs = dir(fullfile('.','*.csv'));
x = 1; HCfftBin = [];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    HC = importdata(filename);
    [row,col] = size(HC);
    for k = 1:col
        n = 1;
        for l = 1:250:row-1
            HCfftBin(n,k) = mean(HC(l:l+250,k));
            n = n+1;
        end
    end
    cd ..
    cd HC_fft_B
    dlmwrite(strcat('BHfftB',num2str(x),'.csv'),HCfftBin);
    cd ..
    cd HC_fft
    x = x+1;
end
cd ..


% AD ---------------------
cd AD_fft
dirs = dir(fullfile('.','*.csv'));
x = 1; ADfftBin = [];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    AD = importdata(filename);
    [row,col] = size(AD);
    for k = 1:col
        n = 1;
        for l = 1:250:row-1
            ADfftBin(n,k) = mean(AD(l:l+250,k));
            n = n+1;
        end
    end
    cd ..
    cd AD_fft_B
    dlmwrite(strcat('BAfftB',num2str(x),'.csv'),ADfftBin);
    cd ..
    cd AD_fft
    x = x+1;
end
cd ..

