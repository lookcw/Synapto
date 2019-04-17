
% HC ---------------------
cd HC_fft_B
dirs = dir(fullfile('.','*.csv'));
x = 1;
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    HC(:,:,x) = importdata(filename);
    [row,col,pla] = size(HC);
    for k = 1:col
        HCP(x,(k-1)*row+1:k*row) = HC(:,k,x);
    end
    
    x = x+1;
end
cd ..
%dlmwrite('HCFFT.csv',HCP);


% AD ---------------------
cd AD_fft_B
dirs = dir(fullfile('.','*.csv'));
x = 1;
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    AD(:,:,x) = importdata(filename);
    [row,col,pla] = size(AD);
    for k = 1:col
        ADP(x,(k-1)*row+1:k*row) = AD(:,k,x);
    end
    
    x = x+1;
end
cd ..
%dlmwrite('ADFFT.csv',ADP);

Ind0 = {};
for n = 1:size(HCP,1)
    Ind0{n} = '-';
end
Ind0 = string(Ind0);
AllHC = [HCP,Ind0'];

Ind1 = {};
for n = 1:size(ADP,1)
    Ind1{n} = '+';
end
Ind1 = string(Ind1);
AllAD = [ADP,Ind1'];


AllFFT = [AllHC;AllAD];
fid=fopen('AllFFT_B.csv','wt');
[rows,cols]=size(AllFFT);
for k = 1:rows
    fprintf(fid,'%s,',AllFFT{k,1:end-1});
    fprintf(fid,'%s\n',AllFFT{k,end});
end
fclose(fid);
