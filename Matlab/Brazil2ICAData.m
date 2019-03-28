Fs = 250;
cd ADF50
dirs = dir(fullfile('.','*.csv'));
x = 1;
for file = dirs'
    % Import data
    filename = file.name;
    filename=fullfile(filename)
    data = importdata(filename);
    data = data(1:Fs*660,:); %columns are electrodes
    [row,col] = size(data);
    
    [wIC,A] = wICA(data',[],5,0);
    ahat = A*wIC;
    nhat = data'-ahat;
    
    cd ..
    cd ADF50ICA
    
    nf = extractAfter(filename,'lp');
    if length(nf) > 5
        n = nf(1:2);
    elseif length(nf) <= 5
        n = strcat('0',nf(1));
    end
    dlmwrite(strcat('AD_50lp_ICA',n,'.csv'),nhat');
    x = x+1;
    
    cd ..
    cd ADF50
end