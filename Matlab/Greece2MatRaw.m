Fs = 250;

cd MCI_GD
dirs1 = dir(fullfile('.','*.mat'));
%dirs2 = dir(fullfile('.','*.txt'));
x = 1; 
for file1 = dirs1'
    %file2 = dirs2(x);
    filename1 = file1.name;
    %filename2 = file2.name;
    filename1 = fullfile(filename1)
    %filename2 = fullfile(filename2)
    dat = importdata(filename1);
    %ton = importdata(filename2);
    
%     times = 1:length(dat.DIN_1);
%     for k = 1:length(dat.DIN_1)
%         times(k) = dat.DIN_1{4,k};
%     end
    
    %T = linspace(1/250,length(dat.Category_1_Segment1(1,:))/250,length(dat.Category_1_Segment1(1,:)))';
    E = [dat.Category_1_Segment1(124,:);dat.Category_1_Segment1(149,:);dat.Category_1_Segment1(95,:);dat.Category_1_Segment1(178,:);dat.Category_1_Segment1(59,:);dat.Category_1_Segment1(183,:);dat.Category_1_Segment1(47,:);dat.Category_1_Segment1(2,:)]; % O1 O2 T5 T6 C3 C4 F7 F8
    
    %T = linspace(1/250,length(dat.Category_1(1,:))/250,length(dat.Category_1(1,:)))';
    %E = [dat.Category_1(124,:);dat.Category_1(149,:);dat.Category_1(95,:);dat.Category_1(178,:);dat.Category_1(59,:);dat.Category_1(183,:);dat.Category_1(47,:);dat.Category_1(2,:)]; % O1 O2 T5 T6 C3 C4 F7 F8
    
    E1lp = eegfilt(E,Fs,0,35);
    E1 = eegfilt(E1lp,Fs,0.2,0)';
    
%     % Baseline removal
%     len = size(E1,1);
%     base = zeros(len,8);
%     for v = 1:8
%         base(v) = mean(E1(:,v));
%         for k = 1:len
%             E1(k,v) = E1(k,v) - base(v);
%         end
%     end

    if x < 10
        n = strcat('0',num2str(x));
    else
        n = num2str(x);
    end
    
    cd MCI_Total
    dlmwrite(strcat('MCI',n,'.csv'),E1);
    cd ..
    
    x=x+1;
    
end

