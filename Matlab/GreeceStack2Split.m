EpLen = 301; elec = 8; newPat = 18; numEp = 20;

cd AD_stanStackNormAll
dirs1 = dir(fullfile('.','*.csv'));
x = 1; a = 1;
for file1 = dirs1'
    filename1 = file1.name;
    filename1 = fullfile(filename1)
    dat = importdata(filename1);
    
    frivolous = zeros(EpLen,elec,numEp,newPat);
    for k = 1:numEp
        for v = 1:elec
            for m = 1:newPat
                frivolous(:,v,k,m) = dat((20*(m-1)*EpLen)+k*EpLen-EpLen+1:(20*(m-1)*EpLen)+k*EpLen,v);
            end
        end
    end
    
    frivR = zeros(EpLen,elec,newPat);
    %frivR(:,1,:) = ones(elec,1)*a;
    for m = 1:newPat
        for v = 1:elec
            for l = 1:EpLen
                frivR(l,v,m) = mean(frivolous(l,v,:,m));
            end
        end
    end
    
    if a < 10
        na = strcat('0',num2str(a));
    else
        na = num2str(a);
    end
    
    for m = 1:newPat
        
        if x < 10
            n = strcat('00',num2str(x));
        elseif x >= 10 && x < 100
            n = strcat('0',num2str(x));
        else
            n = num2str(x);
        end
        
        cd ..
        cd AD_Split
        dlmwrite(strcat('AD',na,'_',n,'.csv'),frivR(:,:,m));
        cd ..
        cd AD_stanStackNormAll
        
        x = x+1;
    end
    a = a+1;
end
cd ..




EpLen = 301; elec = 8; newPat = 18; numEp = 2;

cd AD_targStackNormAll
dirs1 = dir(fullfile('.','*.csv'));
x = 1; a = 1;
for file1 = dirs1'
    filename1 = file1.name;
    filename1 = fullfile(filename1)
    dat = importdata(filename1);
    
    frivolous = zeros(EpLen,elec,numEp,newPat);
    for k = 1:numEp
        for v = 1:elec
            for m = 1:newPat
                frivolous(:,v,k,m) = dat((2*(m-1)*EpLen)+k*EpLen-EpLen+1:(2*(m-1)*EpLen)+k*EpLen,v);
            end
        end
    end
    
    frivR = zeros(EpLen,elec,newPat);
    for m = 1:newPat
        for v = 1:elec
            for l = 1:EpLen
                frivR(l,v,m) = mean(frivolous(l,v,:,m));
            end
        end
    end
    
    if a < 10
        na = strcat('0',num2str(a));
    else
        na = num2str(a);
    end
    
    for m = 1:newPat
        
        if x < 10
            n = strcat('00',num2str(x));
        elseif x >= 10 && x < 100
            n = strcat('0',num2str(x));
        else
            n = num2str(x);
        end
        
        cd ..
        cd AD_Split
        dlmwrite(strcat('AD',na,'_',n,'.csv'),frivR(:,:,m),'-append');
        cd ..
        cd AD_targStackNormAll
        
        x = x+1;
    end
    a = a+1;
end
