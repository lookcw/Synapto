Fs = 250;

% HC ---------------------
cd HC_BD_Fil
dirs = dir(fullfile('.','*.txt'));
x = 1;
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    HC = importdata(filename);
    HC = HC(2:end,3:23)';
    [wIC,A,W,IC] = wICA(HC);
    Ahat = A*wIC;
    HCAR = HC-Ahat;
    cd ..
    cd HC_Fil_AR
    dlmwrite(strcat('BHAR',num2str(x),'.txt'),HCAR);
    cd ..
    cd HC_BD_Fil
    x = x+1;
end
cd ..


% AD ---------------------
cd AD_BD_Fil
dirs = dir(fullfile('.','*.txt'));
x = 1;
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    AD = importdata(filename);
    AD = AD(2:end,3:23)';
    [wIC,A,W,IC] = wICA(AD);
    Ahat = A*wIC;
    ADAR = AD-Ahat;
    cd ..
    cd AD_Fil_AR
    dlmwrite(strcat('BAAR',num2str(x),'.txt'),ADAR);
    cd ..
    cd AD_BD_Fil
    x = x+1;
end
cd ..
