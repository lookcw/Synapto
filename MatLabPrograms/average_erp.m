cd ..\AD_full_csv
dirs = dir(fullfile('.','*.xlsx'));
A = [];
B = [];
C = [];
D = [];
E = [];
F = [];
G = [];
H = [];
I = [];
J = [];
K = [];
L = [];

    for  direc =dirs'
    baseFileName=direc.name
    files0 = dir(fullfile(baseFileName,'*csv.0*'));
    files1 = dir(fullfile(baseFileName,'*csv.1*'));
    files2 = dir(fullfile(baseFileName,'*csv.2*'));
    
    try
        for file = files0'
        filename = file.name;
        stimulusTonefile=fullfile(baseFileName,filename)
        stimP50= erp(stimulusTonefile,24,72,'max');
        stimN100=erp(stimulusTonefile,70,130,'min');
        stimP200=erp(stimulusTonefile,180,235,'max');
        end
        
        for file = files1'
        filename = file.name;
        targetTonefile=fullfile(baseFileName,filename)
        targP50= erp(targetTonefile,24,72,'max');
        targN100=erp(targetTonefile,70,130,'min');
        targP200=erp(targetTonefile,180,235,'max');
        targN200=erp(targetTonefile,205,315,'min');
        targP3b= erp(targetTonefile,325,580,'max');
        targSlow=erp(targetTonefile,460,680,'min');
        end

        for file = files2'
        filename = file.name;
        distractorTonefile=fullfile(baseFileName,filename)
        distP50= erp(distractorTonefile,24,72,'max');
        distN100=erp(distractorTonefile,70,130,'min');
        distP3a= erp(distractorTonefile,325,500,'max');
        end
        
        catch
        stimP50=[]
        stimN100=[]
        stimP200=[]
        targP50=[]
        targN100=[]
        targP200=[]
        targN200=[]
        targP3b=[]
        targSlow=[]
        distP50=[]
        distN100=[]
        distP3a=[]
    end
    
         A = [A stimP50];
         B = [B stimN100];
         C = [C stimP200];
         D = [D targP50];
         E = [E targN100];
         F = [F targP200];
         G = [G targN200];
         H = [H targP3b];
         I = [I targSlow];
         J = [J distP50];
         K = [K distN100];
         L = [L distP3a];
    end
    
    avg_sP50 = mean(A)
    avg_sN100 = mean(B)
    avg_sP200 = mean(C)
    
    avg_tP50 = mean(D)
    avg_tN100 = mean(E)
    avg_tP200 = mean(F)
    avg_tN200 = mean(G)
    avg_tP3b = mean(H)
    avg_tSlow = mean(I)
    
    avg_dP50 = mean(J)
    avg_dN100 = mean(K)
    avg_dP3a = mean(L)
