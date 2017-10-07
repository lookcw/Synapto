function [cleandata] = artrem(rawdata)
[weights,sphere,~,~,~,~,~,~] = runica(rawdata);
W = weights*sphere;
activations = W*rawdata;
Winv = inv(W);
cleandata = Winv*activations;
end