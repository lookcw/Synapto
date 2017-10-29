% Must start in a folder containing 'HC_BD_Fil', 'AD_BD_Fil', 'HC_BD', 'AD_BD'

EL = 8; % Epoch Length in seconds
%FPz=2; Oz=20; F3=6; P3=16; F4=8; P4=18; % (for convolution)

% HC -----------------
cd HC_BD_Fil
dirs = dir(fullfile('.','*.txt'));
descriptorRH=[];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    hig  = higuchi(filename,EL);
%     cent = spec_cent(filename,EL);
%     ent  = spec_ent(filename,EL);
%     peak = spec_peak(filename,EL);
%     roll = spec_roll(filename,EL,80);
%     slow = slowing(filename,EL);
%     con  = fftConMax(filename,EL);
%     braz = brazilstatRest(filename,EL);
%     pow  = bandpow(filename,EL);
    
    %descriptorRH=[descriptorRH;hig,cent,ent,peak,roll]; %,con];
    descriptorRH=[descriptorRH;hig];
end

cd ..
%Ind0 = zeros(length(dirs),1);
Ind0 = {};
for n = 1:size(descriptorRH,1)
    Ind0{n} = '-';
end
Ind0 = string(Ind0);
descriptorH = [descriptorRH,Ind0'];

% cd HC_BD
% dirs = dir(fullfile('.','*.txt'));
% scoreH=[];
% for file = dirs'
%     filename = file.name;
%     filename = upper(fullfile(filename));
%     nfilename = extractAfter(filename,'MM');
%     scoreH = [scoreH;str2double(nfilename(1:2))];
% end
% descriptorH = [descriptorRH,scoreH];
% cd ..


% AD -----------------
cd AD_BD_Fil
dirs = dir(fullfile('.','*.txt'));
descriptorRA=[];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    hig  = higuchi(filename,EL);
%     cent = spec_cent(filename,EL);
%     ent  = spec_ent(filename,EL);
%     peak = spec_peak(filename,EL);
%     roll = spec_roll(filename,EL,80);
%     slow = slowing(filename,EL);
%     con  = fftConMax(filename,EL);
%     braz = brazilstatRest(filename,EL);
%     pow  = bandpow(filename,EL);
    
    %descriptorRA=[descriptorRA;hig,cent,ent,peak,roll]; %,con];
    descriptorRA=[descriptorRA;hig];
end

cd ..
%Ind1 = zeros(length(dirs),1)+1;
Ind1 = {};
for n = 1:size(descriptorRA,1)
    Ind1{n} = '+';
end
Ind1 = string(Ind1);
descriptorA = [descriptorRA,Ind1'];

% cd AD_BD
% dirs = dir(fullfile('.','*.txt'));
% scoreA=[];
% for file = dirs'
%     filename = file.name;
%     filename = upper(fullfile(filename));
%     nfilename = extractAfter(filename,'MM');
%     scoreA = [scoreA;str2double(nfilename(1:2))];
% end
% descriptorA = [descriptorRH,scoreA];
% cd ..

% --------------------
labels = {};
for r = 1:21:length(hig)
    for k = 1:21
        labels{k+(r-1)} = strcat('hig',num2str((r-1)/21+1),'E',num2str(k));
    end
end
labels{length(descriptorRH)+1} = 'Indicator';
labels = string(labels);

descriptor = [descriptorH;descriptorA];
labdesc = [labels;descriptor];
fid=fopen('Fil_higAvg.csv','wt');
[rows,cols]=size(labdesc);
for i=1:rows
    fprintf(fid,'%s,',labdesc{i,1:end-1});
    fprintf(fid,'%s\n',labdesc{i,end});
end
fclose(fid);

