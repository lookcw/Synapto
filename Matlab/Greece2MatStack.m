Fs = 250;

cd MCI_GD
dirs1 = dir(fullfile('.','*.mat'));
dirs2 = dir(fullfile('.','*.txt'));
x = 1; 
for file1 = dirs1'
    file2 = dirs2(x);
    filename1 = file1.name;
    filename2 = file2.name;
    filename1 = fullfile(filename1)
    filename2 = fullfile(filename2)
    dat = importdata(filename1);
    ton = importdata(filename2);
    
    times = 1:length(dat.DIN_1);
    for k = 1:length(dat.DIN_1)
        times(k) = dat.DIN_1{4,k};
    end
    
    T = linspace(1/250,length(dat.Category_1_Segment1(1,:))/250,length(dat.Category_1_Segment1(1,:)))';
    E = [dat.Category_1_Segment1(124,:);dat.Category_1_Segment1(149,:);dat.Category_1_Segment1(95,:);dat.Category_1_Segment1(178,:);dat.Category_1_Segment1(59,:);dat.Category_1_Segment1(183,:);dat.Category_1_Segment1(47,:);dat.Category_1_Segment1(2,:)]; % O1 O2 T5 T6 C3 C4 F7 F8
    
    %T = linspace(1/250,length(dat.Category_1(1,:))/250,length(dat.Category_1(1,:)))';
    %E = [dat.Category_1(124,:);dat.Category_1(149,:);dat.Category_1(95,:);dat.Category_1(178,:);dat.Category_1(59,:);dat.Category_1(183,:);dat.Category_1(47,:);dat.Category_1(2,:)]; % O1 O2 T5 T6 C3 C4 F7 F8
    
    E1lp = eegfilt(E,Fs,0,35);
    E1 = eegfilt(E1lp,Fs,0.2,0);
    
    % Stores 480 events from 8 electrodes
    len = 301;
    events = zeros(len,8,480);
    for v = 1:8
        for k = 11:490
            events(:,v,k-10) = E1(v,times(k-10)-50:times(k-10)+250);
        end
    end
    t = linspace(-200,1000,len)';
    
    % Stores target tones into matrix targ and standard tones into stan
    targ = []; stan = [];
    for v = 1:8
        n = 1; m = 1;
        for k = 1:480
            if ton.data(k,2)==1 && ton.data(k,3)~=0
                targ(:,v,n) = events(:,v,k);
                n = n+1;
            elseif ton.data(k,2)==0 && ton.data(k,3)==0
                stan(:,v,m) = events(:,v,k);
                m = m+1;
            end
        end
    end
    
    % Baseline removal
    lenS = size(stan,3); lenT = size(targ,3);
    poststim = find(t>=0);
    baseS = zeros(lenS,8);
    for v = 1:8
        for k = 1:lenS
            baseS(k,v) = mean(stan(1:poststim(1),v,k));
            stan(:,v,k) = stan(:,v,k) - baseS(k,v);
        end
    end
    baseT = zeros(lenT,8);
    for v = 1:8
        for k = 1:lenT
            baseT(k,v) = mean(targ(1:poststim(1),v,k));
            targ(:,v,k) = targ(:,v,k) - baseT(k,v);
        end
    end
    
    % Stack
    stanStack = zeros(lenS*len,8);
    for v = 1:8
        for k = 1:lenS
            stanStack(len*(k-1)+1:len*k,v) = stan(:,v,k);
        end
    end
    targStack = zeros(lenT*len,8);
    for v = 1:8
        for k = 1:lenT
            targStack(len*(k-1)+1:len*k,v) = targ(:,v,k);
        end
    end
    
%     figure
%     plot(linspace(-50/0.250,1000,length(targStack)),targStack)
%     figure
%     plot(linspace(-50/0.250,1000,length(stanStack)),stanStack)
    
%     datTarg = [t,targStack];
%     datStan = [t,stanStack];

    if x < 10
        n = strcat('0',num2str(x));
    else
        n = num2str(x);
    end
    
    cd MCI_targStack
    dlmwrite(strcat('MCItargS',n,'.csv'),targStack);
    cd ..
    cd MCI_stanStack
    dlmwrite(strcat('MCIstanS',n,'.csv'),stanStack);
    cd ..
    
    x=x+1;
    
end

