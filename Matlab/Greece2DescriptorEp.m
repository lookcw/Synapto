Fs = 250; EpLen = 301;

% HC -----------------------------------------
cd HC_GD
cd HC_Split
dirs  = dir(fullfile('.','*.csv'));
descriptorS=[]; ParPatH = [];
for file = dirs'
    filename = file.name;
    stimulusTonefile=fullfile(filename)
    dat = importdata(stimulusTonefile);
    stimP50 =erpnMat(dat,24, 72, 'max',EpLen);
    stimN100=erpnMat(dat,70, 130,'min',EpLen);
    stimP200=erpnMat(dat,180,235,'max',EpLen);
    stimN200=erpnMat(dat,120,340,'min',EpLen); % 120,340 % 205,315
    stimP3a =erpnMat(dat,325,500,'max',EpLen);
    stimP3b =erpnMat(dat,280,680,'max',EpLen); % 280,680 % 325,580
    stimSlow=erpnMat(dat,460,680,'min',EpLen);
    latP50 =latMat(dat,24, 72, 'max',EpLen);
    latN100=latMat(dat,70, 130,'min',EpLen);
    latP200=latMat(dat,180,235,'max',EpLen);
    latN200=latMat(dat,120,340,'min',EpLen); % 120,340 % 205,315
    latSlow=latMat(dat,460,680,'min',EpLen);
    latP3b =latMat(dat,280,680,'max',EpLen); % 280,680 % 325,580
    %brazilstat_vector=brazilstat(dat);
    %brazilstatMat_vector=brazilStatMat(bands(dat));
    
    % E=[];
    % tandDat = importdata(dat);
    % [row,col] = size(tandDat);
    % for k = 2:col
    %     FF = tandDat(:,k);
    %     N = length(FF);
    %     xdft = fft(FF);
    %     xdft = xdft(1:N/2+1);
    %     psdx = (1/(Fs*N)) * abs(xdft).^2;
    %     psdx(2:end-1) = 2*psdx(2:end-1);
    %     fftval = psdx';
    %     E = [E,fftval];
    % end
    
    ParPatH = str2double(filename(3:4));
    
    %descriptorS = [descriptorS;ParPatH,stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow]; %,latN200,latSlow,latP3b,brazilstat_vector,brazilstatMat_vector];
    descriptorS = [descriptorS;ParPatH,stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,latP50,latN100,latP200,latN200,latSlow,latP3b]; %,brazilstat_vector,E];
    %descriptorS = [descriptorS;ParPatH,latP50,latN100,latP200,latN200, latSlow,latP3b];
end
cd ..
cd ..

% cd HC_targAvg
% dirs  = dir(fullfile('.','*.csv'));
% descriptorT=[];
% for file = dirs'
%     filename = file.name;
%     stimulusTonefile=fullfile(filename)
%     dat = importdata(stimulusTonefile);
%     stimP50 =erpnMat(dat,24, 72, 'max',EpLen);
%     stimN100=erpnMat(dat,70, 130,'min',EpLen);
%     stimP200=erpnMat(dat,180,235,'max',EpLen);
%     stimN200=erpnMat(dat,120,340,'min',EpLen);
%     stimP3a =erpnMat(dat,325,500,'max',EpLen);
%     stimP3b =erpnMat(dat,280,680,'max',EpLen);
%     stimSlow=erpnMat(dat,460,680,'min',EpLen);
%     latP50 =latMat(dat,24, 72, 'max',EpLen);
%     latN100=latMat(dat,70, 130,'min',EpLen);
%     latP200=latMat(dat,180,235,'max',EpLen);
%     latN200=latMat(dat,120,340,'min',EpLen);
%     latSlow=latMat(dat,460,680,'min',EpLen);
%     latP3b =latMat(dat,280,680,'max',EpLen);
%     %brazilstat_vector=brazilstat(dat);
%     %brazilstatMat_vector=brazilStatMat(bands(dat));
%
% % E=[];
% % tandDat = importdata(dat);
% % [row,col] = size(tandDat);
% % for k = 2:col
% %     FF = tandDat(:,k);
% %     N = length(FF);
% %     xdft = fft(FF);
% %     xdft = xdft(1:N/2+1);
% %     psdx = (1/(Fs*N)) * abs(xdft).^2;
% %     psdx(2:end-1) = 2*psdx(2:end-1);
% %     fftval = psdx';
% %     E = [E,fftval];
% % end
%
%     %descriptorT = [descriptorT;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow]; %,latN200,latSlow,latP3b,brazilstat_vector,brazilstatMat_vector];
%     descriptorT = [descriptorT;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,latP50,latN100,latP200,latN200,latSlow,latP3b]; %,brazilstat_vector,E];
%     %descriptorT = [descriptorT;latP50,latN100,latP200,latN200]; %,latSlow,latP3b];
% end
% cd ..

descriptorST = [descriptorS]; %,descriptorT];
Ind0 = {};
for n = 1:size(descriptorST,1)
    Ind0{n} = '0';
end
Ind0 = string(Ind0);
descriptorH = [descriptorST,Ind0'];
%dlmwrite('GreeceHC.csv',descriptor,'delimiter',',','-append');




% MCI ----------------------------------------
cd MCI_GD
cd MCI_Split
dirs  = dir(fullfile('.','*.csv'));
descriptorS=[]; ParPatM = [];
for file = dirs'
    filename = file.name;
    stimulusTonefile=fullfile(filename)
    dat = importdata(stimulusTonefile);
    stimP50 =erpnMat(dat,24, 72, 'max',EpLen);
    stimN100=erpnMat(dat,70, 130,'min',EpLen);
    stimP200=erpnMat(dat,180,235,'max',EpLen);
    stimN200=erpnMat(dat,205,315,'min',EpLen);
    stimP3a =erpnMat(dat,325,500,'max',EpLen);
    stimP3b =erpnMat(dat,325,580,'max',EpLen);
    stimSlow=erpnMat(dat,460,680,'min',EpLen);
    latP50 =latMat(dat,24, 72, 'max',EpLen);
    latN100=latMat(dat,70, 130,'min',EpLen);
    latP200=latMat(dat,180,235,'max',EpLen);
    latN200=latMat(dat,205,315,'min',EpLen);
    latSlow=latMat(dat,460,680,'min',EpLen);
    %latP3b =latMat(dat,325,580,'max',EpLen);
    %brazilstat_vector=brazilstat(dat);
    %brazilstatMat_vector=brazilStatMat(bands(dat));
    
    % E=[];
    % tandDat = importdata(dat);
    % [row,col] = size(tandDat);
    % for k = 2:col
    %     FF = tandDat(:,k);
    %     N = length(FF);
    %     xdft = fft(FF);
    %     xdft = xdft(1:N/2+1);
    %     psdx = (1/(Fs*N)) * abs(xdft).^2;
    %     psdx(2:end-1) = 2*psdx(2:end-1);
    %     fftval = psdx';
    %     E = [E,fftval];
    % end
    
    ParPatM = str2double(filename(4:5))+ParPatH;
    
    %descriptorS = [descriptorS;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow]; %,latN200,latSlow,latP3b,brazilstat_vector,brazilstatMat_vector];
    descriptorS = [descriptorS;ParPatM,stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,latP50,latN100,latP200,latN200,latSlow,latP3b]; %,brazilstat_vector,E];
    %descriptorS = [descriptorS;latP50,latN100,latP200,latN200]; %,latSlow,latP3b];
end
cd ..
cd ..

% cd MCI_targAvg
% dirs  = dir(fullfile('.','*.csv'));
% descriptorT=[];
% for file = dirs'
%     filename = file.name;
%     stimulusTonefile=fullfile(filename)
%     dat = importdata(stimulusTonefile);
%     stimP50 =erpnMat(dat,24, 72, 'max',EpLen);
%     stimN100=erpnMat(dat,70, 130,'min',EpLen);
%     stimP200=erpnMat(dat,180,235,'max',EpLen);
%     stimN200=erpnMat(dat,205,315,'min',EpLen);
%     stimP3a =erpnMat(dat,325,500,'max',EpLen);
%     stimP3b =erpnMat(dat,325,580,'max',EpLen);
%     stimSlow=erpnMat(dat,460,680,'min',EpLen);
%     latP50 =latMat(dat,24, 72, 'max',EpLen);
%     latN100=latMat(dat,70, 130,'min',EpLen);
%     latP200=latMat(dat,180,235,'max',EpLen);
%     latN200=latMat(dat,205,315,'min',EpLen);
%     latSlow=latMat(dat,460,680,'min',EpLen);
%     latP3b =latMat(dat,325,580,'max',EpLen);
%     %brazilstat_vector=brazilstat(dat);
%     %brazilstatMat_vector=brazilStatMat(bands(dat));
%
% % E=[];
% % tandDat = importdata(stimulusTonefile);
% % [row,col] = size(tandDat);
% % for k = 2:col
% %     FF = tandDat(:,k);
% %     N = length(FF);
% %     xdft = fft(FF);
% %     xdft = xdft(1:N/2+1);
% %     psdx = (1/(Fs*N)) * abs(xdft).^2;
% %     psdx(2:end-1) = 2*psdx(2:end-1);
% %     fftval = psdx';
% %     E = [E,fftval];
% % end
%
%     %descriptorT = [descriptorT;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,latN200,latSlow,latP3b,brazilstat_vector,brazilstatMat_vector];
%     descriptorT = [descriptorT;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,latP50,latN100,latP200,latN200,latSlow,latP3b]; %,brazilstat_vector,E];
%     %descriptorT = [descriptorT;latP50,latN100,latP200,latN200]; %,latSlow,latP3b];
% end
% cd ..
% cd ..

descriptorST = [descriptorS]; %,descriptorT];
Ind2 = {};
for n = 1:size(descriptorST,1)
    Ind2{n} = '1';
end
Ind2 = string(Ind2);
descriptorM = [descriptorST,Ind2'];
%dlmwrite('GreeceHC.csv',descriptor,'delimiter',',','-append');




% % AD -----------------------------------------
% cd AD_GD
% cd AD_Split
% dirs  = dir(fullfile('.','*.csv'));
% descriptorS=[]; ParPatA = [];
% for file = dirs'
%     filename = file.name;
%     stimulusTonefile=fullfile(filename)
%     dat = importdata(stimulusTonefile);
%     stimP50= erpnMat(dat,24, 72, 'max',EpLen);
%     stimN100=erpnMat(dat,70, 130,'min',EpLen);
%     stimP200=erpnMat(dat,180,235,'max',EpLen);
%     stimN200=erpnMat(dat,120,340,'min',EpLen);
%     stimP3a= erpnMat(dat,325,500,'max',EpLen);
%     stimP3b= erpnMat(dat,280,680,'max',EpLen);
%     stimSlow=erpnMat(dat,460,680,'min',EpLen);
%     latP50 =latMat(dat,24, 72, 'max',EpLen);
%     latN100=latMat(dat,70, 130,'min',EpLen);
%     latP200=latMat(dat,180,235,'max',EpLen);
%     latN200=latMat(dat,120,340,'min',EpLen);
%     latSlow=latMat(dat,460,680,'min',EpLen);
%     latP3b =latMat(dat,280,680,'max',EpLen);
%     %brazilstat_vector=brazilstat(stimulusTonefile);
% %     brazilstatMat_vector=brazilStatMat(bands(stimulusTonefile));
% 
% % E=[];
% % tandDat = importdata(stimulusTonefile);
% % [row,col] = size(tandDat);
% % for k = 2:col
% %     FF = tandDat(:,k);
% %     N = length(FF);
% %     xdft = fft(FF);
% %     xdft = xdft(1:N/2+1);
% %     psdx = (1/(Fs*N)) * abs(xdft).^2;
% %     psdx(2:end-1) = 2*psdx(2:end-1);
% %     fftval = psdx';
% %     E = [E,fftval];
% % end
% 
%     ParPatA = str2double(filename(3:4))+ParPatH;
% 
%     %descriptorS = [descriptorS;ParPatA,stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow]; %,latN200,latSlow,latP3b,brazilstat_vector,brazilstatMat_vector];
%     descriptorS = [descriptorS;ParPatA,stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,latP50,latN100,latP200,latN200,latSlow,latP3b]; %,brazilstat_vector,E];
%     %descriptorS = [descriptorS;ParPatA,latP50,latN100,latP200,latN200,latSlow,latP3b];
% end
% cd ..
% cd ..
%
% cd AD_targ
% dirs  = dir(fullfile('.','*.csv'));
% descriptorT=[];
% for file = dirs'
%     filename = file.name;
%     stimulusTonefile=fullfile(filename)
%     stimP50 =erpnMat(stimulusTonefile,24, 72, 'max',EpLen);
%     stimN100=erpnMat(stimulusTonefile,70, 130,'min',EpLen);
%     stimP200=erpnMat(stimulusTonefile,180,235,'max',EpLen);
%     stimN200=erpnMat(stimulusTonefile,120,340,'min',EpLen);
%     stimP3a =erpnMat(stimulusTonefile,325,500,'max',EpLen);
%     stimP3b =erpnMat(stimulusTonefile,280,680,'max',EpLen);
%     stimSlow=erpnMat(stimulusTonefile,460,680,'min',EpLen);
%     latP50 =latMat(stimulusTonefile,24, 72, 'max',EpLen);
%     latN100=latMat(stimulusTonefile,70, 130,'min',EpLen);
%     latP200=latMat(stimulusTonefile,180,235,'max',EpLen);
%     latN200=latMat(stimulusTonefile,120,340,'min',EpLen);
%     latSlow=latMat(stimulusTonefile,460,680,'min',EpLen);
%     latP3b =latMat(stimulusTonefile,280,680,'max',EpLen);
%     brazilstat_vector=brazilstat(stimulusTonefile);
% %     brazilstatMat_vector=brazilStatMat(bands(stimulusTonefile));
%
% E=[];
% tandDat = importdata(stimulusTonefile);
% [row,col] = size(tandDat);
% for k = 2:col
%     FF = tandDat(:,k);
%     N = length(FF);
%     xdft = fft(FF);
%     xdft = xdft(1:N/2+1);
%     psdx = (1/(Fs*N)) * abs(xdft).^2;
%     psdx(2:end-1) = 2*psdx(2:end-1);
%     fftval = psdx';
%     E = [E,fftval];
% end
%
%     %descriptorT = [descriptorT;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,latN200,latSlow,latP3b,brazilstat_vector,brazilstatMat_vector];
%     descriptorT = [descriptorT;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,latP50,latN100,latP200,latN200,latSlow,latP3b,brazilstat_vector,E];
%     %descriptorT = [descriptorT;latN200,latSlow,latP3b];
% end
% cd ..
%
% descriptorST = [descriptorS]; %,descriptorT];
% Ind1 = {};
% for n = 1:size(descriptorST,1)
%     Ind1{n} = '+';
% end
% Ind1 = string(Ind1);
% descriptorA = [descriptorST,Ind1'];
%dlmwrite('GreeceAD.csv',descriptor,'delimiter',',','-append');




% Labels -------------------------------------
labels = {};
for k = 1:size(descriptorST,2)
    labels{k} = strcat('col',num2str(k));
end
labels{size(descriptorST,2)+1} = 'Indicator';
labels{1} = 'patient num';
labels = string(labels);



% Descriptor Matrix --------------------------
descriptor = [descriptorH;descriptorM]; %;descriptorM];
labdesc = [labels;descriptor];
fid=fopen('GD_erpAmpLat_ins504_HCvMCI_1.csv','wt');
[rows,cols]=size(labdesc);
for k = 1:rows
    fprintf(fid,'%s,',labdesc{k,1:end-1});
    fprintf(fid,'%s\n',labdesc{k,end});
end
fclose(fid);

