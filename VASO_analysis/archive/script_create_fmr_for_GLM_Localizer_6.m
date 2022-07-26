clear all
clc

% P04, P03, P02, P05, P06
subj={'05'};

for iterSbj=1:length(subj)
    
    % set path with nii files
    PathIn = ['D:\Pilot_Exp_VASO\pilotAOM\sub-' num2str(subj{iterSbj}) '\derivatives\func\loc01\BV_GLM'];
    PathOut = PathIn;
    fileList = dir(fullfile(PathIn, '*.nii'));
    components = fileList.name; % only 1 file (warped time series)
    tempnii=xff(fullfile(PathIn, components));
    % Convert .nii  to .fmr
    tempfmr=tempnii.Dyn3DToFMR;
    data = tempfmr.Slice.STCData;
    data = flip(data,2);
    % This is necessary to flip the y axis
    % save
    
    tempfmr.Slice.STCData = data;
    tempfmr.SaveAs(fullfile(PathOut,[components(1:end-4) '_NeuroElf.fmr']))
end


