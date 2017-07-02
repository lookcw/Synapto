function [brazil] = brazilstat(filename,b,c)
disp('asdfasdfasdfasdfasdfasdf')
if exist('csv0','var')~=1
    csv0 = importdata(filename);
    csv0 = csv0(:,1:8);
end
  exist('csv0','var')

[rows,columns]=size(csv0)

for row = 1:1:rows

%Where csv0 is the amplitudes in microvolts of ERP with baseline averaging
%csv0LREcsv0DY done (1 electrode)

%In addition, if we want we can just make the poststimulus vector into its
%own vector so that there is less need for indexing? 

start_of_stimulus = b; %probably 0
end_of_erp = c; %probably 900

maximum = max(csv0(row,start_of_stimulus:end_of_erp));
minimum = min(csv0(row,start_of_stimulus:end_of_erp));

average = mean(csv0(row,start_of_stimulus:end_of_erp));
med = median(csv0(row,start_of_stimulus:end_of_erp));

standard_deviation = std(csv0(row,start_of_stimulus:end_of_erp));
Variance = var(csv0(row,start_of_stimulus:end_of_erp));
Interquartile_Range=iqr(csv0(row,start_of_stimulus:end_of_erp));
Coefficient_of_Variance = (standard_deviation./average).*100;
variance_to_mean_ratio = Variance./average;

% This is only one method of calculating SNR, we can try others such as
% 1) using the snr matlab function, taking the standard_deviation of the
% entire ERP (including prestimulus)


SignaltoNoise = (maximum)./(standard_deviation);

% if things still don't work, try taking out the dots in the
% division/multiplication to 



brazil = [maximum minimum average med standard_deviation Variance Interquartile_Range Coefficient_of_Variance variance_to_mean_ratio SignaltoNoise];
end
