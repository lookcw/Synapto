function fil = Mat2csv(mat,num)
nam = strcat('file00',num2str(num));
fil = csvwrite(nam,mat);