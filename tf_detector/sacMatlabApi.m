function [sacOutputSpeed] = sacMatlabApi(rpmSpeed)
%% SETUP
pyversion
sacPath = fileparts(which('main.py'))

if count(py.sys.path,sacPath) == 0
    insert(py.sys.path,int32(0),sacPath);
end
%% Run python script
img_route = "test_imgs/1.png"
sacSpeed = 15 %km/h
pyOut = py.main.predict(pyargs('img_route', img_route, 'speed', sacSpeed));
action = pyOut{1};
disp(action(:))

sacOutputSpeed = 0;

if action == "down15"
    % 15 km/h
    sacOutputSpeed = 368.59; %rpm
elseif action == "down10"
    % 10 km/h
    sacOutputSpeed = 275.42; %rpm
else 
    % 5 km/h
    sacOutputSpeed = 122.86; %rpm
end
