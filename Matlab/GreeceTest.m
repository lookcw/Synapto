Fs = 250;

times = 1:length(DIN_1);
for k = 1:length(DIN_1)
    times(k) = DIN_1{4,k};
end

t = linspace(1/250,length(Category_1(1,:))/250,length(Category_1(1,:)))';
E = Category_1(119,:)';

%E1 = eegfilt(E,Fs,0,35); 

%% FIR Lowpass
%plot(t,E1n)
Fs = 250;
Fpass = 30;            % Passband Frequency
Fstop = 33;            % Stopband Frequency
Dpass = 10^-1/10;      % Passband Ripple
Dstop = 10^-40/10;     % Stopband Attenuation
match = 'stopband';

[N, Fo, Ao, W] = firpmord([Fpass,Fstop]/(Fs/2), [1,0], [Dpass,Dstop]); 
b  = firpm(N, Fo, Ao, W);

N = length(E1);
df = Fs/N;
n = (-(N/2):(N/2)-1)*df;

y = filter(b,1,E1);
y = E1;
%figure
%plot(1:length(y),y)
Y = abs(fft(y)/N);
Y2 = abs(fftshift(Y)/N);
figure
plot(n,10*log10(Y2));
%plot(n,Y2);
xlim([0,120]);
%ylim([0,5*10^-5]);

%% Notch Filter 50Hz
Fpass1 = 45;               % First Passband Frequency
Fstop1 = 49;               % First Stopband Frequency
Fstop2 = 51;              % Second Stopband Frequency
Fpass2 = 55;              % Second Passband Frequency
Dpass1 = 0.028774368332;  % First Passband Ripple
Dstop  = 0.031622776602;  % Stopband Attenuation
Dpass2 = 0.057501127785;  % Second Passband Ripple
dens   = 16;              % Density Factor

[N, Fo, Ao, W] = firpmord([Fpass1 Fstop1 Fstop2 Fpass2]/(Fs/2), [1 0 1], [Dpass1 Dstop Dpass2]);
b  = firpm(N, Fo, Ao, W, {dens});

N = length(y);
df = Fs/N;
n = (-(N/2):(N/2)-1)*df;
yn = filter(b,1,y);
Y = abs(fft(yn)/N);
Y2 = abs(fftshift(Y)/N);
figure
plot(n,10*log10(Y2));
xlim([0,120]);
%% Notch Filter 100Hz
Fpass1 = 95;               % First Passband Frequency
Fstop1 = 99;               % First Stopband Frequency
Fstop2 = 101;              % Second Stopband Frequency
Fpass2 = 105;              % Second Passband Frequency
Dpass1 = 0.028774368332;  % First Passband Ripple
Dstop  = 0.031622776602;  % Stopband Attenuation
Dpass2 = 0.057501127785;  % Second Passband Ripple
dens   = 16;              % Density Factor

[N, Fo, Ao, W] = firpmord([Fpass1 Fstop1 Fstop2 Fpass2]/(Fs/2), [1 0 1], [Dpass1 Dstop Dpass2]);
b  = firpm(N, Fo, Ao, W, {dens});

N = length(yn);
df = Fs/N;
n = (-(N/2):(N/2)-1)*df;
yn2 = filter(b,1,yn);
Y = abs(fft(yn2)/N);
Y2 = abs(fftshift(Y)/N);
figure
plot(n,10*log10(Y2));
xlim([0,120]);

%% stores 500 events from single electrode
events = zeros(301,500);
for k = 1:500
    events(:,k) = E1(times(k)-50:times(k)+250);
end
%% plots 6 [-200-1000]ms events
figure
for k = 22:27
    subplot(2,3,k-21)
    plot(linspace(-50/0.250,1000,length(events(:,k))),events(:,k))
    grid on
end

%% Stores target tones into matrix targ and standard tones into stan
n = 1; m = 1;
for k = 1:500
    if s0175(k,2)==1 && s0175(k,3)~=0
        targ(:,n) = events(:,k);
        n = n+1;
    end
    if s0175(k,2)==0 && s0175(k,3)==0
        stan(:,m) = events(:,k);
        m = m+1;
    end
end

% Averages
avgtarg = (1:301)';
for k = 1:301
    avgtarg(k,1) = mean(targ(k,:));
end
avgstan = (1:301)';
for k = 1:301
    avgstan(k,1) = mean(stan(k,:));
end
figure
plot(linspace(-50/0.250,1000,length(avgtarg)),avgtarg)
figure
plot(linspace(-50/0.250,1000,length(avgstan)),avgstan)


%% Baseline removal
normtarg = avgtarg;
for k = 1:301
    normtarg(k,1) = avgtarg(k,1) - avgtarg(51,1);
end
normstan = avgstan;
for k = 1:301
    normstan(k,1) = avgstan(k,1) - avgstan(51,1);
end
figure
plot(linspace(-50/0.250,1000,length(normtarg)),normtarg)
figure
plot(linspace(-50/0.250,1000,length(normstan)),normstan)

