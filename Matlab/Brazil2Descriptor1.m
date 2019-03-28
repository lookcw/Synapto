%HigH = higuchi1('HC11m_A.csv',8);
%HigA = higuchi1('AD11m_A.csv',8);

CentH = spec_cent1('HC11m_A.csv',8);
CentA = spec_cent1('AD11m_A.csv',8);

%PeakH = spec_peak1('HC11m_A.csv',8);
%PeakA = spec_peak1('AD11m_A.csv',8);

Ind0 = {};
for n = 1:size(CentH,1)
    Ind0{n} = '-';
end
Ind0 = string(Ind0);
descriptorH = [CentH,Ind0'];

Ind1 = {};
for n = 1:size(CentA,1)
    Ind1{n} = '+';
end
Ind1 = string(Ind1);
descriptorA = [CentA,Ind1'];


labels = {};
for k = 1:size(CentA,2)
    labels{k} = strcat('col',num2str(k));
end
labels{size(CentA,2)+1} = 'Indicator';
labels = string(labels);


descriptor = [descriptorH;descriptorA];
labdesc = [labels;descriptor];
fid=fopen('CentTest.csv','wt');
[rows,cols]=size(labdesc);
for k = 1:rows
    fprintf(fid,'%s,',labdesc{k,1:end-1});
    fprintf(fid,'%s\n',labdesc{k,end});
end
fclose(fid);