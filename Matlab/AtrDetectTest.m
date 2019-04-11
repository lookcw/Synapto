%% Import data (from HCF50)
Fs = 250;
data = importdata(filename);
data = data(1:Fs*660,:);
%% Epochs, BandPower, K-Means
data1 = intoEpochs(data,1,250,660);
data8 = intoEpochs(data,8,250,660);
data1E2 = []; data1E2(:,:) = data1(:,2,:);
del = [];
for k = 1:size(data1,3)
    del(k) = bandpower(data1E2(:,k),250,[0.5,4]);
end

figure; plot(1:length(del),del)

idx = kmeans(del',7);
%% Vectors of groups
a=1; b=1; c=1; d=1; f=1; g=1; h=1;
dela=[]; delb=[]; delc=[]; deld=[]; delf=[]; delg=[]; delh=[];
Cla=[];  Clb=[];  Clc=[];  Cld=[];  Clf=[];  Clg=[];  Clh=[]; 
for k = 1:length(idx)
    if idx(k) == 1
        dela(a) = del(k);
        Cla(a) = k;
        a = a+1;
    elseif idx(k) == 2
        delb(b) = del(k);
        Clb(b) = k;
        b = b+1;
    elseif idx(k) == 3
        delc(c) = del(k);
        Clc(c) = k;
        c = c+1;
    elseif idx(k) == 4
        deld(d) = del(k);
        Cld(d) = k;
        d = d+1;
    elseif idx(k) == 5
        delf(f) = del(k);
        Clf(f) = k;
        f = f+1;
    elseif idx(k) == 6
        delg(g) = del(k);
        Clg(g) = k;
        g = g+1;
    elseif idx(k) == 7
        delh(h) = del(k);
        Clh(h) = k;
        h = h+1;
    end
end
len = [length(dela),length(delb),length(delc),length(deld),length(delf),length(delg),length(delh)];
inM = find(len==max(len));
if inM == 1
    Cl = Cla;
elseif inM == 2
    Cl = Clb;
elseif inM == 3
    Cl = Clc;
elseif inM == 4
    Cl = Cld;
elseif inM == 5
    Cl = Clf;
elseif inM == 6
    Cl = Clg;
elseif inM == 7
    Cl = Clh;
end


%% Plot groups
figure; scatter(1:length(dela),dela,'r*'); hold on
scatter(1:length(deld),deld,'b*'); hold on
scatter(1:length(delc),delc,'b*'); hold on
scatter(1:length(delb),delb,'b*'); hold on
scatter(1:length(delf),delf,'b*'); hold on
scatter(1:length(delg),delg,'b*'); hold on
scatter(1:length(delh),delh,'b*'); hold on
%scatter(1:length(delj),delj,'b*'); hold on
%scatter(1:length(dell),dell,'b*');
set(gca,'yscale','log')
%% Plot normal Epochs
figure
for k = 1:size(data8,3)
    subplot(9,10,k)
    plot(1:length(data8(:,2,k)),data8(:,2,k))
    ylim([-80,80]); title(num2str((k-1)*8))
end

%% Replace artifacts with 0
for k = 1:size(data1E2,2)
    if find(Cl==k) > 0
        Cle((k-1)*250+1:k*250) = data1E2(:,k);
    else
        Cle((k-1)*250+1:k*250) = zeros(1,250);
    end
end

%% Plot Epochs with 0s instead of artifacts
Clea = intoEpochs(Cle',8,250,660);
figure
for k = 1:size(Clea,3)
    subplot(9,10,k)
    plot(1:length(Clea(:,1,k)),Clea(:,1,k))
    ylim([-80,80]); title(num2str((k-1)*8))
end

%% Replace artifacts with 4Hz highpass
for k = 1:size(data1E2,2)
    if find(Cl==k) > 0
        Clean((k-1)*250+1:k*250) = data1E2(:,k);
    else
        Clean((k-1)*250+1:k*250) = eegfilt(data1E2(:,k)',250,4,0,250,82);
    end
end

%% Plot Epochs with 4Hz highpassed data instead of artifacts
CleanD = intoEpochs(Clean',8,250,660);
figure
for k = 1:size(CleanD,3)
    subplot(9,10,k)
    plot(1:length(CleanD(:,1,k)),CleanD(:,1,k))
    ylim([-80,80]); title(num2str((k-1)*8))
end