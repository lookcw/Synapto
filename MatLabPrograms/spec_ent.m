function SE = spec_ent(filename)

if exist('data','var')~=1
    data = importdata(filename);
    data = data(:,2:8);
    %data = data(1:4000,2:8);
end

rawdata = data';
E1 = rawdata(1,:);
E2 = rawdata(2,:);
E3 = rawdata(3,:);
E4 = rawdata(4,:);
E5 = rawdata(5,:);
E6 = rawdata(6,:);
E7 = rawdata(7,:);
%E8 = rawdata(8,:);
E = [E1;E2;E3;E4;E5;E6;E7];
siz = size(E);

Fs = 250;
N = siz(2);

for n = 1:siz(1)
xdft = fft(E(n,:));
xdft = xdft(1:N/2+1);
psdx = (1/(Fs*N)) * abs(xdft).^2;
psdx(2:end-1) = 2*psdx(2:end-1);
freq = 0:Fs/N:Fs/2;
fftval = 10*log10(psdx);

bandindex = find(freq>0.5 & freq<30);
fftband = fftval(bandindex);

bins = Fs/2;
psd = (abs(fftband).^2)/bins;
psdnorm = psd/sum(psd);

for k = 1:length(psdnorm)
psdnorm(k) = psdnorm(k)*log(psdnorm(k));
end

SE = -sum(psdnorm)

%figure;
%plot(freq,fftval(1:length(freq)))
%xlim([0,30]); 
%ylim([-10,100]);
%grid on
end