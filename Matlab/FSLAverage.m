% FSL Averages ---------------------
dirs = dir(fullfile('.','*.dat'));
SA=[]; SH=[]; y=1; x=1;
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    if filename(1) == 'A'
        A = importdata(filename);
        SA(:,:,x) = A;
        x = x+1;
    elseif filename(1) == 'H'
        H = importdata(filename);
        SH(:,:,y) = H;
        y = y+1;
    end
end

for k = 1:size(SA,1)
    for v = 1:size(SA,2)
        SAavg(k,v) = mean(SA(k,v,:));
    end
end

for k = 1:size(SH,1)
    for v = 1:size(SH,2)
        SHavg(k,v) = mean(SH(k,v,:));
    end
end
