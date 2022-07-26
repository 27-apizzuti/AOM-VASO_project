clear all; clc;
% Run sub-04, sub-03, sub-02
% %% PART 1: Add noise volumes at the end of the functional run using neuroelf
% SUBJ='sub-03';
% pathIN=['D:\Pilot_Exp_VASO\pilotAOM\' SUBJ '\sourcedata\session1\NIFTI\func'];
% pathNORDIC=['D:\Pilot_Exp_VASO\pilotAOM\' SUBJ '\derivatives\func\AOM\NORDIC\data4nordic'];
% 
% func_basename=[SUBJ '_task-aom_acq-3dvasog3_run-'];
% noise_basename= [SUBJ '_task-NOISE_acq-3dvasog3_run-00'];
% 
% 
% noise_M=xff(fullfile(pathIN,[noise_basename '.nii']));
% noise_P=xff(fullfile(pathIN,[noise_basename '_ph.nii']));
% 
% % this folder can contain also motion corrected data (Renzo's pipeline) to apply NORDIC as pilot02
% if ~exist(pathNORDIC, 'dir')
%     mkdir(pathNORDIC)
% end
% 
% nRuns=3;
% for itRun=1:nRuns
%     
%     disp(['Run ', num2str(itRun) ' : adding noise volumes at the end of func data....']);
%     
%     % Before NORDIC Add noise volumes at the end of funct. magnitude and phase data
%     
%     % === magnitude 
%     func_M=xff(fullfile(pathIN, [func_basename, '0' num2str(itRun),'.nii']));
%     tempM=cat(4,func_M.VoxelData, noise_M.VoxelData(:,:,:,1));
% 
%     func_M.VoxelData=tempM;
%     func_M.ImgDim.Dim(5)=size(tempM,4);
%     func_M.SaveAs(fullfile(pathNORDIC, [func_basename, '0' num2str(itRun),'_1noiseVols.nii']));
%     
%     % === phase
%     func_P=xff(fullfile(pathIN, [func_basename, '0' num2str(itRun),'_ph.nii']));
%     tempP=cat(4,func_P.VoxelData, noise_P.VoxelData(:,:,:,1));
% 
%     func_P.VoxelData=tempP;
%     func_P.ImgDim.Dim(5)=size(tempP,4);
%     func_P.SaveAs(fullfile(pathNORDIC, [func_basename, '0' num2str(itRun),'_ph_1noiseVols.nii']) );
% 
% 
% end
% 

%% PART 2: Running NORDIC
addpath(genpath('D:\Pilot_Exp_VASO\AOM-project')); % contains .m function

SUBJ='sub-05';

pathNORDIC=['D:\Pilot_Exp_VASO\pilotAOM\' SUBJ '\sourcedata\session1\NIFTI\func'];

pathOUT=['D:\Pilot_Exp_VASO\pilotAOM\' SUBJ '\derivatives\func\AOM\NORDIC\output'];

func_basename=[SUBJ '_task-aom_acq-3dvasog3_run-'];

cd(pathNORDIC) % working inside the data folder

nRuns=[1:4];

cond={'magn and phase'}; % only magnitude, 'magn and phase'

%% Execute

for iterRuns=1:length(nRuns)
    
    for itCond=1:length(cond)
        
        condition=cond{itCond};
        
        disp(['Starting NORDIC with noise for run '  num2str(iterRuns), ' condition: ' condition]);
        
        switch condition
            
            case 'magn and phase'
                
                ARG.save_add_info=1;
                ARG.noise_volume_last=2;
                ARG.NORDIC=1; % threshold based on Noise
                
                fn_magn_in=[func_basename, '0' num2str(nRuns(iterRuns)) '.nii'];
                fn_phase_in=[func_basename, '0' num2str(nRuns(iterRuns)) '.nii'];
                
                nord_out_dir=[pathOUT '\magn_phase'];
                
                if ~exist(nord_out_dir, 'dir')
                    mkdir(nord_out_dir)
                end
                
%                 fn_out=fullfile(nord_out_dir, ['NORDIC_MP_' fn_magn_in(1:end-4)]);
                fn_out=['NORDIC_MP_' fn_magn_in(1:end-4)];
                NIFTI_NORDIC(fn_magn_in,fn_phase_in,fn_out,ARG)
                
            case 'only magnitude'
                
                ARG.save_add_info =1;
%                 ARG.noise_volume_last=1; % commented only for p02
                ARG.magnitude_only=1;
                
%                 fn_magn_in=[func_basename, '0' num2str(nRuns(iterRuns))
%                 '_1noiseVols.nii']; % commented only for p02
                fn_magn_in=[func_basename, '0' num2str(nRuns(iterRuns)) '.nii'];
                fn_phase_in=fn_magn_in;
                
                if ~exist([pathOUT '\magn_only'], 'dir')
                    mkdir([pathOUT '\magn_only'])
                end
                fn_out=['NORDIC_M_' fn_magn_in(1:end-4)];
                
                NIFTI_NORDIC(fn_magn_in,fn_phase_in,fn_out,ARG)
                
        end
        
        clear ARG
    end
    disp(['----------------------------------------------------------------']);
end

disp('Done.')

%% After NORDIC -- remove noise volumes
pathNORDIC=['D:\Pilot_Exp_VASO\pilotAOM\' SUBJ '\derivatives\func\AOM\NORDIC\output\magn_phase\noiseAdded'];
pathOUT=['D:\Pilot_Exp_VASO\pilotAOM\' SUBJ '\derivatives\func\AOM\NORDIC\output\magn_phase'];
noise_vols=2;
cd(pathNORDIC)
files=dir(['NORDIC' '*.nii']);
for itFiles=1:length(files)
    
     func=xff(files(itFiles).name);
     
     func.VoxelData=func.VoxelData(:,:,:,1:end-noise_vols); %excluding the noise volume 
     func.ImgDim.Dim(5)=size(func.VoxelData,4);
     func.SaveAs(fullfile(pathOUT, files(itFiles).name))
     
     
     
     clear func
end