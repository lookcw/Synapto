  cd ..\AD_csv

  %%fileID = fopen('exp.txt','a');
   %e=exist('B','var')
   
   %if exist('TestAnalysis','var')~= 1
   	%TestAnalysis = importdata('TestAnalysis.txt');
    %TestAnalysis = B(1:52392 , 1:9);
  % end
 dirs = dir(fullfile('.','*.xlsx'));
    for  direc =dirs'
    delimiterIn = ',';
    baseFileName=direc.name
    files0 = dir(fullfile(baseFileName,'*csv.0*'));
    for file = files0'
        filename = file.name;
        targetToneFile=fullfile(baseFileName,filename)
        %TestAnalysis = importdata(targetToneFile);
    end
        files1 = dir(fullfile(baseFileName,'*csv.1*'));
    for file = files1'
        filename = file.name;
        unexpectedToneFile=fullfile(baseFileName,filename)
        %TestAnalysis = importdata(targetToneFile);
    end
        files2 = dir(fullfile(baseFileName,'*csv.2*'));
    for file = files2'
        filename = file.name;
        standardToneFile=fullfile(baseFileName,filename)
        %TestAnalysis = importdata(targetToneFile);
    end
  %  dlmwrite('myFile.txt',A,'newline','pc')
   % A=A(1:52392,1:9)
    end
cd ..\MatLabPrograms

