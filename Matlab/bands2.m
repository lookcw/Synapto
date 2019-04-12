function [delta,theta,alpha,beta,gamma] = bands2(filename)
data = importdata(filename);
Fs = 250;  % Sampling Frequency
%data = data(1:Fs*660,:); %uses 11 minutes
[~,col] = size(data);

dens = 20; % Density Factor

delta = zeros(length(data(:,1)),col);
theta = zeros(length(data(:,1)),col);
alpha = zeros(length(data(:,1)),col);
beta  = zeros(length(data(:,1)),col);
gamma = zeros(length(data(:,1)),col);


for k = 1:col
    
%DELTA
Fstop1 = 0;             % First Stopband Frequency
Fpass1 = 1;             % First Passband Frequency
Fpass2 = 2.8;             % Second Passband Frequency
Fstop2 = 4;             % Second Stopband Frequency
Dstop1 = 0.001;            % First Stopband Attenuation
Dpass  = 0.057501127785;  % Passband Ripple
Dstop2 = 0.001;            % Second Stopband Attenuation
[N, Fo, Ao, W] = firpmord([Fstop1 Fpass1 Fpass2 Fstop2]/(Fs/2), [0 1 0], [Dstop1 Dpass Dstop2]);
b  = firpm(N, Fo, Ao, W, {dens});

delta(:,k) = filter(b,1,data(:,k));

%THETA
Fstop1 = 1.6;             % First Stopband Frequency
Fpass1 = 3.2;             % First Passband Frequency
Fpass2 = 7.8;             % Second Passband Frequency
Fstop2 = 9.4;             % Second Stopband Frequency
Dstop1 = 0.001;            % First Stopband Attenuation
Dpass  = 0.057501127785;  % Passband Ripple
Dstop2 = 0.001;            % Second Stopband Attenuation
[N, Fo, Ao, W] = firpmord([Fstop1 Fpass1 Fpass2 Fstop2]/(Fs/2), [0 1 0], [Dstop1 Dpass Dstop2]);
b  = firpm(N, Fo, Ao, W, {dens});

theta(:,k) = filter(b,1,data(:,k));

%ALPHA
Fstop1 = 6.6;             % First Stopband Frequency
Fpass1 = 8.2;             % First Passband Frequency
Fpass2 = 11.8;            % Second Passband Frequency
Fstop2 = 13.4;            % Second Stopband Frequency
Dstop1 = 0.001;            % First Stopband Attenuation
Dpass  = 0.057501127785;  % Passband Ripple
Dstop2 = 0.001;            % Second Stopband Attenuation
[N, Fo, Ao, W] = firpmord([Fstop1 Fpass1 Fpass2 Fstop2]/(Fs/2), [0 1 0], [Dstop1 Dpass Dstop2]);
b  = firpm(N, Fo, Ao, W, {dens});

alpha(:,k) = filter(b,1,data(:,k));

%BETA
Fstop1 = 10.6;            % First Stopband Frequency
Fpass1 = 12.2;            % First Passband Frequency
Fpass2 = 37.8;            % Second Passband Frequency
Fstop2 = 39.4;            % Second Stopband Frequency
Dstop1 = 0.001;            % First Stopband Attenuation
Dpass  = 0.057501127785;  % Passband Ripple
Dstop2 = 0.001;            % Second Stopband Attenuation
[N, Fo, Ao, W] = firpmord([Fstop1 Fpass1 Fpass2 Fstop2]/(Fs/2), [0 1 0], [Dstop1 Dpass Dstop2]);
b  = firpm(N, Fo, Ao, W, {dens});

beta(:,k) = filter(b,1,data(:,k));

%GAMMA
Fstop1 = 36.6;            % First Stopband Frequency
Fpass1 = 38.2;            % First Passband Frequency
Fpass2 = 50.8;            % Second Passband Frequency
Fstop2 = 52.4;            % Second Stopband Frequency
Dstop1 = 0.001;            % First Stopband Attenuation
Dpass  = 0.057501127785;  % Passband Ripple
Dstop2 = 0.001;            % Second Stopband Attenuation
[N, Fo, Ao, W] = firpmord([Fstop1 Fpass1 Fpass2 Fstop2]/(Fs/2), [0 1 0], [Dstop1 Dpass Dstop2]);
b  = firpm(N, Fo, Ao, W, {dens});

gamma(:,k) = filter(b,1,data(:,k));

end

%bands = [delta,theta,alpha,beta,gamma];
