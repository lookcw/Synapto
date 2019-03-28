cd HC_BD
dirs  = dir(fullfile('.','*.txt'));
k=1;
AllHC = zeros(308281,24,12);
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    AllHC(:,:,k) = toMat(filename);
    k = k+1;
end

AllHC = permute(AllHC,[2,1,3]);