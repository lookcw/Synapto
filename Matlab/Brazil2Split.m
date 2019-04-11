Fs = 250;
LengthT = 660;
InsPerPat = 5;

cd HCF50_1
dirs = dir(fullfile('.','*.csv'));
descriptorRH=[];
x = 1; y = 1;
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    dat = importdata(filename);
    dat = dat(1:Fs*LengthT,:);
    
    cd ..
    cd HC_Split05
    
    L = size(dat,1)/InsPerPat;
    for k = 1:InsPerPat
        datSplit(:,:,k) = dat(L*(k-1)+1:L*k,:);
        datN = datSplit(:,:,k);
        
        if x < 10
        na = strcat('0',num2str(x));
        else
        na = num2str(x);
        end
        
        if y < 10
            n = strcat('00',num2str(y));
        elseif y >= 10 && y < 100
            n = strcat('0',num2str(y));
        else
            n = num2str(y);
        end
        
        dlmwrite(strcat('HC',na,'_',n,'.csv'),datN);
        
        y = y+1;
    end
    
    cd ..
    cd HCF50_1
    
    x = x+1;
end