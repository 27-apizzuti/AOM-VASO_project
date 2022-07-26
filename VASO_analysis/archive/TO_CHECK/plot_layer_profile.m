% Script to plot layering profiles
clear all
close all
clc

subj={'sub-02'};
proc={'standard', 'magn_only'}; % 'standard' or 'magn_only', magn_only_noNOISE
thr=4;
nlay=9;
suff={'0'};         % thresh gm
vox_mask={'0'};     % thresh %signal change maps

% if strcmp(proc{1}, 'standard')
%     bold_lineCol = [0.1 0.1 0.75];
%     vaso_lineCol = [0.75 0.1 0.1];
%     
% else
%     bold_lineCol = ([47, 163, 222])./255;
%     vaso_lineCol = ([219, 143, 29])./255;
% end
pathOUT=['D:\Pilot_Exp_VASO\pilotAOM\Results\LP_mask'];
for iterSbj=1:size(subj,2)
    
    figH=figure();
    set(gcf,'color','w')
    
    for iterProc=1:size(proc,2)
        
%         pathIn=['D:\Pilot_Exp_VASO\pilotAOM\' subj{iterSbj} '\derivatives\func\AOM\vaso_analysis\' proc{iterProc} '\LAYERS\scaled_'...
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
                bold_lineCol = [0.1 0.1 0.75];
                vaso_lineCol = [0.75 0.1 0.1];
            else
                tit='Nordic';
                bold_lineCol = ([47, 163, 222])./255;
                vaso_lineCol = ([219, 143, 29])./255;
            end
            
            
            
            errorbar(dataB(:,1)*100,dataB(:,2), 'LineWidth', 2.5, 'LineStyle','-', 'Color', bold_lineCol)
            
            hold on
            errorbar(dataV(:,1)*100,dataV(:,2), 'LineWidth', 2.5, 'LineStyle','-','Color', vaso_lineCol)
            xlim([1 9])
            title('Layer Profile','FontSize', 15)
%             subtitle([tit ' processing (contrast: ' cond{itcond} ' vs Flick)'],'FontSize', 15)
            xlabel({'Layers (0=white matter)'},'FontSize', 15)
%             legend('BOLD','VASO', 'Location','northwest','FontSize', 15)
            ylabel('Percent signal change','FontSize', 15)
            axis square
            hold on 
            ax = gca;
            ax.XGrid = 'off';
            ax.YGrid = 'on';
%             % Plot separate BOLD and VASO
%             figure
%             subplot(1,2,1)
%             set(gcf,'color','w')
%             
%             errorbar(dataB(:,1)*100,dataB(:,2), 'LineWidth', 1.5, 'LineStyle','-')
%             xticks([1:nlay])
%             xlabel({'Layers (0=white matter)'}, 'FontSize', 15)
%             title('BOLD','FontSize', 15)
%             ylabel('Percent signal change','FontSize', 15)
%             subplot(1,2,2)
%             errorbar(dataV(:,1)*100,dataV(:,2), 'LineWidth', 1.5, 'LineStyle','-')
%             title('VASO','FontSize', 15)
%             ylabel('Percent signal change','FontSize', 15)
%             suptitle(['Layer Profile' tit ' processing (contrast: ' cond{itcond} ' vs Flick)'], 'FontSize', 15)
%            
%             xlabel({'Layers (0=white matter)'})
%             xticks([1:nlay])
%             
%             saveas(gca,fullfile(pathIn,[tit '_new_sep_contrast_',cond{itcond}]),'jpeg')
%             saveas(gca,fullfile(pathIn,[tit '_new_sep_contrast_',cond{itcond}]),'fig')
%             saveas(gca,fullfile(pathIn,[tit '_new_sep_contrast_',cond{itcond}]),'svg')
            
        end
%         hold off;
                saveas(gca,fullfile(pathOUT,[subj{iterSbj} '_' tit '_MASK_new_contrast_',cond{itcond}]),'jpeg')
                saveas(gca,fullfile(pathOUT,[subj{iterSbj} '_' tit '_MASK_new_contrast_',cond{itcond}]),'fig')
                saveas(gca,fullfile(pathOUT,[subj{iterSbj} '_' tit '_MASK_new_contrast_',cond{itcond}]),'svg')
% %         figure
%         bar(dataB(:,3))
%         xlabel({'Layers (0=white matter)'})
%         ylabel('#of voxels')
%         saveas(gca,fullfile(pathIn,[tit '_BARplot_contrast_',cond{itcond}]),'jpeg')
        
    end
end