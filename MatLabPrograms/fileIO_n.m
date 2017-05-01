


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
        stimP50= erp1(stimulusTonefile,24,72,'max');
        stimN100=erp1(stimulusTonefile,70,130,'min')-stimP50;
        stimP200=erp1(stimulusTonefile,180,235,'max')-stimP50;
        stimN200=erp1(stimulusTonefile,205,315,'min')-stimP50;
        stimP3a= erp(stimulusTonefile,325,500,'max')-stimP50;
        stimP3b= erp1(stimulusTonefile,325,580,'max')-stimP50;
        stimSlow=erp1(stimulusTonefile,460,680,'min')-stimP50;
        lstimN200=lat(stimulusTonefile,205,315,'n200');
        lstimSlow=lat(stimulusTonefile,460,680,'slow');
        lstimP3b= lat(stimulusTonefile,325,580,'p3b');
        descriptor=[stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimN200,lstimSlow,lstimP3b];
    end
        files1 = dir(fullfile(baseFileName,'*csv.1*'));
    for file = files1'
        filename = file.name;
        targetTonefile=fullfile(baseFileName,filename)
        targP50= erp1(targetTonefile,24,72,'max');
        targN100=erp1(targetTonefile,70,130,'min')-targP50;
        targP200=erp1(targetTonefile,180,235,'max')-targP50;
        targN200=erp1(targetTonefile,205,315,'min')-targP50;
        targP3a= erp1(targetTonefile,325,500,'max')-targP50;
        targP3b= erp1(targetTonefile,325,580,'max')-targP50;
        targSlow=erp1(targetTonefile,460,680,'min')-targP50;
        ltargN200=lat(targetTonefile,205,315,'n200');
        ltargSlow=lat(targetTonefile,460,680,'slow');
        ltargP3b= lat(targetTonefile,325,580,'p3b');
        %TestAnalysis = importdata(targetToneFile);
        descriptor=[descriptor, targN100,targP200,targN200,targP3a,targP3b,targSlow,ltargN200,ltargSlow,ltargP3b];
    end
        files2 = dir(fullfile(baseFileName,'*csv.2*'));
    for file = files2'
        filename = file.name;
        distractorTonefile=fullfile(baseFileName,filename)
        distP50= erp1(distractorTonefile,24,72,'max');
        distN100=erp1(distractorTonefile,70,130,'min')-distP50;
        distP200=erp1(distractorTonefile,180,235,'max')-distP50;
        distN200=erp1(distractorTonefile,205,315,'min')-distP50;
        distP3a= erp1(distractorTonefile,325,500,'max')-distP50;
        distP3b= erp1(distractorTonefile,325,580,'max')-distP50;
        distSlow=erp1(distractorTonefile,460,680,'min')-distP50;
        ldistN200=lat(distractorTonefile,205,315,'n200');
        ldistSlow=lat(distractorTonefile,460,680,'slow');
        ldistP3b= lat(distractorTonefile,325,580,'p3b');
        descriptor=[descriptor, distN100,distP200,distN200,distP3a,distP3b,distSlow,ldistN200,ldistSlow,ldistP3b];
        
    end
    descriptor=[descriptor,0];
    dlmwrite('..\test1.csv',descriptor,'delimiter',',','-append');
    end
cd ..\MatLabPrograms
