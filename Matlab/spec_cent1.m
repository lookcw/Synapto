function SC = spec_cent1(filename,EpochLength)

dat = importdata(filename);
for k = 1:size(dat,2)/21
    data(:,:,k) = dat(:,(k-1)*21+1:k*21); % (data)row x (electrode)column x (patient)plane
    data(:,:,k) = eegfilt(data(:,:,k)',250,4,0)';
end

[row,col,pla] = size(data);
SC = [];
Fs = 250;
for k = 1:pla
    ep = intoEpochs(data(:,:,k),EpochLength,Fs,660); % (data)row x (electrode)column x (epoch)plane
    SC2 = [];
    for v = 1:size(ep,3)
        
        E = ep(:,:,v);
        
        N = size(E,1);
        SC1 = [];
        for n = 1:size(E,2)
            xdft = fft(E(:,n));
            xdft = xdft(1:N/2+1);
            psdx = (1/(Fs*N)) * abs(xdft).^2;
            psdx(2:end-1) = 2*psdx(2:end-1);
            freq = 0:Fs/N:Fs/2;
            fftval = psdx; %10*log10(psdx);
            
            for i = 1:length(fftval)
                num(i) = sum(i*fftval(i));
            end
            
            num = sum(num);
            den = sum(fftval);
            
            index = num/den;
            
            a = index/length(fftval)*Fs/2;
            SC1 = [SC1,a];
        end
        SC2 = [SC2,SC1];
    end
    SC = [SC;SC2];
end
