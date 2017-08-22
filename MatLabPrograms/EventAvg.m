% With file 1 corresponding to:
%   Rows 1-256 = data
% And file 2 corresponding to:
%   Column 1 = event number (1-500)
%   Column 2 = tone type (1 or 0)
%   Column 3 = button pushed (1 or 0)
% This fuction will output two matrices (Standard and Target) each in this form:
%   Column 1 = time (-200 to 1000 ms after tone, 4 ms increments)
%   Columns 2-257 = averaged event data for a single electrode

function [Stan,Targ] = EventAvg(filename1,filename2)
if exist('ST','var')~=1
    ST = importdata(filename1);
    cat = ST.Category_1;
    din = ST.DIN_1;
end
if exist('BEvent','var')~=1
    BEvent = importdata(filename2);
    Btype = BEvent.data;
end

times = 1:length(din);
for k = 1:length(din)
    times(k) = din{4,k};
end

t = linspace(1/250,length(cat(1,:))/250,length(cat(1,:)))';

avgtarg = zeros(301,256);
avgstan = zeros(301,256);
normtarg = avgtarg;
normstan = avgstan;

for v = 1:256
    E1 = cat(v,:)';
    p = polyfit(t,E1,6);
    reg = polyval(p,t);
    E1n = E1-reg;

    % stores 500 events from single electrode
    events = zeros(301,500);
    for k = 1:500
        events(:,k) = E1n(times(k)-50:times(k)+250);
    end

    % Stores target tones into matrix targ and standard tones into stan
    n = 1; m = 1;
    for k = 1:500
        if Btype(k,2)==1 && Btype(k,3)~=0
            targ(:,n) = events(:,k);
            n = n+1;
        end
        if Btype(k,2)==0 && Btype(k,3)==0
            stan(:,m) = events(:,k);
            m = m+1;
        end
    end

    % Averages
    for k = 1:301
        avgtarg(k,v) = mean(targ(k,:));
    end
    for k = 1:301
        avgstan(k,v) = mean(stan(k,:));
    end
    
    % Baseline removal ver 1.
    prestimT = avgtarg(1:51,v);
    for k = 1:301
        normtarg(k,v) = avgtarg(k,v) - mean(prestimT);
    end
    prestimS = avgstan(1:51,v);
    for k = 1:301
        normstan(k,v) = avgstan(k,v) - mean(prestimS);
    end
    
    % Baseline removal ver 2.
    %normtarg = avgtarg;
    %for k = 1:301
    %    normtarg(k,v) = avgtarg(k,v) - avgtarg(51,v);
    %end
    %normstan = avgstan;
    %for k = 1:301
    %    normstan(k,v) = avgstan(k,v) - avgstan(51,v);
    %end


    %figure
    %plot(tim,normtarg(:,119))
    %figure
    %plot(tim,normstan(:,119))
end

tim = linspace(-50/0.250,1000,length(normtarg(:,1)))';
Stan = [tim,normstan];
Targ = [tim,normtarg];

