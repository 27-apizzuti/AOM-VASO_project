addpath(genpath('D:\Pilot_Exp_VASO\AOM-project')); % contains .m function

SUBJ='sub-06';

pathIn=['D:\Pilot_Exp_VASO\pilotAOM\' SUBJ '\sourcedata\session1\NIFTI\func'];

pathOUT=['D:\Pilot_Exp_VASO\pilotAOM\' SUBJ '\sourcedata\session1\NIFTI\func\vaso'];

func_basename=[SUBJ '_task-aom_acq-3dvasog3_run-'];

cd(pathIn) % working inside the data folder

nRuns=[1:4];
noiseVol=2;
%% After NORDIC -- remove noise volumes

for itFiles=1:length(nRuns)
     data=[func_basename, '0', num2str(itFiles), '.nii'];
     func=xff(fullfile(pathIn, data));
     
     func.VoxelData=func.VoxelData(:,:,:,1:end-noiseVol); %excluding the last volume = noise
     func.ImgDim.Dim(5)=size(func.VoxelData,4);
     
     func.SaveAs(fullfile(pathOUT, [data(1:end-4),'_noNOISE.nii']))
     
     
     
     clear func
end