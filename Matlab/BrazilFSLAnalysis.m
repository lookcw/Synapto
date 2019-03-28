%% Delta ---------------------
cd ADDeltaran6
dirs = dir(fullfile('.','*.csv'));
SDA=[]; SDH=[];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    if filename(1) == 'A'
        DelA = importdata(filename);
        SDA = [SDA;DelA];
    elseif filename(1) == 'H'
        DelH = importdata(filename);
        SDH = [SDH;DelH];
    end
end
cd ..
cd HCDeltaran6
dirs = dir(fullfile('.','*.csv'));
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    if filename(1) == 'A'
        DelA = importdata(filename);
        SDA = [SDA;DelA];
    elseif filename(1) == 'H'
        DelH = importdata(filename);
        SDH = [SDH;DelH];
    end
end
cd ..

Ind0 = {};
for n = 1:size(SDH,1)
    Ind0{n} = '-';
end
Ind0 = string(Ind0);
SDelH = [SDH,Ind0'];

Ind1 = {};
for n = 1:size(SDA,1)
    Ind1{n} = '+';
end
Ind1 = string(Ind1);
SDelA = [SDA,Ind1'];

labels = {};
for k = 1:size(SDA,2)
    labels{k} = strcat('col',num2str(k));
end
labels{size(SDA,2)+1} = 'Indicator';
labels = string(labels);

SDel = [SDelH;SDelA];
labdescDel = [labels;SDel];

fid=fopen('DeltaS_ran6.csv','wt');
[rows,cols]=size(labdescDel);
for k = 1:rows
    fprintf(fid,'%s,',labdescDel{k,1:end-1});
    fprintf(fid,'%s\n',labdescDel{k,end});
end
fclose(fid);



%% Theta ---------------------
cd Theta
dirs = dir(fullfile('.','*.csv'));
STA=[]; STH=[];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    if filename(1) == 'A'
        TheA = importdata(filename);
        STA = [STA;(sum(TheA)-21)/210]; % **Avg analysis**
    elseif filename(1) == 'H'
        TheH = importdata(filename);
        STH = [STH;(sum(TheH)-21)/210];
    end
end
cd ..

STheH = [STH,Ind0'];
STheA = [STA,Ind1'];

SThe = [STheH;STheA];
labdescThe = [labels;SThe];

% fid=fopen('ThetaS.csv','wt');
% [rows,cols]=size(labdescThe);
% for k = 1:rows
%     fprintf(fid,'%s,',labdescThe{k,1:end-1});
%     fprintf(fid,'%s\n',labdescThe{k,end});
% end
% fclose(fid);



%% Alpha ---------------------
cd Alpha
dirs = dir(fullfile('.','*.csv'));
SAA=[]; SAH=[];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    if filename(1) == 'A'
        AlpA = importdata(filename);
        SAA = [SAA;(sum(AlpA)-21)/2];
    elseif filename(1) == 'H'
        AlpH = importdata(filename);
        SAH = [SAH;(sum(AlpH)-21)/2];
    end
end
cd ..

SAlpH = [SAH,Ind0'];
SAlpA = [SAA,Ind1'];

SAlp = [SAlpH;SAlpA];
labdescAlp = [labels;SAlp];

% fid=fopen('AlphaS.csv','wt');
% [rows,cols]=size(labdescAlp);
% for k = 1:rows
%     fprintf(fid,'%s,',labdescAlp{k,1:end-1});
%     fprintf(fid,'%s\n',labdescAlp{k,end});
% end
% fclose(fid);



%% Beta ---------------------
cd Beta
dirs = dir(fullfile('.','*.csv'));
SBA=[]; SBH=[];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    if filename(1) == 'A'
        BetA = importdata(filename);
        SBA = [SBA;(sum(BetA)-21)/2];
    elseif filename(1) == 'H'
        BetH = importdata(filename);
        SBH = [SBH;(sum(BetH)-21)/2];
    end
end
cd ..

SBetH = [SBH,Ind0'];
SBetA = [SBA,Ind1'];

SBet = [SBetH;SBetA];
labdescBet = [labels;SBet];

% fid=fopen('BetaS.csv','wt');
% [rows,cols]=size(labdescBet);
% for k = 1:rows
%     fprintf(fid,'%s,',labdescBet{k,1:end-1});
%     fprintf(fid,'%s\n',labdescBet{k,end});
% end
% fclose(fid);



%% Gamma ---------------------
cd Gamma
dirs = dir(fullfile('.','*.csv'));
SGA=[]; SGH=[];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    if filename(1) == 'A'
        GamA = importdata(filename);
        SGA = [SGA;(sum(GamA)-21)/2];
    elseif filename(1) == 'H'
        GamH = importdata(filename);
        SGH = [SGH;(sum(GamH)-21)/2];
    end
end
cd ..

SGamH = [SGH,Ind0'];
SGamA = [SGA,Ind1'];

SGam = [SGamH;SGamA];
labdescGam = [labels;SGam];

% fid=fopen('GammaS.csv','wt');
% [rows,cols]=size(labdescGam);
% for k = 1:rows
%     fprintf(fid,'%s,',labdescGam{k,1:end-1});
%     fprintf(fid,'%s\n',labdescGam{k,end});
% end
% fclose(fid);



%% All_bands ---------------------
cd all_bands
dirs = dir(fullfile('.','*.csv'));
SABA=[]; SABH=[];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    if filename(1) == 'A'
        AllA = importdata(filename);
        SABA = [SABA;(sum(AllA)-21)/2];
    elseif filename(1) == 'H'
        AllH = importdata(filename);
        SABH = [SABH;(sum(AllH)-21)/2];
    end
end
cd ..

SAllH = [SABH,Ind0'];
SAllA = [SABA,Ind1'];

SAll = [SAllH;SAllA];
labdescAll = [labels;SAll];

% fid=fopen('AllS.csv','wt');
% [rows,cols]=size(labdescAll);
% for k = 1:rows
%     fprintf(fid,'%s,',labdescAll{k,1:end-1});
%     fprintf(fid,'%s\n',labdescAll{k,end});
% end
% fclose(fid);



%% All ---------------------
SH = [SDH,STH,SAH,SBH,SGH,Ind0'];
SA = [SDA,STA,SAA,SBA,SGA,Ind1'];
labels = {};
for k = 1:size(SA,2)-1
    labels{k} = strcat('col',num2str(k));
end
labels{size(SA,2)} = 'Indicator';
labels = string(labels);
labdesc = [labels;SH;SA];

fid=fopen('AllSum.csv','wt');
[rows,cols]=size(labdesc);
for k = 1:rows
    fprintf(fid,'%s,',labdesc{k,1:end-1});
    fprintf(fid,'%s\n',labdesc{k,end});
end
fclose(fid);