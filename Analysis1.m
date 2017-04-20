% Import 'TestAnalysis' from Drive and select the range [A1:I52392].
% There is a 'range' box to do this easily. Be sure to change 'output type'
% to Numeric Matrix (not Table) before importing.
rng default
Fs = 250; %sample frequency
FvsV = TestAnalysis'; %inverses the imported matrix
Elec1 = FvsV(9,:); %creates vector with values from only one electrode
x = Elec1(15300:19125); %stores the 15300th to 19125th values of Elec1 into x (aka 60sec to 75sec, aka 'eyes closed for 15sec')
xn = Elec1(1:3825); %stores the 1st to 3000th values of Elec1 into xn (aka 0sec to 15sec, aka 'eyes open for 15sec')

% This section was basically taken straight from MatLab's fft() page. Type fft( then click 'More Help'
N = length(x);
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

%%
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

%%
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
%%
% Can ignore this section for now. My next step was to check out how the
% derivatives compare to see if any significant differences can be found.
%K = length(psdxMod);
%slp = zeros(K,1);
%for n=1:K
%    slp(n) = (avgVal(n)-avgVal(n+1))/(freq(n+489)-freq(n+1+489));
%end
%%
figure
plot(freq,10*log10(psdx)) %raw data for closed eyes
hold on
plot(freq,10*log10(avgVal),'r') %moving average for closed eyes
hold on
%plot(freqn,10*log10(psdxn),'k') %get rid of the two '%' marks to the left to plot raw data for opened eyes
%hold on
plot(freqn,10*log10(avgValn),'m') %moving average for opened eyes
xlim([7,12]); ylim([-10,40])
grid on
title('Periodogram Using FFT')
xlabel('Frequency (Hz)')
ylabel('Power/Frequency (dB/Hz)')