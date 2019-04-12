function outEp = AARBrazil(filename,EpochLength)

data = importdata(filename);
data = data(2:end,3:23);

Fs = 250;
[row,col] = size(data);
rowS = Fs*660; % 11 mins if Fs=250Hz
newDat = zeros(Fs*EpochLength,1);
for l = 1:col
    y = 1;
    for v = 1:floor(rowS/(Fs*EpochLength))
        newDat(1:Fs*EpochLength,1) = data((v-1)*Fs*EpochLength+1:v*Fs*EpochLength,l);
        if std(newDat) < 13
            outEp((y-1)*Fs*EpochLength+1:y*Fs*EpochLength,l) = newDat;
            y = y+1;
        end
    end
end

% for m = 1:col
%     y = 1;
%     for k = 1:length(outEp(1:end-1,1))
%         if outEp(k+1,m) ~= 0 || outEp(k,m) ~= 0
%             arEp{y,m} = outEp(k,m);
%             y = y+1;
%         end
%     end
% end