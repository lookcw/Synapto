function fd = higuchi(filename,EpochLength)
%data = toMat(filename);
%data = data(:,2:22);
data = importdata(filename);
data = data(2:end,3:23);

fd = [];
Fs = 250;
[row,col] = size(data);
rowS = Fs*660; % 11 mins if Fs=250Hz
newDat = zeros(Fs*EpochLength,col);
for v = 1:floor(rowS/(Fs*EpochLength))
    for l = 1:col
        newDat(1:Fs*EpochLength,l) = data((v-1)*Fs*EpochLength+1:v*Fs*EpochLength,l);
    end
    E = newDat;
    
    N = size(E,1);
    fd1 = zeros(1,size(E,2));
    for n = 1:size(E,2)
        %xdft = fft(E(:,n));
        %xdft = xdft(1:N/2+1);
        %psdx = (1/(Fs*N)) * abs(xdft).^2;
        %psdx(2:end-1) = 2*psdx(2:end-1);
        %freq = 0:Fs/N:Fs/2;
        %fftval = psdx; %10*log10(psdx);
        %fftvaln = fftval;
        %x = fftvaln;
        x = E(:,n);
        
        % input:    x       data
        % output:   fd      fractal dimension estimate (using Higuchi method)
        
        % set-up
        kmax = 40;
        M =      length(x); % get length of signal
        % maximal degree of reduction/degree of time stretch (increasing this will increase FD estimates)
        Lmk =    zeros(kmax,kmax);
        
        % get the mean length of curve
        for k = 1:kmax
            for m = 1:k
                Lmki = 0;
                for i=1:fix((M-m)/k)
                    Lmki = Lmki+abs(x(m+i*k)-x(m+(i-1)*k));
                end
                Ng =        (M-1)/(fix((M-m)/k)*k);
                Lmk(m,k) =  (Lmki*Ng)/k;
            end
        end
        
        Lk = zeros(1,kmax);
        for k = 1:kmax
            Lk(1,k) = sum(Lmk(1:k,k))/k;
        end
        
        % calculate the logarithmic values for slope calculation (which is the FD estimate)
        lnLk =  log(Lk);
        lnk =   log(1./(1:kmax));
        
        % calculate the slope and assign it to output
        b =  polyfit(lnk,lnLk,1);
        a =  b(1);
        fd1(n) = a;
    end
    fd = [fd,fd1];
end
end
