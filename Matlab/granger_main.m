% HC ---------------------
cd HC_BD_Fil
dirs = dir(fullfile('.','*.txt'));
grangerHC = zeros(12,82,2);
CVHC = zeros(12,82,2);
TestHC = zeros(12,82,2);

% c and d represent zones
j = 1;
for c = 1:2
    for d = 1:2
        if c == d
            continue; % don't want to compare two same zones 
        end
        
        i = 1;
        for file = dirs'
            filename = file.name;
            filename = fullfile(filename);

            % get fstat value from the two zones and place this value in
            % grangerHC matrix. Each file will have a value (because each
            % file will be getting an fstat value for the two compared
            % zones)
            [grangerHC(i,:,j),CVHC(i,:,j),TestHC(i,:,j)] = grangerFstat(filename,c,d);
            i = i+1;
        end
        j = j+1;
        disp(c);
        disp(d);
    end
end 

cd ..

%% AD ---------------------
cd AD_BD_Fil
dirs = dir(fullfile('.','*.txt'));
grangerAD = zeros(12,82,2);
CVAD = zeros(12,82,2);
TestAD = zeros(12,82,2);

% c and d represent zones
j = 1;
for c = 1:2
    for d = 1:2
        if c == d
            continue; % don't want to compare two same electrodes 
        end
        
        i = 1;
        for file = dirs'
            filename = file.name;
            filename = fullfile(filename);

            [grangerAD(i,:,j),CVAD(i,:,j),TestAD(i,:,j)] = grangerFstat(filename,c,d);
            i = i+1;
        end
        j = j+1;
         disp(c);
         disp(d);
    end
end 

cd ..
%%
% T-Test -----------------
% Null hypthesis = There is no significant difference between HC and AD
% fstats

[rows, cols] = size(grangerHC);
ttest_values = [];

for element = 1:cols
    ad = grangerAD(:,element);
    hc = grangerHC(:,element);
    [h,p] = ttest(ad,hc,'Alpha',0.05)
    ttest_values(element,1) = h;
%     ttest_values(element,2) = p;
    
end 

