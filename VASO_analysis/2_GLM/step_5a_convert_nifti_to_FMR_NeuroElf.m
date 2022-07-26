clear all
clc
% P04, P03, P02, P05 and P06
subj={'05', '06'};
cond={'standard'};

for iterSbj=1:length(subj)
    for iterCond=1:length(cond)
        % set path with nii files
        PathIn = ['D:\Pilot_Exp_VASO\pilotAOM\sub-' num2str(subj{iterSbj}) '\derivatives\func\AOM\vaso_analysis\' cond{iterCond} '\boco'];

        if exist(PathIn, 'dir')
            PathOut =['D:\Pilot_Exp_VASO\pilotAOM\sub-' num2str(subj{iterSbj}) '\derivatives\func\AOM\vaso_analysis\' cond{iterCond} '\GLM'];

            if ~exist(PathOut, 'dir')
                mkdir(PathOut)
            end

            % set fmr names
            components = {'BOLD_interp', 'VASO_interp_LN'};

            % define number of runs
            nr_fmrs = length(components);

            % deduce motion corrected *.nii names
            for i=1:nr_fmrs
                nii_names{i}=fullfile(PathIn,[components{i} '.nii']);
            end

            % convert nii to fmr
            for i=1:nr_fmrs;
                % create temporary nii
                tempnii=xff(nii_names{i});
                % Convert .nii  to .fmr
                tempfmr=tempnii.Dyn3DToFMR;
                data = tempfmr.Slice.STCData;
                data = flip(data,2);
                % This is necessary to flip the y axis
                % save

                if (i == 2)
                    data = flip(data,2)*30000;
                    %     data = data*30000;
                else
                    data = flip(data,2);
                end

                tempfmr.Slice.STCData = data;
                tempfmr.SaveAs(fullfile(PathOut,[components{i} '_NeuroElf.fmr']))
            end
        end
    end
end
