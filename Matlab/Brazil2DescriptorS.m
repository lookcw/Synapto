
%% Delta ---------------------
cd Delta11
dirs = dir(fullfile('.','*.csv'));
descriptorDA=[]; descriptorDH=[];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    if filename(1) == 'A'
        delA = importdata(filename);
        descriptorDA = [descriptorDA;delA];
    elseif filename(1) == 'H'
        delH = importdata(filename);
        descriptorDH = [descriptorDH;delH];
    end
end
cd ..

Ind0 = {};
for n = 1:size(descriptorDH,1)
    Ind0{n} = '-';
end
Ind0 = string(Ind0);
descriptorDelH = [descriptorDH,Ind0'];

Ind1 = {};
for n = 1:size(descriptorDA,1)
    Ind1{n} = '+';
end
Ind1 = string(Ind1);
descriptorDelA = [descriptorDA,Ind1'];

labels = {};
for k = 1:size(descriptorDA,2)
    labels{k} = strcat('col',num2str(k));
end
labels{size(descriptorDA,2)+1} = 'Indicator';
labels = string(labels);

descriptorDel = [descriptorDelH;descriptorDelA];
labdescDel = [labels;descriptorDel];

fid=fopen('DeltaS11.csv','wt');
[rows,cols]=size(labdescDel);
for k = 1:rows
    fprintf(fid,'%s,',labdescDel{k,1:end-1});
    fprintf(fid,'%s\n',labdescDel{k,end});
end
fclose(fid);



%% Theta ---------------------
cd Theta11
dirs = dir(fullfile('.','*.csv'));
descriptorTA=[]; descriptorTH=[];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    if filename(1) == 'A'
        TheA = importdata(filename);
        descriptorTA = [descriptorTA;TheA];
    elseif filename(1) == 'H'
        TheH = importdata(filename);
        descriptorTH = [descriptorTH;TheH];
    end
end
cd ..

descriptorTheH = [descriptorTH,Ind0'];
descriptorTheA = [descriptorTA,Ind1'];

descriptorThe = [descriptorTheH;descriptorTheA];
labdescThe = [labels;descriptorThe];

fid=fopen('ThetaS11.csv','wt');
[rows,cols]=size(labdescThe);
for k = 1:rows
    fprintf(fid,'%s,',labdescThe{k,1:end-1});
    fprintf(fid,'%s\n',labdescThe{k,end});
end
fclose(fid);



%% Alpha ---------------------
cd Alpha11
dirs = dir(fullfile('.','*.csv'));
descriptorAA=[]; descriptorAH=[];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    if filename(1) == 'A'
        AlpA = importdata(filename);
        descriptorAA = [descriptorAA;AlpA];
    elseif filename(1) == 'H'
        AlpH = importdata(filename);
        descriptorAH = [descriptorAH;AlpH];
    end
end
cd ..

descriptorAlpH = [descriptorAH,Ind0'];
descriptorAlpA = [descriptorAA,Ind1'];

descriptorAlp = [descriptorAlpH;descriptorAlpA];
labdescAlp = [labels;descriptorAlp];

fid=fopen('AlphaS11.csv','wt');
[rows,cols]=size(labdescAlp);
for k = 1:rows
    fprintf(fid,'%s,',labdescAlp{k,1:end-1});
    fprintf(fid,'%s\n',labdescAlp{k,end});
end
fclose(fid);



%% Beta ---------------------
cd Beta11
dirs = dir(fullfile('.','*.csv'));
descriptorBA=[]; descriptorBH=[];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    if filename(1) == 'A'
        BetA = importdata(filename);
        descriptorBA = [descriptorBA;BetA];
    elseif filename(1) == 'H'
        BetH = importdata(filename);
        descriptorBH = [descriptorBH;BetH];
    end
end
cd ..

descriptorBetH = [descriptorBH,Ind0'];
descriptorBetA = [descriptorBA,Ind1'];

descriptorBet = [descriptorBetH;descriptorBetA];
labdescBet = [labels;descriptorBet];

fid=fopen('BetaS11.csv','wt');
[rows,cols]=size(labdescBet);
for k = 1:rows
    fprintf(fid,'%s,',labdescBet{k,1:end-1});
    fprintf(fid,'%s\n',labdescBet{k,end});
end
fclose(fid);



%% Gamma ---------------------
cd Gamma11
dirs = dir(fullfile('.','*.csv'));
descriptorGA=[]; descriptorGH=[];
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    if filename(1) == 'A'
        GamA = importdata(filename);
        descriptorGA = [descriptorGA;GamA];
    elseif filename(1) == 'H'
        GamH = importdata(filename);
        descriptorGH = [descriptorGH;GamH];
    end
end
cd ..

descriptorGamH = [descriptorGH,Ind0'];
descriptorGamA = [descriptorGA,Ind1'];

descriptorGam = [descriptorGamH;descriptorGamA];
labdescGam = [labels;descriptorGam];

fid=fopen('GammaS11.csv','wt');
[rows,cols]=size(labdescGam);
for k = 1:rows
    fprintf(fid,'%s,',labdescGam{k,1:end-1});
    fprintf(fid,'%s\n',labdescGam{k,end});
end
fclose(fid);



%% All_bands ---------------------
% cd all_bands
% dirs = dir(fullfile('.','*.csv'));
% descriptorABA=[]; descriptorABH=[];
% for file = dirs'
%     filename = file.name;
%     filename=fullfile(filename)
%     if filename(1) == 'A'
%         AllA = importdata(filename);
%         descriptorABA = [descriptorABA;AllA];
%     elseif filename(1) == 'H'
%         AllH = importdata(filename);
%         descriptorABH = [descriptorABH;AllH];
%     end
% end
% cd ..
% 
% descriptorAllH = [descriptorABH,Ind0'];
% descriptorAllA = [descriptorABA,Ind1'];
% 
% descriptorAll = [descriptorAllH;descriptorAllA];
% labdescAll = [labels;descriptorAll];
% 
% fid=fopen('AllS11.csv','wt');
% [rows,cols]=size(labdescAll);
% for k = 1:rows
%     fprintf(fid,'%s,',labdescAll{k,1:end-1});
%     fprintf(fid,'%s\n',labdescAll{k,end});
% end
% fclose(fid);
% 
% 

%% All ---------------------
descriptorH = [descriptorDH,descriptorTH,descriptorAH,descriptorBH,descriptorGH,Ind0'];
descriptorA = [descriptorDA,descriptorTA,descriptorAA,descriptorBA,descriptorGA,Ind1'];
labels = {};
for k = 1:size(descriptorA,2)-1
    labels{k} = strcat('col',num2str(k));
end
labels{size(descriptorA,2)} = 'Indicator';
labels = string(labels);
labdesc = [labels;descriptorH;descriptorA];

fid=fopen('CombS11.csv','wt');
[rows,cols]=size(labdesc);
for k = 1:rows
    fprintf(fid,'%s,',labdesc{k,1:end-1});
    fprintf(fid,'%s\n',labdesc{k,end});
end
fclose(fid);

