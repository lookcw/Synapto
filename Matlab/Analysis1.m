%% FFT Section
if exist('TestAnalysis','var')~=1
    TestAnalysis = importdata('TestAnalysis.txt');
    TestAnalysis = TestAnalysis(1:52392, 1:9);
end
% A52488 - I81286
rng default
Fs = 250; %sample frequency
FvsV = TestAnalysis'; %inverses the imported matrix
FvsV2 = TestAnalysis1';
Elec1 = FvsV(9,:); %creates vector with values from only one electrode
x = Elec1(15300:19125); %stores the 15300th to 19125th values of Elec1 into x (aka 60sec to 75sec, aka 'eyes closed for 15sec')
xn = Elec1(1:3825); %stores the 1st to 3825th values of Elec1 into xn (aka 0sec to 15sec, aka 'eyes open for 15sec')
Elec4 = FvsV(5,:);

% This section was basically taken straight from MatLab's fft() page. Type fft( then click 'More Help'
N = length(x);
%x = detrend(x);
xdft = fft(x);
xdft = xdft(1:N/2+1);
psdx = (1/(Fs*N)) * abs(xdft).^2;
psdx(2:end-1) = 2*psdx(2:end-1);
freq = 0:Fs/length(x):Fs/2;

% Repeat of last section but using open eye data
Nn = length(xn);
xdftn = fft(xn);
xdftn = xdftn(1:Nn/2+1);
psdxn = (1/(Fs*Nn)) * abs(xdftn).^2;
psdxn(2:end-1) = 2*psdxn(2:end-1);
freqn = 0:Fs/length(xn):Fs/2;
%% 1 Electrode (#4)
figure
se = 199;
mm=linspace(0,255*se,255*se+1);
plot(mm,Elec4((1*255):(200*255)),'r');
%xlim([0,255*se]); ylim([-11000,-5000]);

%% All Raw Data (Eyes O/C Test)
figure
for k = 1:9
    mm = linspace(0,length(FvsV(k,:)),length(FvsV(k,:)+1));
    plot(mm,FvsV(k,:))
    hold on
end

%% Raw Data (2nd Test)
figure
for k = 1:9
    mm = linspace(0,length(FvsV2(k,:)),length(FvsV2(k,:)+1));
    plot(mm,FvsV2(k,:))
    hold on
end

%% Moving Averages
S = length(psdx); %stores length of psdx (power in this case aka the y-axis)
avgVal = zeros(S); %creates a 0 vector to be filled in by going through the for loop
% The for loop creates a vector of the moving average of psdx (smooths the data)
for n=10:S
    avgVal(n-5) = (psdx(n)+psdx(n-1)+psdx(n-2)+psdx(n-3)+psdx(n-4)+psdx(n-5)+psdx(n-6)+psdx(n-7)+psdx(n-8)+psdx(n-9))/10;
end

% Same as the section before but with open eye data
S1 = length(psdxn);
avgValn = zeros(S1);
for n=10:S1
    avgValn(n-5) = (psdxn(n)+psdxn(n-1)+psdxn(n-2)+psdxn(n-3)+psdxn(n-4)+psdxn(n-5)+psdxn(n-6)+psdxn(n-7)+psdxn(n-8)+psdxn(n-9))/10;
end

% *ignore for now.. 490 (7.9897) to 644 (10.5058)*

%% Difference Analysis
% This section attempts to compare the difference between the values in
% closed eye data to the difference between the values in open eye data.
% (Cannot directly compare the two b/c the power of each do not map well
% with each other, instead an indirect comparison (comparing each dataset's
% moving difference) is used)
% However, I am running into trouble with this section so it may not be
% perfect. I'm using a different dataset than what was originally used to
% make this code and something seems off.
logpsdx = 10*log10(avgVal);
psdxMod = logpsdx(490:644);
M = find(psdxMod==max(psdxMod));
Val = psdxMod(M);
for n=M:-15:1
    Val = Val-(Val-psdxMod(n));
end
Val

logpsdxn = 10*log10(avgValn);
psdxModn = logpsdxn(490:644);
M1 = find(psdxMod==max(psdxMod));
Valn = psdxModn(M1);
for n=M1:-15:1
    Valn = Valn-(Valn-psdxModn(n));
end
Valn
%% Slope Analysis
% Can ignore this section for now. My next step was to check out how the
% derivatives compare to see if any significant differences can be found.
%K = length(psdxMod);
%slp = zeros(K,1);
%for n=1:K
%    slp(n) = (avgVal(n)-avgVal(n+1))/(freq(n+489)-freq(n+1+489));
%end
%% Closed Eye FvsP
figure
plot(freq,10*log(psdx)) %raw data for closed eyes
hold on
plot(freq,10*log(avgVal),'r') %moving average for closed eyes
hold on
xlim([0,40]); ylim([-20,100])
%%
%plot(freqn,10*log10(psdxn),'k') %get rid of the two '%' marks to the left to plot raw data for opened eyes
%hold on
plot(freqn,10*log10(avgValn),'m') %moving average for opened eyes
xlim([7,12]); ylim([-10,40])
grid on
title('Periodogram Using FFT')
xlabel('Frequency (Hz)')
ylabel('Power/Frequency (dB/Hz)')

%%
tic
G = fftConMax('NL 0001 IVCV  F 77A E4 MM26 C0 NL DAS 03 03 2014].txt',8,3,9);
toc

%%
for k = 1:12
    ph(k,:) = bandpow(strcat('BHFil',num2str(k),'.txt'),8);
end

%%
for n = 1:12
    y = 1;
    for k = 1:21:length(ph)
        hc(y,:,n) = ph(n,k:k+20);
        y = y+1;
    end
    % x = 1;
    % for k = 1:21:length(p)
    %     ad(x,:) = ph2(k:k+20);
    %     x = x+1;
    % end
    for k = 1:4
        hca(:,k,n) = hc(k:4:end,1,n);
    end
end
figure
for n = 1:12
    subplot(2,6,n)
    plot(1:length(hca(:,1,n)),hca(:,1,n)); ylim([0,1000]);
end

%% 
figure
for k = 1:4
    subplot(2,2,k)
    hca = hc(k:4:end,1);
    ada = ad(k:4:end,1);
    plot(1:length(ada),ada); hold on
    plot(1:length(hca),hca); hold off
end
%%
a = importdata('BAFil1.txt');
h = importdata('BHFil1.txt');
%%
figure
histogram([0,8,35,10,5,4,3,15,4,6,2],35); xlim([0,40]); ylim([0,4]); hold on
histogram([10,5,3,4.5,8,6,3,15,4,3,4,5],12); xlim([0,40]); ylim([0,4]); hold off
legend('STM','ENGR'); xlabel('Time studying per week (hrs)'); ylabel('Frequency');
%%
mean([0,8,10,5,4,3,15,4,6,2]);
std([0,8,10,5,4,3,15,4,6,2]);

%%
yn = zeros(15,2040);
ynd = zeros(15,2040);
for k = 1:size(EDhruv,2)
x = 1:length(EDhruv(:,k));
y = EDhruv(:,k)';
%figure
%plot(1:length(DhruvTestF(2,:)),DhruvTestF(2,:)); hold on
%DhruvTestT(2,:) = detrend(DhruvTestF(2,:));
%plot(1:length(DhruvTestT(2,:)),DhruvTestT(2,:));
%plot(x,y); hold on
val = polyval(polyfit(x,y,6),x);
%plot(x,val)
yn(k,:) = y-val;
ynd(k,:) = detrend(yn(k,:));
%plot(x,yn)
end
%%
figure
for k = 1:4
    subplot(2,2,k)
    plot(1:60,pow(k:4:end))
end

%% Epochs
x = ADEp(:,:,1,1);
figure
for k = 1:82
    subplot(6,14,k)
    plot(linspace(0,length(x(:,k))/250,length(x(:,k))),x(:,k))
    xlim([0,8]); ylim([-80,80]);
    title(strcat(num2str(k),'---',num2str(std(x(:,k)))));
end
%%
for k = 1:82
    Test(k) = std(BAEp9(:,k));
end
figure
histogram(Test,20)
%%
figure
for k = 1:15
    subplot(3,5,k)
    plot(linspace(0,length(ynd(:,k))/250,length(ynd(:,k))),ynd(:,k))
    xlim([0,8]); ylim([-160,160]);
end
%%
Maj = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]';
Grd = [1,2,4,3,4,4,4,2,2,3,4,2,1,1,4,4,2,3,2,3,4,4,4,1,4,3,4,4,4,4,4,3,4,4,4,3,4,3,4,4,4,4,4,4,1,4,4,4,4,4,4,4,3,4,3,3,4,4,3,4,3,4,3,2,3,4,4,4,4,4,4,3,4]';
Cre = [15,17,16,17,13,12,12,15,16,15,12,14,15,14,16,16,17,15,18,17,16,16,6,16,15,16,15,15,19,15,15,15,17,14,16,15,13,17,15,17,16,16,16,15,16,12,16,15,15,12,16,19,13,16,18,17,16,14,9,17,17,21,13,17,12,12,12,15,17,12,14,16,15]';
Stu = [0.5,2,2,2,2,2,4,4,4,4,4,4,6,6,6,6,6,6,6,8,8,8,8,10,10,10,12,12,14,16,16,16,0.5,0.5,0.5,0.5,2,2,2,2,2,2,2,2,4,4,4,4,4,4,4,4,6,6,8,8,8,8,8,8,8,8,10,10,10,12,12,12,14,14,14,16,16]';
x = [Grd,Maj,Cre];
mdl = fitlm(x,Stu)
p = polyfit(Grd,Stu,1);
figure
%scatter(Grd,Stu,'*'); hold on
scatter(GrdEGR,StuEGR,'r*'); hold on
scatter(GrdNEG,StuNEG,'b*')
plot(Grd,polyval(p,Grd)); hold off
xlabel('Class (1=Fr, 2=So, 3=Ju, 4=Se)'); ylabel('Hours studied per week')
%% 
x = 1; y = 1;
for k = 1:length(Maj)
    if Maj(k) == 1
        StuEGR(x) = Stu(k);
        GrdEGR(x) = Grd(k);
        x = x+1;
    end
    if Maj(k) == 0
        StuNEG(y) = Stu(k);
        GrdNEG(y) = Grd(k);
        y = y+1;
    end
end
%%
x = [Grd,Maj,Cre];
mdl = fitlm(x,Stu)

%% 
figure
subplot(1,2,1)
scatter(1:length(BHfftB1(:,3)),10*log10(BHfftB5(:,3)),'.'); ylim([-70,30]);
subplot(1,2,2)
scatter(1:length(BHfftB1(:,3)),10*log10(BHfftICA5B(:,3)),'.'); ylim([-70,30]);
%%
[row,col] = size(BHICAfft5);
    for k = 1:col
        n = 1;
        for l = 1:250:row-1
            BHfftICA5B(n,k) = mean(BHICAfft5(l:l+250,k));
            n = n+1;
        end
    end


