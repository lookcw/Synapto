% Input: two 2D matricies n1 x m and n2 x m where...
% n1 and n2 = number of patients and m = number of features
% Output: a labeled descriptor matrix ready to be used for machine learning

% This function also writes a .csv file of the output in the current folder

function labdesc = combine4ML(HC,AD)

Ind0 = {};
for n = 1:size(HC,1)
    Ind0{n} = '-';
end
Ind0 = string(Ind0);
descriptorH = [HC,Ind0'];

Ind1 = {};
for n = 1:size(AD,1)
    Ind1{n} = '+';
end
Ind1 = string(Ind1);
descriptorA = [AD,Ind1'];

labels = {};
for k = 1:size(HC,2)
    labels{k} = strcat('col',num2str(k));
end
labels{k+1} = 'Indicator';
labels = string(labels);

labdesc = [labels;descriptorH;descriptorA];
fid=fopen('BrazilZones.csv','wt'); % CHANGE NAME HERE <<<<<
[rows,~]=size(labdesc);
for k = 1:rows
    fprintf(fid,'%s,',labdesc{k,1:end-1});
    fprintf(fid,'%s\n',labdesc{k,end});
end
fclose(fid);
