%% Must import data first (this case: struct named pat1) (From "Patients_Lucas")
% Copies useful part of struct into array y
y = zeros(20,60001);
for a=1:20
    y(a,:) = pat1.Signal(a,:);
end

%% Conducts and plots 20 FFTs
Fs = 250;
N = length(y);
df = Fs/N;
n = (-(N/2):(N/2)-1)*df;

Y2 = zeros(20,60001);
figure
for a = 1:20
    Y = abs(fft(y(a,:))/N);
    Y2(a,:) = abs(fftshift(Y)/N);
    subplot(4,5,a)
    %plot(n,10*log10(Y2(a,:)));
    plot(n,Y2(a,:));
    xlim([0,40]);
end

%% 1 FFT where y is the raw data (general use)
figure
N = length(y);
df = Fs/N;
n = (-(N/2):(N/2)-1)*df;
Y = abs(fft(y)/N);
Y2 = abs(fftshift(Y)/N);
plot(n,Y2) %don't necessarily need 10*log10()

%% Alternate
%for k = 1:21
%FF = DhruvTest(:,2);
FF = colNa;
Fs = 250;
N = length(FF);
xdft = fft(FF);
xdft = xdft(1:N/2+1);
psdx = (1/(Fs*N)) * abs(xdft).^2;
psdx(2:end-1) = 2*psdx(2:end-1);
freq = 0:Fs/N:Fs/2;
fftval = psdx; %10*log10(psdx);
%BHICAfft5(:,k) = fftval;
figure;
%subplot(3,2,5)
plot(freq,10*log10(fftval));
%plot(freq,fftval);
%end

%% Averaging to smooth the plots
figure
for a = 1:20
    subplot(4,5,a)
    %plot(n,10*log10(movmean(Y2(a,:),10)))
    plot(n,movmean(Y2(a,:),10))
    xlim([0,40])
    %ylim([-80,-55])
    title(a)
end

%%
con = zeros(20,120001);
figure
for a = 1:19
    con(a,:) = conv(Y2(a,:),Y2(a+1,:));
    plot(1:length(con(a,:)),con(a,:))
    hold on
end

%% 
con = zeros(20,120001);
figure
for a = 1:3
    con(a,:) = conv(Y2(a,:),Y2(a+7,:));
    plot(1:length(con(a,:)),con(a,:))
    hold on
end
