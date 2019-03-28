
dP=[]; tP=[]; aP=[]; bP=[];
for k = 1:12
    E = DhruvTest(1+((k-1)*2550):2551+((k-1)*2550),:);
    
    dP = [dP;bandpower(E,Fs,[1,3])];
    tP = [tP;bandpower(E,Fs,[3,8])];
    aP = [aP;bandpower(E,Fs,[8,12])];
    bP = [bP;bandpower(E,Fs,[12,35])];
    
end
figure
for k = 1:8
    subplot(2,4,k)
    plot(1:length(dP(:,1)),dP(:,k)); hold on
    plot(1:length(tP(:,1)),tP(:,k))
    plot(1:length(aP(:,1)),aP(:,k))
    plot(1:length(bP(:,1)),bP(:,k))
    ylim([0,1500]);
    xlim([0,13]); legend('\delta','\theta','\alpha','\beta');
    title(strcat('Electrode',num2str(k)));
end
