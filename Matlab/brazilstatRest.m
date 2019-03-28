function brazil = brazilstatRest(filename,EpochLength)
%data = toMat(filename);
%data = data(:,2:22);

% Using F50
data = importdata(filename)';
data = data(:,2:22);

% Using BD_Fil
%data = importdata(filename);
%data = data(2:end,3:23);

brazil = [];
Fs = 250;
[row,col] = size(data);
rowS = Fs*660; % 11 mins if Fs=250Hz
newDat = zeros(Fs*EpochLength,col);
for v = 1:floor(rowS/(Fs*EpochLength))
    for l = 1:col
        newDat(1:Fs*EpochLength,l) = data((v-1)*Fs*EpochLength+1:v*Fs*EpochLength,l);
    end
    E = newDat;
     
    brazil1 = [];
    [rows,columns] = size(E);
    for elec = 1:columns
        
        start = 1; %find(n==0); %probably 0 (erp)
        fin = rows; %find(n==936); %probably 900 (erp)
        
        maximum = max(E(start:fin,elec));
        minimum = min(E(start:fin,elec));
        
        average = mean(E(start:fin,elec));
        med = median(E(start:fin,elec));
        
        standard_deviation = std(E(start:fin,elec));
        Variance = var(E(start:fin,elec));
        Interquartile_Range=iqr(E(start:fin,elec));
        Coefficient_of_Variance = (standard_deviation./average).*100;
        variance_to_mean_ratio = Variance./average;
        
        SignaltoNoise = (maximum)./(standard_deviation);
        
        brazil1 = [brazil1 maximum minimum average med standard_deviation Variance Interquartile_Range Coefficient_of_Variance variance_to_mean_ratio SignaltoNoise];
    end
    brazil = [brazil,brazil1];
end
