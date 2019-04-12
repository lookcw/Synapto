function brazil = brazilstat(filename)
tandDat = importdata(filename);

brazil = [];
[rows,columns] = size(tandDat);
n=tandDat(:,1);
for elec = 2:columns
    
    start = find(n==0); %probably 0
    fin = find(n==936); %probably 900
    
    maximum = max(tandDat(start:fin,elec));
    minimum = min(tandDat(start:fin,elec));
    
    average = mean(tandDat(start:fin,elec));
    med = median(tandDat(start:fin,elec));
    
    standard_deviation = std(tandDat(start:fin,elec));
    Variance = var(tandDat(start:fin,elec));
    Interquartile_Range=iqr(tandDat(start:fin,elec));
    Coefficient_of_Variance = (standard_deviation./average).*100;
    variance_to_mean_ratio = Variance./average;
    
    SignaltoNoise = (maximum)./(standard_deviation);
    
    brazil = [brazil maximum minimum average med standard_deviation Variance Interquartile_Range Coefficient_of_Variance variance_to_mean_ratio SignaltoNoise];
end
