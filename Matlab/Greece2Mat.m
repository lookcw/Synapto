Fs = 250;

cd HC_GD
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
    
    E1lp = eegfilt(E,Fs,0,35);
    E1 = eegfilt(E1lp,Fs,0.2,0);
    
    % Stores 480 events from 8 electrodes
    len = 301;
    events = zeros(len,8,480);
    for v = 1:8
        for k = 1:480
            events(:,v,k) = E1(v,times(k)-50:times(k)+250);
        end
    end
    t = linspace(-200,1000,len)';
    
    % Stores target tones into matrix targ and standard tones into stan
    for v = 1:8
        n = 1; m = 1;
        for k = 1:480
            if ton.data(k,2)==1 && ton.data(k,3)~=0
                targ(:,v,n) = events(:,v,k);
                n = n+1;
            end
            if ton.data(k,2)==0 && ton.data(k,3)==0
                stan(:,v,n) = events(:,v,k);
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
    
    % Averages
    avgtarg = zeros(len,8);
    for v = 1:8
        for k = 1:len
            avgtarg(k,v) = mean(targ(k,v,:));
        end
    end
    avgstan = zeros(len,8);
    for v = 1:8
        for k = 1:len
            avgstan(k,v) = mean(stan(k,v,:));
        end
    end
%     figure
%     plot(linspace(-50/0.250,1000,length(avgtarg)),avgtarg)
%     figure
%     plot(linspace(-50/0.250,1000,length(avgstan)),avgstan)
    
    hctarg = [t,avgtarg];
    hcstan = [t,avgstan];
    
    cd ..
    cd HC_targ
    dlmwrite(strcat('MCItarg',num2str(x),'.csv'),hctarg);
    cd ..
    cd HC_stan
    dlmwrite(strcat('MCIstan',num2str(x),'.csv'),hcstan);
    cd ..
    cd HC_GD
    
    x=x+1;
    
end

