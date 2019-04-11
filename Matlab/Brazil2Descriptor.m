
Fs = 250; 
TotalLength_s = 660; % Total Length of data in seconds
EL = 8; % Epoch Length in seconds
%FPz=2; Oz=20; F3=6; P3=16; F4=8; P4=18; % (for convolution)
hig=[]; cent=[]; ent=[]; peak=[]; roll=[]; slow=[]; con=[]; braz=[]; pow=[]; FFT=[];

% HC ---------------------
cd HCF50_1
dirs = dir(fullfile('.','*.csv'));
descriptorRH=[];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    hig  = higuchi(filename,EL,TotalLength_s,Fs);
    %cent = spec_cent(filename,EL);
    %ent  = spec_ent(filename,EL);
    %peak = spec_peak(filename,EL);
    %roll = spec_roll(filename,EL,80);
    %slow = slowing(filename,EL);
    %con  = fftConMax(filename,EL);
    %braz = brazilstatRest(filename,EL);
    %pow  = bandpow(filename,EL);
    %domF = DomFreq(filename,EL,TotalLength_s,Fs);
    
% FFT=[];
% Dat = importdata(filename)';
% Dat = Dat(1:Fs*660);
% [row,col] = size(Dat);
% for k = 19
%     FF = Dat(:,k);
%     N = length(FF);
%     xdft = fft(FF);
%     xdft = xdft(1:N/2+1);
%     psdx = (1/(Fs*N)) * abs(xdft).^2;
%     psdx(2:end-1) = 2*psdx(2:end-1);
%     fftval = psdx';
%     FFT = [FFT,fftval];
% end
    
    %descriptorRH=[descriptorRH;hig,cent,ent,peak,roll,slow,FFT]; %,con];
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


% AD ---------------------
cd ADF50_1
dirs = dir(fullfile('.','*.csv'));
descriptorRA=[];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    hig  = higuchi(filename,EL,TotalLength_s,Fs);
    %cent = spec_cent(filename,EL);
    %ent  = spec_ent(filename,EL);
    %peak = spec_peak(filename,EL);
    %roll = spec_roll(filename,EL,80);
    %slow = slowing(filename,EL);
    %con  = fftConMax(filename,EL);
    %braz = brazilstatRest(filename,EL);
    %pow  = bandpow(filename,EL);
    %domF = DomFreq(filename,EL,TotalLength_s,Fs);
    
% FFT=[];
% Dat = importdata(filename)';
% [row,col] = size(Dat);
% for k = 2:22
%     FF = Dat(:,k);
%     N = length(FF);
%     xdft = fft(FF);
%     xdft = xdft(1:N/2+1);
%     psdx = (1/(Fs*N)) * abs(xdft).^2;
%     psdx(2:end-1) = 2*psdx(2:end-1);
%     fftval = psdx';
%     FFT = [FFT,fftval];
% end
    
    %descriptorRA=[descriptorRA;hig,cent,ent,peak,roll,slow,FFT]; %,con];
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


% Labels -----------------
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


% Descriptor Matrix ------
descriptor = [descriptorH;descriptorA];
labdesc = [labels;descriptor];
fid=fopen('Test.csv','wt');
[rows,cols]=size(labdesc);
for k = 1:rows
    fprintf(fid,'%s,',labdesc{k,1:end-1});
    fprintf(fid,'%s\n',labdesc{k,end});
end
fclose(fid);

