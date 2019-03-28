Fs = 125;

% HC ---------------------
cd HC_csv
dirs = dir(fullfile('.','*.xlsx'));
descriptorS=[]; descriptorT=[]; descriptorD=[];
for direc = dirs'
    delimiterIn = ',';
    baseFileName=direc.name
    
    files0 = dir(fullfile(baseFileName,'*csv.0*'));
    for file = files0'
        filename = file.name;
        stimulusTonefile=fullfile(baseFileName,filename)
        stimP50= erpn(stimulusTonefile,24, 72, 'max');
        stimN100=erpn(stimulusTonefile,70, 130,'min');
        stimP200=erpn(stimulusTonefile,180,235,'max');
        stimN200=erpn(stimulusTonefile,205,315,'min');
        stimP3a= erpn(stimulusTonefile,325,500,'max');
        stimP3b= erpn(stimulusTonefile,325,580,'max');
        stimSlow=erpn(stimulusTonefile,460,680,'min');
        lstimN200=lat(stimulusTonefile,205,315,'min');
        lstimSlow=lat(stimulusTonefile,460,680,'min');
        lstimP3b= lat(stimulusTonefile,325,580,'max');
        brazilstat_vector=brazilstat(stimulusTonefile);
        %bands_vector =brazilStatMat(bands(stimulusTonefile));

E=[];
tandDat = importdata(stimulusTonefile);
[row,col] = size(tandDat);
for k = 2:col
    FF = tandDat(:,k);
    N = length(FF);
    xdft = fft(FF);
    xdft = xdft(1:N/2+1);
    psdx = (1/(Fs*N)) * abs(xdft).^2;
    psdx(2:end-1) = 2*psdx(2:end-1);
    fftval = psdx';
    E = [E,fftval];
end

        
        %descriptorS = [descriptorS;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,bands_vector,E];
        descriptorS = [descriptorS;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,E];        
        %descriptorS = [descriptorS;E];
    end
    
    files1 = dir(fullfile(baseFileName,'*csv.1*'));
    for file = files1'
        filename = file.name;
        targetTonefile=fullfile(baseFileName,filename)
        targP50= erpn(targetTonefile,24, 72, 'max');
        targN100=erpn(targetTonefile,70, 130,'min');
        targP200=erpn(targetTonefile,180,235,'max');
        targN200=erpn(targetTonefile,205,315,'min');
        targP3a= erpn(targetTonefile,325,500,'max');
        targP3b= erpn(targetTonefile,325,580,'max');
        targSlow=erpn(targetTonefile,460,680,'min');
        ltargN200=lat(targetTonefile,205,315,'min');
        ltargSlow=lat(targetTonefile,460,680,'min');
        ltargP3b= lat(targetTonefile,325,580,'max');
        brazilstat_vector=brazilstat(targetTonefile);
        %bands_vector =brazilStatMat(bands(targetTonefile));

E=[];
tandDat = importdata(targetTonefile);
[row,col] = size(tandDat);
for k = 2:col
    FF = tandDat(:,k);
    N = length(FF);
    xdft = fft(FF);
    xdft = xdft(1:N/2+1);
    psdx = (1/(Fs*N)) * abs(xdft).^2;
    psdx(2:end-1) = 2*psdx(2:end-1);
    fftval = psdx';
    E = [E,fftval];
end
        
        %descriptorT = [descriptorT;targP50,targN100,targP200,targN200,targP3a,targP3b,targSlow,ltargN200,ltargSlow,ltargP3b,brazilstat_vector,bands_vector,E];
        descriptorT = [descriptorT;targP50,targN100,targP200,targN200,targP3a,targP3b,targSlow,ltargN200,ltargSlow,ltargP3b,brazilstat_vector,E];
        %descriptorT = [descriptorT;E];
    end
    
    files2 = dir(fullfile(baseFileName,'*csv.2*'));
    for file = files2'
        filename = file.name;
        distractorTonefile=fullfile(baseFileName,filename)
        distP50= erpn(distractorTonefile,24, 72, 'max');
        distN100=erpn(distractorTonefile,70, 130,'min');
        distP200=erpn(distractorTonefile,180,235,'max');
        distN200=erpn(distractorTonefile,205,315,'min');
        distP3a= erpn(distractorTonefile,325,500,'max');
        distP3b= erpn(distractorTonefile,325,580,'max');
        distSlow=erpn(distractorTonefile,460,680,'min');
        ldistN200=lat(distractorTonefile,205,315,'min');
        ldistSlow=lat(distractorTonefile,460,680,'min');
        ldistP3b= lat(distractorTonefile,325,580,'max');
        brazilstat_vector=brazilstat(distractorTonefile);
        %bands_vector =brazilStatMat(bands(distractorTonefile));

E=[];
tandDat = importdata(distractorTonefile);
[row,col] = size(tandDat);
for k = 2:col
    FF = tandDat(:,k);
    N = length(FF);
    xdft = fft(FF);
    xdft = xdft(1:N/2+1);
    psdx = (1/(Fs*N)) * abs(xdft).^2;
    psdx(2:end-1) = 2*psdx(2:end-1);
    fftval = psdx';
    E = [E,fftval];
end
        
        %descriptorD = [descriptorD;distP50,distN100,distP200,distN200,distP3a,distP3b,distSlow,ldistN200,ldistSlow,ldistP3b,brazilstat_vector,bands_vector,E];
        descriptorD = [descriptorD;distP50,distN100,distP200,distN200,distP3a,distP3b,distSlow,ldistN200,ldistSlow,ldistP3b,brazilstat_vector,E];
        %descriptorD = [descriptorD;E];
    end
    
end
cd ..

descriptorH = [descriptorS,descriptorT,descriptorD];
Ind0 = {};
for n = 1:size(descriptorH,1)
    Ind0{n} = '-';
end
Ind0 = string(Ind0);
descriptorH = [descriptorH,Ind0'];




% AD ---------------------
cd AD_csv
dirs = dir(fullfile('.','*.xlsx'));
descriptorS=[]; descriptorT=[]; descriptorD=[];
for direc =dirs'
    delimiterIn = ',';
    baseFileName=direc.name
    files0 = dir(fullfile(baseFileName,'*csv.0*'));
    
    for file = files0'
        filename = file.name;
        stimulusTonefile=fullfile(baseFileName,filename)
        stimP50= erpn(stimulusTonefile,24, 72, 'max');
        stimN100=erpn(stimulusTonefile,70, 130,'min');
        stimP200=erpn(stimulusTonefile,180,235,'max');
        stimN200=erpn(stimulusTonefile,205,315,'min');
        stimP3a= erpn(stimulusTonefile,325,500,'max');
        stimP3b= erpn(stimulusTonefile,325,580,'max');
        stimSlow=erpn(stimulusTonefile,460,680,'min');
        lstimN200=lat(stimulusTonefile,205,315,'min');
        lstimSlow=lat(stimulusTonefile,460,680,'min');
        lstimP3b= lat(stimulusTonefile,325,580,'max');
        brazilstat_vector=brazilstat(stimulusTonefile);
        %bands_vector =brazilStatMat(bands(stimulusTonefile));

E=[];
tandDat = importdata(stimulusTonefile);
[row,col] = size(tandDat);
for k = 2:col
    FF = tandDat(:,k);
    N = length(FF);
    xdft = fft(FF);
    xdft = xdft(1:N/2+1);
    psdx = (1/(Fs*N)) * abs(xdft).^2;
    psdx(2:end-1) = 2*psdx(2:end-1);
    fftval = psdx';
    E = [E,fftval];
end
        
        %descriptorS = [descriptorS;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,bands_vector,E];
        descriptorS = [descriptorS;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,E];
        %descriptorS = [descriptorS;E];
    end
    
    files1 = dir(fullfile(baseFileName,'*csv.1*'));
    for file = files1'
        filename = file.name;
        targetTonefile=fullfile(baseFileName,filename)
        targP50= erpn(targetTonefile,24, 72, 'max');
        targN100=erpn(targetTonefile,70, 130,'min');
        targP200=erpn(targetTonefile,180,235,'max');
        targN200=erpn(targetTonefile,205,315,'min');
        targP3a= erpn(targetTonefile,325,500,'max');
        targP3b= erpn(targetTonefile,325,580,'max');
        targSlow=erpn(targetTonefile,460,680,'min');
        ltargN200=lat(targetTonefile,205,315,'min');
        ltargSlow=lat(targetTonefile,460,680,'min');
        ltargP3b= lat(targetTonefile,325,580,'max');
        brazilstat_vector=brazilstat(targetTonefile);
        %bands_vector =brazilStatMat(bands(targetTonefile));

E=[];
tandDat = importdata(targetTonefile);
[row,col] = size(tandDat);
for k = 2:col
    FF = tandDat(:,k);
    N = length(FF);
    xdft = fft(FF);
    xdft = xdft(1:N/2+1);
    psdx = (1/(Fs*N)) * abs(xdft).^2;
    psdx(2:end-1) = 2*psdx(2:end-1);
    fftval = psdx';
    E = [E,fftval];
end
        
        %descriptorT = [descriptorT;targP50,targN100,targP200,targN200,targP3a,targP3b,targSlow,ltargN200,ltargSlow,ltargP3b,brazilstat_vector,bands_vector,E];
        descriptorT = [descriptorT;targP50,targN100,targP200,targN200,targP3a,targP3b,targSlow,ltargN200,ltargSlow,ltargP3b,brazilstat_vector,E];
        %descriptorT = [descriptorT;E];
    end
    
    files2 = dir(fullfile(baseFileName,'*csv.2*'));
    for file = files2'
        filename = file.name;
        distractorTonefile=fullfile(baseFileName,filename)
        distP50= erpn(distractorTonefile,24, 72, 'max');
        distN100=erpn(distractorTonefile,70, 130,'min');
        distP200=erpn(distractorTonefile,180,235,'max');
        distN200=erpn(distractorTonefile,205,315,'min');
        distP3a= erpn(distractorTonefile,325,500,'max');
        distP3b= erpn(distractorTonefile,325,580,'max');
        distSlow=erpn(distractorTonefile,460,680,'min');
        ldistN200=lat(distractorTonefile,205,315,'min');
        ldistSlow=lat(distractorTonefile,460,680,'min');
        ldistP3b= lat(distractorTonefile,325,580,'max');
        brazilstat_vector=brazilstat(distractorTonefile);
        %bands_vector =brazilStatMat(bands(distractorTonefile));

E=[];
tandDat = importdata(distractorTonefile);
[row,col] = size(tandDat);
for k = 2:col
    FF = tandDat(:,k);
    N = length(FF);
    xdft = fft(FF);
    xdft = xdft(1:N/2+1);
    psdx = (1/(Fs*N)) * abs(xdft).^2;
    psdx(2:end-1) = 2*psdx(2:end-1);
    fftval = psdx';
    E = [E,fftval];
end
        
        %descriptorD = [descriptorD;distP50, distN100,distP200,distN200,distP3a,distP3b,distSlow,ldistN200,ldistSlow,ldistP3b,brazilstat_vector,bands_vector,E];
        descriptorD = [descriptorD;distP50, distN100,distP200,distN200,distP3a,distP3b,distSlow,ldistN200,ldistSlow,ldistP3b,brazilstat_vector,E];
        %descriptorD = [descriptorD;E];
    end
    
end
cd ..

descriptorA = [descriptorS,descriptorT,descriptorD];
Ind1 = {};
for n = 1:size(descriptorA,1)
    Ind1{n} = '+';
end
Ind1 = string(Ind1);
descriptorA = [descriptorA,Ind1'];




% Labels -----------------
labels = {};
for k = 1:size(descriptorA,2)-1
    labels{k} = strcat('col',num2str(k));
end
labels{size(descriptorA,2)} = 'Indicator';
labels = string(labels);




% Descriptor Matrix ------
descriptor = [descriptorH;descriptorA];
labdesc = [labels;descriptor];
fid=fopen('NNFullFFT.csv','wt');
[rows,cols]=size(labdesc);
for k = 1:rows
    fprintf(fid,'%s,',labdesc{k,1:end-1});
    fprintf(fid,'%s\n',labdesc{k,end});
end
fclose(fid);

