function [brazil] = brazilstat(A,b,c)

for 
%Where A is the amplitudes in microvolts of ERP with baseline averaging
%ALREADY done (1 electrode)

%In addition, if we want we can just make the poststimulus vector into its
%own vector so that there is less need for indexing? 

start_of_stimulus = b; %probably 0
end_of_erp = c; %probably 900

maximum = max(A(start_of_stimulus:end_of_erp));
minimum = min(A(start_of_stimulus:end_of_erp));

average = mean(A(start_of_stimulus:end_of_erp));
med = median(A(start_of_stimulus:end_of_erp));

standard_deviation = std(A(start_of_stimulus:end_of_erp));
Variance = var(A(start_of_stimulus:end_of_erp));
Interquartile_Range=iqr(A(start_of_stimulus:end_of_erp));
Coefficient_of_Variance = (standard_deviation./average).*100;
variance_to_mean_ratio = Variance./average;

% This is only one method of calculating SNR, we can try others such as
% 1) using the snr matlab function, taking the standard_deviation of the
% entire ERP (including prestimulus)


SignaltoNoise = (maximum)./(standard_deviation);

% if things still don't work, try taking out the dots in the
% division/multiplication to 

brazil = [maximum minimum average med standard_deviation Variance Interquartile_Range Coefficient_of_Variance variance_to_mean_ratio SignaltoNoise];

