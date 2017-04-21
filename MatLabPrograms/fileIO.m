  files = dir(fullfile('sample_data\','*.txt'));
  fileID = fopen('exp.txt','a');
   e=exist('B','var')
   
   if exist('TestAnalysis','var')~= 1
   	TestAnalysis = importdata('TestAnalysis.txt');
    TestAnalysis = B(1:52392 , 1:9);
   end
for file = files'
    disp('new try')
    delimiterIn = ',';
    baseFileName=file.name
    fullFileName = fullfile('sample_data\', baseFileName);
    headerlinesIn = 0;
    e=exist('A','var')
    e
    if e ~= 1
	A = importdata(fullFileName)
    end

    dlmwrite('myFile.txt',A,'newline','pc')
   % A=A(1:52392,1:9)
end

