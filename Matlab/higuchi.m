function fd = higuchi(filename,EpochLength,TotalLength_s,Fs)
%data = toMat(filename);
%data = data(:,2:22);

% Using F50
data = importdata(filename);

% Using BD_Fil
%data = importdata(filename);
%data = data(2:end,3:23);
%data = data(2:end,14); % One electrode

% No filename
%data = filename;

fd = [];
[row,col] = size(data);
rowS = Fs*TotalLength_s;
newDat = zeros(Fs*EpochLength,col);
%SDM = zeros(1,floor(rowS/(Fs*EpochLength))*col);
for v = 1:floor(rowS/(Fs*EpochLength))
    for l = 1:col
        newDat(1:Fs*EpochLength,l) = data((v-1)*Fs*EpochLength+1:v*Fs*EpochLength,l);
    end
    E = newDat;
    
    N = size(E,1);
    fd1 = zeros(1,size(E,2));
    for n = 1:size(E,2)
        
        % FFT
%         xdft = fft(E(:,n));
%         xdft = xdft(1:N/2+1);
%         psdx = (1/(Fs*N)) * abs(xdft).^2;
%         psdx(2:end-1) = 2*psdx(2:end-1);
%         freq = 0:Fs/N:Fs/2;
%         fftval = psdx; %10*log10(psdx);
%         fftvaln = fftval;
%         x = fftvaln;
        
        %a = 1; x = zeros(100,size(E,2));
        %for l = linspace(0,size(xn,1)-11,100)+1
        %    x(a,n) = mean(xn(l:l+10));
        %    a = a+1;
        %end
        
        x = E(:,n); 
        
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
                Ng = (M-1)/(fix((M-m)/k)*k);
                Lmk(m,k) = (Lmki*Ng)/k;
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
%     for k = 1:col
%         SDM(k+(v-1)*col) = std(E(:,k));
%     end
    fd = [fd,fd1];
end

% for k = 1:col
%     SDME(:,k) = SDM(k:col:length(SDM)); % (82 row)epochs x (21 column)electrodes (StDev)
%     fdME(:,k) = fd(k:col:length(fd)); % (82 row)epochs x (21 column)electrodes (HigVal)
% end
% S = 7; % Number of grouped epochs    **Comments based on S = 5**
% SDMES = zeros(S,floor(size(SDME,1)/S),col);
% fdMES = zeros(S,floor(size(fdME,1)/S),col);
% for p = 1:col
%     y = 1;
%     for k = 1:S:size(SDME,1)-S
%         SDMES(:,y,p) = SDME(k:k+S-1,p); % (5 row x 16 column)epochs x (21 plane)electrodes (StDev)
%         fdMES(:,y,p) = fdME(k:k+S-1,p); % (5 row x 16 column)epochs x (21 plane)electrodes (HigVal)
%         y = y+1;
%     end
% end
% 
% for u = 1:size(SDMES,3)
%     Thresh = min(SDME(:,u)) + 7; %prctile(SDME(:,u),25)+6;
%     for p = 1:size(SDMES,2)
%         SDEp2Av = [];
%         y = 1;
%         for k = 1:size(SDMES,1)
%             if SDMES(k,p,u) < Thresh
%                 SDEp2Av(y) = SDMES(k,p,u); % (1 row x 0-5 column)epochs (StDev)
%                 fdEp2Av(y) = fdMES(k,p,u); % (1 row x 0-5 column)epochs (HigVal)
%                 y = y+1;
%             end
%         end
%         if length(SDEp2Av) < 1
%             SDEp2Av = min(SDMES(:,p,u)); % (1 row x 1 column)epoch (least varying artifact) (StDev)
%             fdEp2Av = fdMES(SDMES(:,p,u) == SDEp2Av,p,u); % (1 row x 1 column)epoch (least varying artifact) (HigVal)
%         end
%         SDAvEp(p+size(SDMES,2)*(u-1)) = mean(SDEp2Av); % (1 row x 16x21 column)epochs (mean StDev)
%         fdAvEp(p+size(SDMES,2)*(u-1)) = mean(fdEp2Av); % (1 row x 16x21 column)epochs (mean HigVal)
%     end
% end
% fd = fdAvEp;
% 
% % GE = 8;
% % fdz = [];
% % for z = 0:21*GE:length(fd)-21*GE-mod(length(fd),21*GE)
% %     fdnr = [];
% %     for r = 0:20
% %         y = 1;
% %         for k = 1:21:21*GE
% %             fdn(y) = fd(k+r+z);
% %             y = y+1;
% %         end
% %         fdnr = [fdnr,mean(fdn)];
% %     end
% %     fdz = [fdz,fdnr];
% % end
% % fd = fdz;
%     
% end
