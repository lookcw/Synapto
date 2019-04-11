function [SE1,CV,Test] = grangerFstat(filename,c,d)

data = importdata(filename);
data = data(2:end,3:23);

% Division into 5 zones ---------------------
% Zone 1 ------------------------------------
    z_1(:,1) = data(:, 1);
    z_1(:,2) = data(:, 2);
    z_1(:,3) = data(:, 3);
    z_1(:,4) = data(:, 6);
    z_1(:,5) = data(:, 9);
    
    % Average of zone 1
    z_1(:,1) = mean(z_1,2);
    
% Zone 2 ------------------------------------
    z_2(:,1) = data(:, 4);
    z_2(:,2) = data(:, 9);
    z_2(:,3) = data(:, 14);
    
    % Average of zone 2
    z_2(:,1) = mean(z_2,2);

% Zone 3 ------------------------------------    
    z_3(:,1) = data(:, 16);
    z_3(:,2) = data(:, 18);
    z_3(:,3) = data(:, 19);
    z_3(:,4) = data(:, 20);
    z_3(:,5) = data(:, 21);
    
    % Average of zone 3
    z_3(:,1) = mean(z_3,2);
  
% Zone 4 ------------------------------------
    z_4(:,1) = data(:, 7);
    z_4(:,2) = data(:, 11);
    z_4(:,3) = data(:, 12);
    z_4(:,4) = data(:, 13);
    z_4(:,5) = data(:, 17);
    
    % Average of zone 4
    z_4(:,1) = mean(z_4,2);
    
% Zone 5 ------------------------------------
    z_5(:,1) = data(:, 5);
    z_5(:,2) = data(:, 10);
    z_5(:,3) = data(:, 15);
    
    % Average of zone 5
    z_5(:,1) = mean(z_5,2);
 
% All Averages ------------------------------
    zone(:,1) = z_1(:,1);
    zone(:,2) = z_2(:,1);
    zone(:,3) = z_3(:,1);
    zone(:,4) = z_4(:,1);
    zone(:,5) = z_5(:,1);
    
    z_1 = [];
    z_2 = [];
    z_3 = [];
    z_4 = [];
    z_5 = [];

alpha = 0.05; max_lag = 10; 

% x = zone(2:50,c); % comparing c zone
% y = zone(2:50,d); % with d zone
% fstat_value = granger_cause(x, y, alpha, max_lag);

SE1 = []; CV = [];
Fs = 250;
oneEpoch = Fs*8;
[~,col] = size(zone); %(Value assigned to row is unused so replaced w ~)
rowS = Fs*660; % 11 mins if Fs=250Hz
newDat = zeros(oneEpoch,col);
% for each epoch
for v = 1:floor(rowS/(oneEpoch))
    % for each electrode 
    for l = 1:col
        newDat(1:oneEpoch,l) = zone((v-1)*oneEpoch+1:v*oneEpoch,l);
    end
    E = newDat;
    
    % Number of rows 
    N = size(E,1);

    x = E(1:N,c); % comparing c zone
    y = E(1:N,d); % with d zone
    [fstat_value,c_v] = granger_cause(x, y, alpha, max_lag);
    
    SE1 = [SE1, fstat_value];
    CV = [CV, c_v];
    
    for k = 1:length(SE1)
        if SE1(k) > CV(k)
            Test(k) = 1;
        else
            Test(k) = 0;
        end
    end
end
%SE1 = mean(SE1);
%CV = mean(CV);
