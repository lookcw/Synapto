% With an input matrix in this form:
%       Column 1      = time (must include a time 0)
%       Columns 2-end = data (one dataset (i.e. electrode) per column)
% This function outputs a vector in this form:
%   [[Stats of column 2 of input],[Stats of column 3 of input],etc...]

function [brazil] = brazilStatMat(mat)

brazil = [];
[rows,columns] = size(mat);
n=mat(:,1);
for data = 2:columns

start_of_stimulus = find(n==0); %probably 0
end_of_erp = find(max(n)); %probably around 900
maximum = max(csv0(start_of_stimulus:end_of_erp,data));
minimum = min(csv0(start_of_stimulus:end_of_erp,data));

average = mean(csv0(start_of_stimulus:end_of_erp,data));
med = median(csv0(start_of_stimulus:end_of_erp,data));

standard_deviation = std(csv0(start_of_stimulus:end_of_erp,data));
Variance = var(csv0(start_of_stimulus:end_of_erp,data));
Interquartile_Range=iqr(csv0(start_of_stimulus:end_of_erp,data));
Coefficient_of_Variance = (standard_deviation./average).*100;
variance_to_mean_ratio = Variance./average;

SignaltoNoise = (maximum)./(standard_deviation);

brazil = [brazil maximum minimum average med standard_deviation Variance Interquartile_Range Coefficient_of_Variance variance_to_mean_ratio SignaltoNoise];
end
