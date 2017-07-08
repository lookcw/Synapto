% With a file that corresponds to:
%   Columns 2-8 = data (in neuronetrix case: 7 electrodes outputting in mV)
% This function outputs a vector in this form:
%   [[AOC of 5 bands for electrode 1],...,[AOC of 5 bands for electrode 7]]

function [AOC] = AOCbands(filename)
if exist('dat','var')~=1 %checks to see if dat is not a variable
    dat = importdata(filename); %if not, downloads it from this file
    dat = dat(:,1:8); %sets dat equal to all rows of columns 1-8 of the file
end
Fs = 250; %sampling frequency
AOC = [];

bandst = [.5, 3, 8,  12, 38]; %start frequency of each band
banden = [3,  8, 12, 38, 42]; %end frequency of each band
for k = 2:8
    %Conducts the fft and shifts it to the proper location
    N = length(dat(:,k)); 
    df = Fs/N;
    n = (-(N/2):(N/2)-1)*df;
    Y = abs(fft(dat(:,k))/N);
    Y2 = abs(fftshift(Y)/N); %finalized position of fft
    
    bnd = zeros(1,5);
    for band = 1:5
        %Isolates a band for analysis 
        [~,inds] = min(abs(n-bandst(band))); %inds = closest value to band start in n
        [~,inde] = min(abs(n-banden(band))); %inde = closest value to band end in n
        stI = find(n==n(inds)); %stI = index of closest value
        enI = find(n==n(inde)); %enI = index of closest value
        Xa = n(stI:enI); %Xa = n from band start to band end
        Ya = Y2(stI:enI); %Ya = Y2 from when n = band start to band end

        %Area under curve for isolated band
        bnd(band) = trapz(Xa,Ya); %with no function, this is the AOC method that works for raw data (uses trapezoids with data points)
    end
    AOC = [AOC,bnd];
end