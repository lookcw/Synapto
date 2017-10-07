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
        stimP50= erp(stimulusTonefile,24,72,'max');
        stimN100=erp(stimulusTonefile,70,130,'min');
        stimP200=erp(stimulusTonefile,180,235,'max');
        stimN200=erp(stimulusTonefile,205,315,'min');
        stimP3a= erp(stimulusTonefile,325,500,'max');
        stimP3b= erp(stimulusTonefile,325,580,'max');
        stimSlow=erp(stimulusTonefile,460,680,'min');
        lstimN200=lat(stimulusTonefile,205,315,'n200');
        lstimSlow=lat(stimulusTonefile,460,680,'slow');
        lstimP3b= lat(stimulusTonefile,325,580,'p3b');
        brazilstat_vector=brazilstat(stimulusTonefile);
        bands_vector =brazilStatMat(bands(stimulusTonefile));

        descriptor=[ stimP50,stimN100, stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,bands_vector];
    end
        files1 = dir(fullfile(baseFileName,'*csv.1*'));
    for file = files1'
        filename = file.name;
        targetTonefile=fullfile(baseFileName,filename)
        targP50= erp(targetTonefile,24,72,'max');
        targN100=erp(targetTonefile,70,130,'min');
        targP200=erp(targetTonefile,180,235,'max');
        targN200=erp(targetTonefile,205,315,'min');
        targP3a= erp(targetTonefile,325,500,'max');
        targP3b= erp(targetTonefile,325,580,'max');
        targSlow=erp(targetTonefile,460,680,'min');
        ltargN200=lat(targetTonefile,205,315,'n200');
        ltargSlow=lat(targetTonefile,460,680,'slow');
        ltargP3b= lat(targetTonefile,325,580,'p3b');
         brazilstat_vector=brazilstat(targetTonefile);
        bands_vector =brazilStatMat(bands(targetTonefile));

         
        descriptor=[descriptor,targP50, targN100,targP200,targN200,targP3a,targP3b,targSlow,ltargN200,ltargSlow,ltargP3b,brazilstat_vector,bands_vector];
      %  descriptor=[descriptor,ltargN200,ltargSlow,ltarglstimp3b,brazilstat_vector];
    end
        files2 = dir(fullfile(baseFileName,'*csv.2*'));
    for file = files2'
        filename = file.name;
        distractorTonefile=fullfile(baseFileName,filename)
        distP50= erp(distractorTonefile,24,72,'max');
        distN100=erp(distractorTonefile,70,130,'min');
        distP200=erp(distractorTonefile,180,235,'max');
        distN200=erp(distractorTonefile,205,315,'min');
        distP3a= erp(distractorTonefile,325,500,'max');
        distP3b= erp(distractorTonefile,325,580,'max');
        distSlow=erp(distractorTonefile,460,680,'min');
        ldistN200=lat(distractorTonefile,205,315,'n200');
        ldistSlow=lat(distractorTonefile,460,680,'slow');
        ldistP3b= lat(distractorTonefile,325,580,'p3b');
         brazilstat_vector=brazilstat(distractorTonefile);
        bands_vector =brazilStatMat(bands(distractorTonefile));

       descriptor=[descriptor,distP50, distN100,distP200,distN200,distP3a,distP3b,distSlow,ldistN200,ldistSlow,ldistP3b,brazilstat_vector,bands_vector];
           %descriptor=[descriptor,ldistN200,ldistSlow,ldistlstimp3b,brazilstat_vector];
        
    end
    descriptor=[descriptor,0];
    dlmwrite('..\brazil_erp_7.csv',descriptor,'delimiter',',','-append');
    end
cd ..\MatLabPrograms

cd ..\AD_csv
 dirs = dir(fullfile('.','*.xlsx'));
    for  direc =dirs'
    delimiterIn = ',';
    baseFileName=direc.name
    files0 = dir(fullfile(baseFileName,'*csv.0*'));
    descriptor=[];
    for file = files0'
        filename = file.name;
        stimulusTonefile=fullfile(baseFileName,filename)
        stimP50= erp(stimulusTonefile,24,72,'max');
        stimN100=erp(stimulusTonefile,70,130,'min');
        stimP200=erp(stimulusTonefile,180,235,'max');
        stimN200=erp(stimulusTonefile,205,315,'min');
        stimP3a= erp(stimulusTonefile,325,500,'max');
        stimP3b= erp(stimulusTonefile,325,580,'max');
        stimSlow=erp(stimulusTonefile,460,680,'min');
        lstimN200=lat(stimulusTonefile,205,315,'n200');
        lstimSlow=lat(stimulusTonefile,460,680,'slow');
        lstimP3b= lat(stimulusTonefile,325,580,'p3b');
        brazilstat_vector=brazilstat(stimulusTonefile);
        bands_vector =brazilStatMat(bands(stimulusTonefile));

         descriptor=[ stimP50,stimN100, stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,bands_vector];
    end
        files1 = dir(fullfile(baseFileName,'*csv.1*'));
    for file = files1'
        filename = file.name;
        targetTonefile=fullfile(baseFileName,filename)
        targP50= erp(targetTonefile,24,72,'max');
        targN100=erp(targetTonefile,70,130,'min');
        targP200=erp(targetTonefile,180,235,'max');
        targN200=erp(targetTonefile,205,315,'min');
        targP3a= erp(targetTonefile,325,500,'max');
        targP3b= erp(targetTonefile,325,580,'max');
        targSlow=erp(targetTonefile,460,680,'min');
        ltargN200=lat(targetTonefile,205,315,'n200');
        ltargSlow=lat(targetTonefile,460,680,'slow');
        ltargP3b= lat(targetTonefile,325,580,'p3b');
        brazilstat_vector=brazilstat(targetTonefile);
        bands_vector =brazilStatMat(bands(targetTonefile));

        descriptor=[descriptor,targP50, targN100,targP200,targN200,targP3a,targP3b,targSlow,ltargN200,ltargSlow,ltargP3b,brazilstat_vector,bands_vector];
        %descriptor=[descriptor,ltargN200,ltargSlow,ltarglstimp3b,brazilstat_vector];
    end
        files2 = dir(fullfile(baseFileName,'*csv.2*'));
    for file = files2'
        filename = file.name;
        distractorTonefile=fullfile(baseFileName,filename)
        distP50= erp(distractorTonefile,24,72,'max');
        distN100=erp(distractorTonefile,70,130,'min');
        distP200=erp(distractorTonefile,180,235,'max');
        distN200=erp(distractorTonefile,205,315,'min');
        distP3a= erp(distractorTonefile,325,500,'max');
        distP3b= erp(distractorTonefile,325,580,'max');
        distSlow=erp(distractorTonefile,460,680,'min');
        ldistN200=lat(distractorTonefile,205,315,'n200');
        ldistSlow=lat(distractorTonefile,460,680,'slow');
        ldistP3b= lat(distractorTonefile,325,580,'p3b');
        brazilstat_vector=brazilstat(distractorTonefile);
        bands_vector =brazilStatMat(bands(distractorTonefile));

       descriptor=[descriptor,distP50, distN100,distP200,distN200,distP3a,distP3b,distSlow,ldistN200,ldistSlow,ldistP3b,brazilstat_vector,bands_vector];
       %descriptor=[descriptor,ldistN200,ldistSlow,ldistlstimp3b,brazilstat_vector];
        
    end
    descriptor=[descriptor,1];
    dlmwrite('..\brazil_erp_7.csv',descriptor,'delimiter',',','-append');
    end
cd ..\MatLabPrograms




