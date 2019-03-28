% Imports HC and AD data, turns each into 6 min long matrix (by 21
% electrodes); 6 min length is chosen randomly for each patient

cd HCF50
dirs = dir(fullfile('.','*.csv'));
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    H = importdata(filename);
    H = H(1:165000,:);
    p = randperm(75001,1);
    p36 = dec2base(p,36,4);
    Hn = H(p:90000+p-1,:);
    cd ..
    cd HCF50ran6
    Fname = strcat(filename(1:9),'_',p36,'.csv');
    dlmwrite(Fname,Hn,'delimiter',',','-append');
    cd ..
    cd HCF50
end
cd ..

cd ADF50
dirs = dir(fullfile('.','*.csv'));
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    A = importdata(filename);
    A = A(1:165000,:);
    p = randperm(75000,1);
    p36 = dec2base(p,36,4);
    An = A(p:90000+p-1,:);
    cd ..
    cd ADF50ran6
    Fname = strcat(filename(1:9),'_',p36,'.csv');
    dlmwrite(Fname,An,'delimiter',',','-append');
    cd ..
    cd ADF50
end