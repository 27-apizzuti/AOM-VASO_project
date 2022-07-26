% Script to plot layering profiles
clear all
close all
clc

subj={'sub-02'};
proc={'standard','magn_only'}; % 'standard' or 'magn_only', magn_only_noNOISE
thr=4;
nlay=10;
suff={'0'};         % thresh gm
vox_mask={'0'};     % thresh %signal change maps

PathOut=['D:\Pilot_Exp_VASO\pilotAOM\Results\LP'];

if ~exist(PathOut, 'dir')
       mkdir(PathOut)
end

colorSbj=[1 0 0.5; 0 1 0.8; 0 0 1];

for iterProc=1:size(proc,2)
    
    
%     figure('units','normalized','outerposition',[0 0 1 1]);
    figure
    set(gcf,'color','w')
    axes
    axis('equal')

    
    for iterSbj=1:size(subj,2)
        
        flag=proc{iterProc};
        
            if strcmp(proc{iterProc},'magn_only')
                if iterSbj==2
                    flag='magn_only_noNOISE';
                else
                    flag=proc{iterProc};
                end
            end
        
%         pathIn=['D:\Pilot_Exp_VASO\pilotAOM\' subj{iterSbj} '\derivatives\func\AOM\vaso_analysis\' flag '\LAYERS\scaled_'...
%             num2str(thr) '_nlayers_' num2str(nlay) '_mask_' vox_mask{1} '_thick_' suff{1}];
          pathIn=['D:\Pilot_Exp_VASO\pilotAOM\' subj{iterSbj} '\derivatives\func\AOM\vaso_analysis\' proc{iterProc} '\LAYERS_masked'];

        cond={'allTask', 'Diag45','Diag135','Horizontal','Vertical'};
        
        
        
        for itcond=1:size(cond,1)
            
%             if (vox_mask{1}=='0')
%                 fileBOLD=['scaled_', num2str(thr), '_act_', cond{itcond},...
%                     '_BOLD_n_' num2str(nlay) '_' suff{1} '_layer.dat'];
%                 fileVASO=['scaled_', num2str(thr), '_act_', cond{itcond},...
%                     '_VASO_n_' num2str(nlay) '_' suff{1} '_layer.dat'];
%                 
%             else
%                 fileBOLD=['scaled_', num2str(thr), '_act_', cond{itcond},...
%                     '_BOLD_n_' num2str(nlay) '_' suff{1} '_mask_layer.dat'];
%                 fileVASO=['scaled_', num2str(thr), '_act_', cond{itcond},...
%                     '_VASO_n_' num2str(nlay) '_' suff{1} '_mask_layer.dat'];
%             end

            fileBOLD='BOLD_masked_layers.dat';
            fileVASO='VASO_masked_layers.dat';
            
            dataB=importdata(fullfile(pathIn, fileBOLD));
            dataV=importdata(fullfile(pathIn, fileVASO));
            
            if strcmp(proc{iterProc}, 'standard')
                tit='Standard';
            else
                tit='Nordic';
            end

            % FIG. 1 BOLD
            subplot(1,2,1)
            errorbar(dataB(:,1)*100,dataB(:,2),'Color', colorSbj(iterSbj,:), 'LineWidth', 1.5, 'LineStyle','-');
            xticks([1:nlay])
%             xlabel({'Layers (0=white matter)'},'FontSize',14)
%             ylabel('Percent signal change','FontSize',14)
            legend({'P02', 'P03', 'P04'},'Location','NorthOutside')
            hold on
            
            % FIG. 2 VASO
           
            subplot(1,2,2)
            errorbar(dataV(:,1)*100,dataV(:,2),'Color', colorSbj(iterSbj,:), 'LineWidth', 1.5, 'LineStyle','-')
            xticks([1:nlay])
%             xlabel({'Layers (0=white matter)'},'FontSize',14)
%             ylabel('Percent signal change','FontSize',14)
            legend({'P02', 'P03', 'P04'},'Location','NorthOutside')
            hold on
            
       
        end
        
    end
    
%     saveas(gca,fullfile(PathOut,[tit '_contrast_BOLD_',cond{itcond}]),'jpeg')
%     saveas(gca,fullfile(PathOut,[tit '_contrast__BOLD_',cond{itcond}]),'fig')
   
    
end

