function FD = higuchi1(filename,EpochLength)

dat = importdata(filename);
for k = 1:size(dat,2)/21
    data(:,:,k) = dat(:,(k-1)*21+1:k*21); % (data)row x (electrode)column x (patient)plane
    data(:,:,k) = eegfilt(data(:,:,k)',250,4,0)';
end

[row,col,pla] = size(data);
FD = [];
Fs = 250;
for k = 1:pla
    ep = intoEpochs(data(:,:,k),EpochLength,Fs,660); % (data)row x (electrode)column x (epoch)plane
    fd2 = [];
    for v = 1:size(ep,3)
        
        E = ep(:,:,v);
        
        N = size(E,1);
        fd1 = zeros(1,size(E,2));
        for n = 1:size(E,2)
            xdft = fft(E(:,n));
            xdft = xdft(1:N/2+1);
            psdx = (1/(Fs*N)) * abs(xdft).^2;
            psdx(2:end-1) = 2*psdx(2:end-1);
            freq = 0:Fs/N:Fs/2;
            fftval = psdx; %10*log10(psdx);
            fftvaln = fftval;
            x = fftvaln;
            %a = 1; x = zeros(100,size(E,2));
            %for l = linspace(0,size(xn,1)-11,100)+1
            %    x(a,n) = mean(xn(l:l+10));
            %    a = a+1;
            %end
            %x = E(:,n);
            
            % input:    x       data
            % output:   fd      fractal dimension estimate (using Higuchi method)
            
            % set-up
            kmax = 60;
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
        fd2 = [fd2,fd1];
    end
    FD = [FD;fd2];
end