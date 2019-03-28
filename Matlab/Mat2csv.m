cd ../HC_GD

dirs1 = dir(fullfile('.','*.mat'));
dirs2 = dir(fullfile('.','*.txt'));
for k = 1:19
    filename1 = dirs1(k).name;
    filename2 = dirs2(k).name;
    [S,T] = EventAvgHC(filename1,filename2);
    csvwrite(strcat('StanHC',num2str(k),'.csv'),S);
    csvwrite(strcat('TargHC',num2str(k),'.csv'),T);
end
