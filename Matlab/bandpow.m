function pow = bandpow(filename,EpochLength)
%data = toMat(filename);
%data = data(:,2:22);

% Using F50
data = importdata(filename)';
data = data(:,2:22);

% Using BD_Fil
%data = importdata(filename);
%data = data(2:end,3:23);
%data = data';


pow=[]; deltaP=[]; thetaP=[]; alphaP=[]; betaP=[];
Fs = 250;
[row,col] = size(data);
rowS = Fs*660; % 11 mins if Fs=250Hz (660)
newDat = zeros(Fs*EpochLength,col);
for v = 1:floor(rowS/(Fs*EpochLength))
    for l = 1:col
        newDat(1:Fs*EpochLength,l) = data((v-1)*Fs*EpochLength+1:v*Fs*EpochLength,l);
    end
    E = newDat;

    deltaP = bandpower(E,Fs,[1,3]); %[deltaP,bandpower(E,Fs,[1,3])];
    thetaP = bandpower(E,Fs,[3,8]); %[thetaP,bandpower(E,Fs,[3,8])];
    alphaP = bandpower(E,Fs,[8,12]); %[alphaP,bandpower(E,Fs,[8,12])];
    betaP  = bandpower(E,Fs,[12,35]); %[betaP,bandpower(E,Fs,[12,35])];
    
    for k = 1:col
        SDM(k+(v-1)*col) = std(E(:,k));
    end
    
    pow = [pow,deltaP,thetaP,alphaP,betaP];
end
% 
% 
% for k = 1:col
%     SDME(:,k) = SDM(k:col:length(SDM)); % (82 row)epochs x (21 column)electrodes (StDev)
%     dPME(:,k) = deltaP(k:col:length(deltaP)); % (82 row)epochs x (21 column)electrodes (Val)
%     tPME(:,k) = thetaP(k:col:length(thetaP));
%     aPME(:,k) = alphaP(k:col:length(alphaP));
%     bPME(:,k) = betaP(k:col:length(betaP));
% end
% S = 5; % Number of grouped epochs    **Comments based on S = 5**
% SDMES = zeros(S,floor(size(SDME,1)/S),col);
% dPMES = zeros(S,floor(size(dPME,1)/S),col);
% tPMES = zeros(S,floor(size(tPME,1)/S),col);
% aPMES = zeros(S,floor(size(aPME,1)/S),col);
% bPMES = zeros(S,floor(size(bPME,1)/S),col);
% for p = 1:col
%     y = 1;
%     for k = 1:S:size(SDME,1)-S
%         SDMES(:,y,p) = SDME(k:k+S-1,p); % (5 row x 16 column)epochs x (21 plane)electrodes (StDev)
%         dPMES(:,y,p) = dPME(k:k+S-1,p); % (5 row x 16 column)epochs x (21 plane)electrodes (Val)
%         tPMES(:,y,p) = tPME(k:k+S-1,p);
%         aPMES(:,y,p) = aPME(k:k+S-1,p);
%         bPMES(:,y,p) = bPME(k:k+S-1,p);
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
%                 dPEp2Av(y) = dPMES(k,p,u); % (1 row x 0-5 column)epochs (Val)
%                 tPEp2Av(y) = tPMES(k,p,u);
%                 aPEp2Av(y) = aPMES(k,p,u);
%                 bPEp2Av(y) = bPMES(k,p,u);
%                 y = y+1;
%             end
%         end
%         if length(SDEp2Av) < 1
%             SDEp2Av = min(SDMES(:,p,u)); % (1 row x 1 column)epoch (least varying artifact) (StDev)
%             dPEp2Av = dPMES(SDMES(:,p,u) == SDEp2Av,p,u); % (1 row x 1 column)epoch (least varying artifact) (Val)
%             tPEp2Av = tPMES(SDMES(:,p,u) == SDEp2Av,p,u);
%             aPEp2Av = aPMES(SDMES(:,p,u) == SDEp2Av,p,u);
%             bPEp2Av = bPMES(SDMES(:,p,u) == SDEp2Av,p,u);
%         end
%         SDAvEp(p+size(SDMES,2)*(u-1)) = mean(SDEp2Av); % (1 row x 16x21 column)epochs (mean StDev)
%         dPAvEp(p+size(SDMES,2)*(u-1)) = mean(dPEp2Av); % (1 row x 16x21 column)epochs (mean Val)
%         tPAvEp(p+size(SDMES,2)*(u-1)) = mean(tPEp2Av);
%         aPAvEp(p+size(SDMES,2)*(u-1)) = mean(aPEp2Av);
%         bPAvEp(p+size(SDMES,2)*(u-1)) = mean(bPEp2Av);
%     end
% end
% pow = [dPAvEp,tPAvEp,aPAvEp,bPAvEp];

end

    