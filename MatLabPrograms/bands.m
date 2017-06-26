% With a file that corresponds to:
%   Column 1 = time (in neuronetrix case: -200 to 1000 ms after stimulus)
%   Columns 2-8 = data (in neuronetrix case: 7 electrodes outputting in mV)
% This function will output a matrix in this form:
%     Column 1      = time (exactly the same as column 1 of the input file)
%     Columns 2-8   = delta bands of each electrode from input file
%     Columns 9-15  = theta bands of each electrode from input file
%     Columns 16-22 = alpha bands of each electrode from input file
%     Columns 23-29 = beta bands of each electrode from input file
%     Columns 30-36 = gamma bands of each electrode from input file

function [bands] = bands(filename)
if exist('csv0','var')~=1
    csv0 = importdata(filename);
    csv0 = csv0(:,1:8);
end
Fs = 250;  % Sampling Frequency
dens = 20; % Density Factor

delta = zeros(length(csv0(:,1)),7);
theta = zeros(length(csv0(:,1)),7);
alpha = zeros(length(csv0(:,1)),7);
beta  = zeros(length(csv0(:,1)),7);
gamma = zeros(length(csv0(:,1)),7);


for k = 1:7
    
%DELTA
Fstop1 = 0;             % First Stopband Frequency
Fpass1 = 1;             % First Passband Frequency
Fpass2 = 2.8;             % Second Passband Frequency
Fstop2 = 4;             % Second Stopband Frequency
Dstop1 = 0.01;            % First Stopband Attenuation
Dpass  = 0.057501127785;  % Passband Ripple
Dstop2 = 0.01;            % Second Stopband Attenuation
[N, Fo, Ao, W] = firpmord([Fstop1 Fpass1 Fpass2 Fstop2]/(Fs/2), [0 1 0], [Dstop1 Dpass Dstop2]);
b  = firpm(N, Fo, Ao, W, {dens});

delta(:,k) = filter(b,1,csv0(:,k+1));

%THETA
Fstop1 = 1.6;             % First Stopband Frequency
Fpass1 = 3.2;             % First Passband Frequency
Fpass2 = 7.8;             % Second Passband Frequency
Fstop2 = 9.4;             % Second Stopband Frequency
Dstop1 = 0.01;            % First Stopband Attenuation
Dpass  = 0.057501127785;  % Passband Ripple
Dstop2 = 0.01;            % Second Stopband Attenuation
[N, Fo, Ao, W] = firpmord([Fstop1 Fpass1 Fpass2 Fstop2]/(Fs/2), [0 1 0], [Dstop1 Dpass Dstop2]);
b  = firpm(N, Fo, Ao, W, {dens});

theta(:,k) = filter(b,1,csv0(:,k+1));

%ALPHA
Fstop1 = 6.6;             % First Stopband Frequency
Fpass1 = 8.2;             % First Passband Frequency
Fpass2 = 11.8;            % Second Passband Frequency
Fstop2 = 13.4;            % Second Stopband Frequency
Dstop1 = 0.01;            % First Stopband Attenuation
Dpass  = 0.057501127785;  % Passband Ripple
Dstop2 = 0.01;            % Second Stopband Attenuation
[N, Fo, Ao, W] = firpmord([Fstop1 Fpass1 Fpass2 Fstop2]/(Fs/2), [0 1 0], [Dstop1 Dpass Dstop2]);
b  = firpm(N, Fo, Ao, W, {dens});

alpha(:,k) = filter(b,1,csv0(:,k+1));

%BETA
Fstop1 = 10.6;            % First Stopband Frequency
Fpass1 = 12.2;            % First Passband Frequency
Fpass2 = 37.8;            % Second Passband Frequency
Fstop2 = 39.4;            % Second Stopband Frequency
Dstop1 = 0.01;            % First Stopband Attenuation
Dpass  = 0.057501127785;  % Passband Ripple
Dstop2 = 0.01;            % Second Stopband Attenuation
[N, Fo, Ao, W] = firpmord([Fstop1 Fpass1 Fpass2 Fstop2]/(Fs/2), [0 1 0], [Dstop1 Dpass Dstop2]);
b  = firpm(N, Fo, Ao, W, {dens});

beta(:,k) = filter(b,1,csv0(:,k+1));

%GAMMA
Fstop1 = 36.6;            % First Stopband Frequency
Fpass1 = 38.2;            % First Passband Frequency
Fpass2 = 41.8;            % Second Passband Frequency
Fstop2 = 43.4;            % Second Stopband Frequency
Dstop1 = 0.01;            % First Stopband Attenuation
Dpass  = 0.057501127785;  % Passband Ripple
Dstop2 = 0.01;            % Second Stopband Attenuation
[N, Fo, Ao, W] = firpmord([Fstop1 Fpass1 Fpass2 Fstop2]/(Fs/2), [0 1 0], [Dstop1 Dpass Dstop2]);
b  = firpm(N, Fo, Ao, W, {dens});

gamma(:,k) = filter(b,1,csv0(:,k+1));

end

bands = [csv0(:,1),delta,theta,alpha,beta,gamma];
