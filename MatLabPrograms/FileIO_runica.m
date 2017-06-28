cd ..\HC_csv
 dirs = dir(fullfile('.','*.xlsx'));
    for  direc =dirs'
    delimiterIn = ',';
    baseFileName=direc.name
    files0 = dir(fullfile(baseFileName,'*csv.0*'));
    descriptor=[];
    for file = files0'
        filename = file.name;
        stimulusTonefile=fullfile(baseFileName,filename)
        A= importdata(stimulusTonefile)
        cleanData= artrem(A.');
        dlmwrite(strcat('../cleaned_data_AD/',stimulusTonefile),cleanData,'delimiter',',','-write');
    end
        files1 = dir(fullfile(baseFileName,'*csv.1*'));
    for file = files1'
        filename = file.name;
        targetTonefile=fullfile(baseFileName,filename);
        cleanData = artrem(importdata(targetTonefile));
        dlmwrite(strcat('../cleaned_data_AD/',targetTonefile),cleanData,'delimiter',',','-write');
        
    end
        files2 = dir(fullfile(baseFileName,'*csv.2*'));
    for file = files2'
        filename = file.name;
        distractorTonefile=fullfile(baseFileName,filename)
        cleanData = artrem(importdata(distractorTonefile));
        dlmwrite(strcat('../cleaned_data_AD/',targetTonefile),cleanData,'delimiter',',','-write');
        
    end
    	
    end
cd ..\MatLabPrograms


cd ..\HC_csv
 dirs = dir(fullfile('.','*.xlsx'));
    for  direc =dirs'
    delimiterIn = ',';
    baseFileName=direc.name
    files0 = dir(fullfile(baseFileName,'*csv.0*'));
    descriptor=[];
    for file = files0'
        filename = file.name;
        stimulusTonefile=fullfile(baseFileName,filename)
        cleanData= artrem(importdata(stimulusTonefile));
        dlmwrite(strcat('../cleaned_data_HC/',targetTonefile),cleanData,'delimiter',',','-write');
    end
        files1 = dir(fullfile(baseFileName,'*csv.1*'));
    for file = files1'
        filename = file.name;
        targetTonefile=fullfile(baseFileName,filename);
        cleanData = artrem(importdata(targetTonefile));
        dlmwrite(strcat('../cleaned_data_HC/',targetTonefile),cleanData,'delimiter',',','-write');
    end
        files2 = dir(fullfile(baseFileName,'*csv.2*'));
    for file = files2'
        filename = file.name;
        distractorTonefile=fullfile(baseFileName,filename)
        cleanData = artrem(importdata(distractorTonefile));
        dlmwrite(strcat('../cleaned_data_HC/',targetTonefile),cleanData,'delimiter',',','-write');
    end
    end
    cd ..\MatlabPrograms