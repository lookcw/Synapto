figure
for k = 1:82
    ep = bhat(:,4,k);
    subplot(9,10,k)
    plot(1:length(ep),ep)
    ylim([-80,80])
end