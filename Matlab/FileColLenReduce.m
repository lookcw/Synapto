Fs = 250;

cd MCI_stanStack
dirs1 = dir(fullfile('.','*.csv'));
x = 1; len = [];
for file1 = dirs1'
    filename1 = file1.name;
    filename1 = fullfile(filename1)
    dat = importdata(filename1);
    
    len(x) = size(dat,1);
    x = x+1;
end
minL = min(len);
%%
x = 1;
for file1 = dirs1'
    filename1 = file1.name;
    filename1 = fullfile(filename1)
    dat = importdata(filename1);
    
    datn = dat(1:minL,:);
    
    if x < 10
        n = strcat('0',num2str(x));
    else
        n = num2str(x);
    end
    
    cd ..
    cd MCI_stanStackNorm
    dlmwrite(strcat('MCIstanSN',n,'.csv'),datn);
    cd ..
    cd MCI_stanStack
    
    x = x+1;
end