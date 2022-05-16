%% SETUP
pyversion
sacPath = fileparts(which('main.py'))

if count(py.sys.path,sacPath) == 0
    insert(py.sys.path,int32(0),sacPath);
end
%% Run python script
img_route = "test_imgs/1.png"
speed = 15
pyOut = py.main.predict(pyargs('img_route', img_route, 'speed' ,speed));
action = pyOut{1};
pyImg = pyOut{2};
disp(action(:))

%% Read png from filesystem

outputImg = imread("sacOutputImg.png");
imshow(outputImg);

%%  Read output npArray Image

% pyList = cell(pyImg);
% numRows = length(pyList)
% numCols = length(pyList{1})
% 
% matlabImg = zeros(numRows, numCols,3);
% % R = zeros(numRows, numCols);
% % G = zeros(numRows, numCols);
% % B = zeros(numRows, numCols);
% 
% for i = 1:numRows
%     tempRow = cell(pyList{i});
%     for j = 1:numCols
%         pyPixel = cell(tempRow{j});
%         pixel = cellfun(@double, pyPixel);
%         matlabImg(i,j,1) = pixel(1);
%         matlabImg(i,j,2) = pixel(2);
%         matlabImg(i,j,3) = pixel(3);
%         %pyMatrix(i,j) = cell(pyList{i})
%     end
% end




% image = [R, G, B];
% imshow(image)
% 
% for j = 1:numCols
% 
% end
% rows = zeros(1, numRows)
% pyCols = cell(pyRows)
% 
% numCols = length(pyCols)
