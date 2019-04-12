Fs = 250;

% HC ---------------------
cd HCF50
dirs = dir(fullfile('.','*.csv'));
rowS = Fs*660; patCut = [];
x = 1;
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    pat = importdata(filename)';
    patCut(:,:,x) = pat(1:rowS,2:22);
    
    x = x+1;
end
cd ..
dlmwrite('HC11m_A.csv',patCut);


% AD ---------------------
cd ADF50
dirs = dir(fullfile('.','*.csv'));
rowS = Fs*660; patCut = [];
x = 1; 
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    pat = importdata(filename)';
    patCut(:,:,x) = pat(1:rowS,2:22);
    
    x = x+1;
end
cd ..
dlmwrite('AD11m_A.csv',patCut);
