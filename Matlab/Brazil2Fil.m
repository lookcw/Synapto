
% HC ---------------------
cd HC_BD
dirs = dir(fullfile('.','*.txt'));
x = 1;
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    HC = toMat(filename)';
    HCf50 = eegfilt(HC,250,0,50);
    
    cd ..
    cd HCF50_8
    dlmwrite(strcat('HC50lp8_',num2str(x),'.csv'),HCf50);
    cd ..
    cd HC_BD
    
    x = x+1;
    
end
cd ..

% AD ---------------------
cd AD_BD
dirs = dir(fullfile('.','*.txt'));
x = 1;
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    AD = toMat(filename)';
    ADf50 = eegfilt(AD,250,0,50);
    
    cd ..
    cd ADF50_8
    dlmwrite(strcat('AD50lp8_',num2str(x),'.csv'),ADf50);
    cd ..
    cd AD_BD
    
    x = x+1;
    
end
cd ..
