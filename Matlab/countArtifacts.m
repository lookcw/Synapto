dat1 = importdata(filename1);
for k = 1:size(dat1,2)/21
    data1(:,:,k) = dat1(:,(k-1)*21+1:k*21); % (data)row x (electrode)column x (patient)plane
end

[row,col,pla] = size(data1);
Fs = 250; EpochLength = 8;
HC = []; H_All = [];
for k = 1:pla
    H = [];
    ep = intoEpochs(data1(:,:,k),EpochLength,Fs,660); % (data)row x (electrode)column x (epoch)plane
    ar = AAR_StDev(ep,7); % (data)row x (electrode)column x (epoch)plane   [some missing columns]
    
    for p = 1:size(ar,3)
        art = 0;
        for v = 1:col
            if isnan(ar(1,v,p))
                art = art + 1;
            end
        end
        H = [H,art];
    end
    H_All = [H_All;sum(H)];
    HC = [HC;H];
end

Ind0 = {};
for n = 1:size(HC,1)
    Ind0{n} = '-';
end
Ind0 = string(Ind0);
descriptorH = [HC,Ind0'];



dat2 = importdata(filename2);
for k = 1:size(dat2,2)/21
    data2(:,:,k) = dat2(:,(k-1)*21+1:k*21); % (data)row x (electrode)column x (patient)plane
end

[row,col,pla] = size(data2);
Fs = 250;
AD = []; A_All = [];
for k = 1:pla
    A = [];
    ep = intoEpochs(data2(:,:,k),EpochLength,Fs,660); % (data)row x (electrode)column x (epoch)plane
    ar = AAR_StDev(ep,7); % (data)row x (electrode)column x (epoch)plane   [some missing columns]
    
    for p = 1:size(ar,3)
        art = 0;
        for v = 1:col
            if isnan(ar(1,v,p))
                art = art + 1;
            end
        end
        A = [A,art];
    end
    A_All = [A_All;sum(A)];
    AD = [AD;A];
end

Ind1 = {};
for n = 1:size(AD,1)
    Ind1{n} = '+';
end
Ind1 = string(Ind1);
descriptorA = [AD,Ind1'];


labels = {};
for k = 1:size(AD,2)
    labels{k} = strcat('col',num2str(k));
end
labels{size(AD,2)+1} = 'Indicator';
labels = string(labels);


descriptor = [descriptorH;descriptorA];
labdesc = [labels;descriptor];
fid=fopen('Artifacts.csv','wt');
[rows,cols]=size(labdesc);
for k = 1:rows
    fprintf(fid,'%s,',labdesc{k,1:end-1});
    fprintf(fid,'%s\n',labdesc{k,end});
end
fclose(fid);