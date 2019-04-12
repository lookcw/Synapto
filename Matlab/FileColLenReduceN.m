Fs = 250;

lenT = 1:3; lenS = 1:3;
cd AD_GD
cd AD_stanStackNorm
dat = importdata('ADstanSN01.csv');
lenS(1) = size(dat,1);
cd ..
cd AD_targStackNorm
dat = importdata('ADtargSN01.csv');
lenT(1) = size(dat,1);
cd ..
cd ..
cd HC_GD
cd HC_stanStackNorm
dat = importdata('HCstanSN01.csv');
lenS(2) = size(dat,1);
cd ..
cd HC_targStackNorm
dat = importdata('HCtargSN01.csv');
lenT(2) = size(dat,1);
cd ..
cd ..
cd MCI_GD
cd MCI_stanStackNorm
dat = importdata('MCIstanSN01.csv');
lenS(3) = size(dat,1);
cd ..
cd MCI_targStackNorm
dat = importdata('MCItargSN01.csv');
lenT(3) = size(dat,1);
cd ..
cd ..

minLT = min(lenT);
minLS = min(lenS);
%%
cd MCI_GD
cd MCI_targStack
dirs1 = dir(fullfile('.','*.csv'));
x = 1;
for file1 = dirs1'
    filename1 = file1.name;
    filename1 = fullfile(filename1)
    dat = importdata(filename1);
    
    datn = dat(1:minLT,:);
    
    if x < 10
        n = strcat('0',num2str(x));
    else
        n = num2str(x);
    end
    
    cd ..
    cd MCI_targStackNormAll
    dlmwrite(strcat('ADtargSNA',n,'.csv'),datn);
    cd ..
    cd MCI_targStack
    
    x = x+1;
end