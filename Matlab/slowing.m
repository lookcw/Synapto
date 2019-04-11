function sl = slowing(filename,EpochLength)
%data = toMat(filename);
%data = data(:,2:22);

% Using F50
data = importdata(filename)';
data = data(:,2:22);

% Using BD_Fil
%data = importdata(filename);
%data = data(2:end,3:23);
%data = data';

sl = [];
Fs = 250;
[row,col] = size(data);
rowS = Fs*660; % 11 mins if Fs=250Hz
newDat = zeros(Fs*EpochLength,col);
for v = 1:floor(rowS/(Fs*EpochLength))
    for l = 1:col
        newDat(1:Fs*EpochLength,l) = data((v-1)*Fs*EpochLength+1:v*Fs*EpochLength,l);
    end
    data1 = newDat;
    
    sl1 = [];
    for b = 1:size(data1,2)
        
        totals = [];
        for c = 1:Fs:size(data1,1)
            
            x = data1(c:c+Fs-1,b);
            
            %plot(1:length(x),x,'-*')
            %hold on
            
            % Create vector of amplitude peaks
            n = 1;
            peaks = [];
            while n < size(x,1)-3
                
                %valley
                while (x(n+1) < x(n) && n < size(x,1)-2)
                    n=n+1;
                end
                
                %peak
                while (x(n+1) > x(n) && n < size(x,1)-1)
                    n=n+1;
                end
                peaks = [peaks x(n)];
                
                if x(n+1) == x(n)
                    n=n+1;
                end
            end
            
            % Create vector of amplitude differences
            differences = [];
            for k = 1:length(peaks)-1
                differences(k) = abs(peaks(k+1)-peaks(k));
            end
            
            % Sum differences and create vector of sums (for each second)
            total = sum(differences);
            totals = [totals total];
        end
        
        % Average sums for entire time length
        avgSlowing = sum(totals)/length(totals);
        %sl = avgSlowing;
        sl1 = [sl1 avgSlowing];
    end
    sl = [sl sl1];
end
end