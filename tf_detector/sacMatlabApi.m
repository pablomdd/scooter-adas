function [sacOutputSpeedRpm] = sacMatlabApi(rpmSpeed)
%% SETUP
clear all;
pyversion
sacPath = fileparts(which('main.py'))

if count(py.sys.path,sacPath) == 0
    insert(py.sys.path,int32(0),sacPath);
end
%% Run python script
img_route = "test_imgs/25.png"
sacSpeed = 20 %km/h
r = 0.2159; %m
sacSpeedRpm = sacSpeed / (r*0.1885)
assignin('base','sacSpeedRpm', sacSpeedRpm);

pyOut = py.main.predict( ...
    pyargs('img_route', img_route, ...
            'speed', sacSpeed));
action = pyOut{1};
disp(action(:))

%% Processing Python output to simulink

% Output speed placeholder
sacOutputSpeedRpm = 0;
if action == "down15"
    % 15 km/h
    sacOutputSpeedRpm = 368.59; %rpm
elseif action == "down10"
    % 10 km/h
    sacOutputSpeedRpm = 245.72; %rpm
elseif action == "down5" 
    % 5 km/h
    sacOutputSpeedRpm = 122.86; %rpm
else 
    % 0 km/h
    sacOutputSpeedRpm = 0; %rpm
end
% Save rpm speed programatically in the workspace
assignin('base','sacOutputSpeedRpm', sacOutputSpeedRpm)
%% Call simulink BLDC sacOutputSpeedRpmsimulation.
sim("BLDC_PWM_control.slx")

return