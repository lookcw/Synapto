function [cleandata] = artrem(rawdata)
[w, s] = runica(rawdata);
W = w*s;
activations = W*rawdata;
Winv = inv(W);
cleandata = Winv*activations;
end