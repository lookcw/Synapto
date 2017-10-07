% Must start in a folder containing 'HC_BD' and 'AD_BD'

 EL = 8; % Epoch Length in seconds
 FPz=2; Oz=20; F3=6; P3=16; F4=8; P4=18; % (for convolution)
 
% HC -----------------
cd HC_BD
 dirs  = dir(fullfile('.','*.txt'));
    descriptorRH=[];
    for file = dirs'
        filename = file.name;
        filename=fullfile(filename)
        hig  = higuchi(filename,EL);
        cent = spec_cent(filename,EL);
        ent  = spec_ent(filename,EL);
        peak = spec_peak(filename,EL);
        roll = spec_roll(filename,EL,80);
        conFBc  = fftConMax(filename,EL,FPz,Oz);
        conFBl  = fftConMax(filename,EL,F3,P3);
        conFBr  = fftConMax(filename,EL,F4,P4);
        conFrBl = fftConMax(filename,EL,F4,P3);
        conFlBr = fftConMax(filename,EL,F3,P4);
        conBlBr = fftConMax(filename,EL,P3,P4);
        conFlFr = fftConMax(filename,EL,F3,F4);
        
        descriptorRH=[descriptorRH;hig,cent,ent,peak,roll,conFBc,conFBl,conFBr,conFrBl,conFlBr,conBlBr,conFlFr];
    end

  cd ..
    Ind0 = zeros(length(dirs),1);
    descriptorH = [descriptorRH,Ind0];
    %dlmwrite('BrazilHC.csv',descriptorH,'delimiter',',','-append'); %for HC only output file


% AD -----------------
cd AD_BD
 dirs  = dir(fullfile('.','*.txt'));
    descriptorRA=[];
    for file = dirs'
        filename = file.name;
        filename=fullfile(filename)
        hig  = higuchi(filename,EL);
        cent = spec_cent(filename,EL);
        ent  = spec_ent(filename,EL);
        peak = spec_peak(filename,EL);
        roll = spec_roll(filename,EL,80);
        conFBc  = fftConMax(filename,EL,FPz,Oz);
        conFBl  = fftConMax(filename,EL,F3,P3);
        conFBr  = fftConMax(filename,EL,F4,P4);
        conFrBl = fftConMax(filename,EL,F4,P3);
        conFlBr = fftConMax(filename,EL,F3,P4);
        conBlBr = fftConMax(filename,EL,P3,P4);
        conFlFr = fftConMax(filename,EL,F3,F4);
        
        descriptorRA=[descriptorRA;hig,cent,ent,peak,roll,conFBc,conFBl,conFBr,conFrBl,conFlBr,conBlBr,conFlFr];
    end
    
  cd ..
    Ind1 = zeros(length(dirs),1)+1;
    descriptorA = [descriptorRA,Ind1];
    %dlmwrite('BrazilAD.csv',descriptorA,'delimiter',',','-append'); %for AD only output file
    
    descriptor = [descriptorH;descriptorA];
    dlmwrite('Brazil_UF.csv',descriptor,'delimiter',',','-append');


