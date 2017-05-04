filePath = fullfile(fileparts(which('PathPlanningExample')),'data','exampleMaps.mat');
load(filePath)


f = imread('playground.pgm');
% f = cat(3, f, f, f);
imshow(f)
f = double(f);
ff = zeros(size(f));
maxVal = max(max(f));

for row = 1:size(f, 1)
    for col = 1:size(f, 2)
        ff(row, col) = f(row, col) / maxVal;
        
    end
end

% for row = 1:size(ff, 1)
%     for

% figure; imshow(f);
%zero is the border, 254 is the path, 205 is the area outside the path
% figure; imshow(f);
% ff = imbinarize(f);
roboRadius = 0.05;

% g = ff(150:300, 300:725);

fff = zeros(size(ff));

for row = 1:size(ff, 1)
    for col = 1:size(ff, 2)
        
        if (ff(row, col) == 1)
            
            fff(row, col) = 0;
            
        elseif(ff(row, col) == 0)
            
            fff(row, col) = 1;
            
        else
            
            fff(row, col) = ff(row, col) - .20;
        end
        
    end
end

% fff = zeros(size(ff,1), size(ff, 2));
% 
% for row = 1:size(fff, 1)
%     for col = 1:size(fff, 2)
%         
%         if (ff(row, col) >= .999)
%             
%             fff(row, col) = 0;
%             
%         elseif (ff(row, col) == 0)
%             fff(row, col) = .999;
%         end
%         
%     end
% end

map = robotics.OccupancyGrid(fff, 20);
map = robotics.BinaryOccupancyGrid(simpleMap, 2);
im = imbinarize(fff);
im = imcomplement(im);
im = bwmorph(im,'thicken',3);
%im = bwmorph(im,'close');
im = bwmorph(im,'clean',1);
im = imcomplement(im);

imshow(im)

dlmwrite('mod_playground.txt',im,'delimiter',' ');

startLocation = [2 1];
endLocation = [12 10];
