Fs = 250;

% HC ---------------------
%cd HCF50
dirs = dir(fullfile('.','*.csv'));
x = 1;
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    pat = importdata(filename)';
    pat = pat(1:end,2:22);
    nf = extractAfter(filename,'lp');
    if length(nf) > 5
        n = nf(1:2);
    elseif length(nf) <= 5
        n = strcat('0',nf(1));
    end
    dlmwrite(strcat('HC_50lp',n,'.csv'),pat);
    x = x+1;
end
cd ..


%% AD ---------------------
%cd ADF50
dirs = dir(fullfile('.','*.csv'));
x = 1;
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    pat = importdata(filename)';
    pat = pat(1:end,2:22);
    nf = extractAfter(filename,'lp');
    if length(nf) > 5
        n = nf(1:2);
    elseif length(nf) <= 5
        n = strcat('0',nf(1));
    end
    dlmwrite(strcat('AD_50lp',n,'.csv'),pat);
    x = x+1;
end
cd ..
