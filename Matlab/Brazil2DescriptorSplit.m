
Fs = 250; 
TotalLength_s = 660; % Total Length of data in seconds
EL = 8; % Epoch Length in seconds

hig  = [];  higS  = 0;
cent = [];  centS = 0;
ent  = [];  entS  = 0;
peak = [];  peakS = 0;
roll = [];  rollS = 0;
slow = [];  slowS = 0;
con  = [];  conS  = 0;
braz = [];  brazS = 0;
pow  = [];  powS  = 0;
domF = [];  domFS = 1;
FFT  = [];  FFTS  = 0;

% HC ---------------------------------------------------------------
cd HCF50_1
dirs = dir(fullfile('.','*.csv'));
descriptorRH=[]; PatNumH = [];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    
    if higS == 1
        hig  = higuchi(filename,EL,TotalLength_s,Fs);
    end
    if centS == 1
        cent = spec_cent(filename,EL);
    end
    if entS == 1
        ent  = spec_ent(filename,EL);
    end
    if peakS == 1
        peak = spec_peak(filename,EL);
    end
    if rollS == 1
        roll = spec_roll(filename,EL,80);
    end
    if slowS == 1
        slow = slowing(filename,EL);
    end
    if conS == 1
        con  = fftConMax(filename,EL);
    end
    if brazS == 1
        braz = brazilstatRest(filename,EL);
    end
    if powS == 1
        pow  = bandpow(filename,EL);
    end
    if domFS == 1
        domF = DomFreq(filename,EL,TotalLength_s,Fs);
    end
    
    if FFTS == 1
        FFT=[];
        Dat = importdata(filename)';
        Dat = Dat(1:Fs*660);
        [row,col] = size(Dat);
        for k = 19
            FF = Dat(:,k);
            N = length(FF);
            xdft = fft(FF);
            xdft = xdft(1:N/2+1);
            psdx = (1/(Fs*N)) * abs(xdft).^2;
            psdx(2:end-1) = 2*psdx(2:end-1);
            fftval = psdx';
            FFT = [FFT,fftval];
        end
    end
    
    descriptorRH=[descriptorRH;hig,cent,ent,peak,roll,slow,con,braz,pow,domF,FFT];
    
    PatNumH = [PatNumH;str2double(filename(3:4))];
end
cd ..

Ind0 = {};
for n = 1:size(descriptorRH,1)
    Ind0{n} = '0';
end
Ind0 = string(Ind0);
descriptorH = [PatNumH,descriptorRH,Ind0'];

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


% AD ---------------------------------------------------------------
cd ADF50_1
dirs = dir(fullfile('.','*.csv'));
descriptorRA=[]; PatNumA = [];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    
    if higS == 1
        hig  = higuchi(filename,EL,TotalLength_s,Fs);
    end
    if centS == 1
        cent = spec_cent(filename,EL);
    end
    if entS == 1
        ent  = spec_ent(filename,EL);
    end
    if peakS == 1
        peak = spec_peak(filename,EL);
    end
    if rollS == 1
        roll = spec_roll(filename,EL,80);
    end
    if slowS == 1
        slow = slowing(filename,EL);
    end
    if conS == 1
        con  = fftConMax(filename,EL);
    end
    if brazS == 1
        braz = brazilstatRest(filename,EL);
    end
    if powS == 1
        pow  = bandpow(filename,EL);
    end
    if domFS == 1
        domF = DomFreq(filename,EL,TotalLength_s,Fs);
    end
    
    if FFTS == 1
        FFT=[];
        Dat = importdata(filename)';
        [row,col] = size(Dat);
        for k = 2:22
            FF = Dat(:,k);
            N = length(FF);
            xdft = fft(FF);
            xdft = xdft(1:N/2+1);
            psdx = (1/(Fs*N)) * abs(xdft).^2;
            psdx(2:end-1) = 2*psdx(2:end-1);
            fftval = psdx';
            FFT = [FFT,fftval];
        end
    end
    
    descriptorRA=[descriptorRA;hig,cent,ent,peak,roll,slow,con,braz,pow,domF,FFT];
    
    PatNumA = [PatNumA;str2double(filename(3:4))+PatNumH(end)];
end
cd ..

Ind1 = {};
for n = 1:size(descriptorRA,1)
    Ind1{n} = '1';
end
Ind1 = string(Ind1);
descriptorA = [PatNumA,descriptorRA,Ind1'];

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


% Labels -----------------------------------------------------------
higlab={}; centlab={}; entlab={}; peaklab={}; rolllab={}; slowlab={}; conlab={}; brazlab={}; powlab={}; fftlab={};

if length(hig) > 1
    for r = 1:21:length(hig)
        for k = 1:21
            higlab{k+(r-1)} = strcat('hig',num2str((r-1)/21+1),'_E',num2str(k));
        end
    end
end
if length(cent) > 1
    for r = 1:21:length(cent)
        for k = 1:21
            centlab{k+(r-1)} = strcat('cent',num2str((r-1)/21+1),'_E',num2str(k));
        end
    end
end
if length(ent) > 1
    for r = 1:21:length(ent)
        for k = 1:21
            entlab{k+(r-1)} = strcat('ent',num2str((r-1)/21+1),'_E',num2str(k));
        end
    end
end
if length(peak) > 1
    for r = 1:21:length(peak)/5
        for k = 1:21
            for p = 1:5
                peaklab{p+5*(k-1)+105*(r-1)/21} = strcat('peak',num2str((r-1)/21+1),'_E',num2str(k),'_B',num2str(p));
            end
        end
    end
end
if length(roll) > 1
    for r = 1:21:length(roll)
        for k = 1:21
            rolllab{k+(r-1)} = strcat('roll',num2str((r-1)/21+1),'_E',num2str(k));
        end
    end
end
if length(slow) > 1
    for r = 1:21:length(slow)
        for k = 1:21
            slowlab{k+(r-1)} = strcat('slow',num2str((r-1)/21+1),'_E',num2str(k));
        end
    end
end
if length(con) > 1
    for r = 1:length(con)
        conlab{r} = strcat('con',num2str(r));
    end
end
if length(braz) > 1
    for r = 1:length(braz)
        brazlab{r} = strcat('braz',num2str(r));
    end
end
if length(pow) > 1
    for r = 1:21:length(pow)/4
        for k = 1:21
            for p = 1:4
                powlab{p+4*(k-1)+84*(r-1)/21} = strcat('pow',num2str((r-1)/21+1),'_E',num2str(k),'_B',num2str(p));
            end
        end
    end
end
if length(FFT) > 1
    for k = 1:size(FFT,2)
        fftlab{k} = strcat('fft',num2str(k));
    end
end

% labels = [higlab,centlab,entlab,peaklab,rolllab,slowlab,conlab,brazlab,powlab,fftlab];
% labels{length(descriptorRH)+1} = 'Indicator';
% labels = string(labels);

labels = {};
for k = 1:size(descriptorRH,2)
    labels{k} = strcat('col',num2str(k));
end
labels{size(descriptorRH,2)+1} = 'Indicator';
labels = string(labels);
labels = ['patient num',labels];


% Descriptor Matrix ------
descriptor = [descriptorH;descriptorA];
labdesc = [labels;descriptor];
fid=fopen('DomFreq_ins25_lp50_ep8.csv','wt');
[rows,cols]=size(labdesc);
for k = 1:rows
    fprintf(fid,'%s,',labdesc{k,1:end-1});
    fprintf(fid,'%s\n',labdesc{k,end});
end
fclose(fid);

