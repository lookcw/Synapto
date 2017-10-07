function dat = toMat(filename)
fid = fopen(filename,'r');
cac = textscan(fid,'%s','Delimiter','\n');
[~] = fclose(fid);
cac1 = cac{1,1};
for k = 1:length(cac1)
    if strfind(cac1{k},';') ~= 0
        cac1{k} = [];
    end
end
cac1 = cac1(~cellfun('isempty',cac1));

cac8 = cell(round(length(cac1)/8),1);
for k = 1:round(length(cac1)/8)
    cac8{k,1} = cac1{8*k-7,1};
end

cac8n = cac8;
for k = 1:length(cac8)
    cac8n{k} = strrep(cac8{k},',','.');
end

one_str = strjoin(cac8n,'\n');
result  = textscan(one_str,'%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f','CollectOutput',true);
dat = result{1};
end

