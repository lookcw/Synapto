% Must start in a folder containing 'HC_BD_Fil', 'AD_BD_Fil'

Fs = 250;

% HC ---------------------
cd HC_BD_Fil
dirs = dir(fullfile('.','*.txt'));
x = 1; HCEp = [];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    HC = importdata(filename);
    HC = HC(2:end,3:23);
    [row,col] = size(HC);
    for k = 1:col
        HCEp(:,:,k,x) = intoEpochs(HC(:,k),8,Fs,660); % 8 sec x 82 epochs x 21 electrodes x 12 HC patients
    end
    x = x+1;
end
cd ..

% AD ---------------------
cd AD_BD_Fil
dirs = dir(fullfile('.','*.txt'));
x = 1; ADEp = [];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    AD = importdata(filename);
    AD = AD(2:end,3:23);
    [row,col] = size(AD);
    for k = 1:col
        ADEp(:,:,k,x) = intoEpochs(AD(:,k),8,Fs,660); % 8 sec x 82 epochs x 21 electrodes x 13 AD patients
    end
    x = x+1;
end
cd ..
