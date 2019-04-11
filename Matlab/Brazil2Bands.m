
% HC ---------------------
cd HCF50ran6
dirs = dir(fullfile('.','*.csv'));
x = 1;
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    [delta,theta,alpha,beta,gamma] = bands2(filename);
    
    nf = extractAfter(filename,'lp');
    if length(nf) > 8
        n = nf(1:2);
    elseif length(nf) <= 8
        n = strcat('0',nf(1));
    end
    
    cd ..
    cd HCDeltaran6
    dlmwrite(strcat('HC_Deltaran6',n,'.csv'),delta);
    cd ..
    cd HCThetaran6
    dlmwrite(strcat('HC_Thetaran6',n,'.csv'),theta);
    cd ..
    cd HCAlpharan6
    dlmwrite(strcat('HC_Alpharan6',n,'.csv'),alpha);
    cd ..
    cd HCBetaran6
    dlmwrite(strcat('HC_Betaran6', n,'.csv'),beta);
    cd ..
    cd HCGammaran6
    dlmwrite(strcat('HC_Gammaran6',n,'.csv'),gamma);
    cd ..
    cd HCF50ran6
    
    x = x+1;
end
cd ..



% AD ---------------------
cd ADF50ran6
dirs = dir(fullfile('.','*.csv'));
x = 1;
for file = dirs'
    filename = file.name;
    filename=fullfile(filename)
    [delta,theta,alpha,beta,gamma] = bands2(filename);
    
    nf = extractAfter(filename,'lp');
    if length(nf) > 8
        n = nf(1:2);
    elseif length(nf) <= 8
        n = strcat('0',nf(1));
    end
    
    cd ..
    cd ADDeltaran6
    dlmwrite(strcat('AD_Deltaran6',n,'.csv'),delta);
    cd ..
    cd ADThetaran6
    dlmwrite(strcat('AD_Thetaran6',n,'.csv'),theta);
    cd ..
    cd ADAlpharan6
    dlmwrite(strcat('AD_Alpharan6',n,'.csv'),alpha);
    cd ..
    cd ADBetaran6
    dlmwrite(strcat('AD_Betaran6', n,'.csv'),beta);
    cd ..
    cd ADGammaran6
    dlmwrite(strcat('AD_Gammaran6',n,'.csv'),gamma);
    cd ..
    cd ADF50ran6
    
    x = x+1;
end
cd ..
