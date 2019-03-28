[samp,epoch,elec,pat] = size(HCEp);
rN = 3;
a = 1; b = 1; ART2 = []; CLE2 = [];
figure
for p = 1:pat
    disp(strcat('Patient #',num2str(p),' / ',num2str(pat)));
    for r = [4,16]
        
        x = ADEp(:,:,r,p);
        
        ra = sort(randperm(epoch,rN),'ascend');
        y = 1;
        for k = ra
            subplot(2,rN,y)
            plot(linspace(0,length(x(:,k))/250,length(x(:,k))),x(:,k))
            xlim([0,8]); ylim([-80,80]);
            title(strcat(num2str(k),'---',num2str(std(x(:,k)))));
            y = y+1;
        end
        ar = input('Artifacts: ');
        
        for l = 1:rN
            if ar(l) == 1
                ART2(a,:) = ADEp(:,ra(l),r,p);
                a = a+1;
            end
            if ar(l) == 0
                CLE2(b,:) = ADEp(:,ra(l),r,p);
                b = b+1;
            end
        end
        
    end
end

%%
CleN = [CLE;CLE2];
for n = 1:size(CleN,1)
    Ind0{n} = '-';
end
Ind0 = string(Ind0);
CleN = [CleN,Ind0'];

ArtN = [ART;ART2];
for n = 1:size(ArtN,1) 
    Ind1{n} = '+';
end
Ind1 = string(Ind1);
ArtN = [ArtN,Ind1'];

%%
des = [CleN;ArtN];

% Labels -----------------
labels = {};
for k = 1:size(des,2)-1
    labels{k} = strcat('col',num2str(k));
end
labels{size(des,2)} = 'Indicator';
labels = string(labels);


% Descriptor Matrix ------
labdesc = [labels;des];
fid=fopen('ArtS.csv','wt');
[rows,cols]=size(labdesc);
for k = 1:rows
    fprintf(fid,'%s,',labdesc{k,1:end-1});
    fprintf(fid,'%s\n',labdesc{k,end});
end
fclose(fid);