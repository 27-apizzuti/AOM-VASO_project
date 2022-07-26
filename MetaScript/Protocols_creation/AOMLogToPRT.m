%% Convert .log file into .prt file (BV style)
% Axis of Motion
% We use TR to extract the initial point of the condition
% Start: TR before the label; then 1 empty line to detect the block
clear all;
clc;

% Parameters
subj = 'sub-05';
mainPath = ['D:\Pilot_Exp_VASO\pilotAOM\', subj, '\Protocols'];
outPath = ['D:\Pilot_Exp_VASO\pilotAOM\', subj, '\Protocols'];

%% Execute

colors = [64 64 64;     % fixation
    192 192 192;        % static/flickering dots
    255 0 0;            % horizontal
    0 255 0;            % 45deg
    0 0 255;            % vertical
    255 255 0;          % 135deg
    0 255 255];         % target

plotPRT = 1; % flag to plot prt file and save it

file = dir(fullfile(mainPath,'Logging','*_RndDotMot*.log'));    % load log file

for rr=1:numel(file)
    
    fid = fopen(fullfile(mainPath,'Logging', file(rr).name));
    tmp = textscan(fid,'%s','delimiter','\n');                  % This just reads every line
    logFile = tmp{1};
    fclose(fid);
    
    CondNames = {'CondFix','CondStat','Cond0','Cond45','Cond90','Cond135','Keypress: 1'};
    condInit_all= cell(numel(CondNames),1);
    for cc=1:numel(CondNames)
        
        if cc<numel(CondNames)                          % aom condition
            keyword = CondNames{cc};
            pos = find(contains(logFile,keyword)==1);   % find all locations with keyword (condition name)
            posTR = pos-1;
            tmp = logFile(posTR);
            
            condInit = zeros(numel(posTR),1);
            for ff=1:numel(tmp)
                pos = strfind(tmp{ff},'TR ') + numel('TR ');
                posSpace = find(isspace(tmp{ff})==1);
                condInit(ff) = str2double(tmp{ff}(pos:posSpace(find((posSpace>pos)==1,1,'first'))));
            end
            
            condInit_all{cc} = condInit;
            
        else                                            % target condition
            keyword = CondNames{cc};
            pos = find(contains(logFile,keyword)==1);
            posTR = pos-1;
            %                 tmp = hdr_str(posTR);
            tmp = logFile(posTR);
            targetInit = zeros(numel(posTR),1);
            for ff=1:numel(tmp)
%                 if isempty(tmp{ff})
%                     tmp(ff) = hdr_str(posTR(ff)-2);
%                 end
                pos = strfind(tmp{ff},'TR ') + numel('TR ');
                posSpace = find(isspace(tmp{ff})==1);
                targetInit(ff) = str2double(tmp{ff}(pos:posSpace(find((posSpace>pos)==1,1,'first'))));
            end
            
            targetOnOff = [targetInit targetInit+1];
        end
    end
    
    %%% extract start-end of stimulus presentation %%%
    
    % Fixation
    
    FixOnOff = zeros(numel(condInit_all{1}),2);
    if numel(condInit_all{1}) ==1
        FixOnOff(1,:) = [1 min([condInit_all{3};condInit_all{4};condInit_all{5};condInit_all{6}])];
    else
        temp = [condInit_all{3};condInit_all{4};condInit_all{5};condInit_all{6}];   % concatenate starting points
        FixOnOff = [1 min(temp)];
        for nn=2:numel(condInit_all{1})-1
            dif = temp - condInit_all{1}(nn);
            val = temp((dif == min(dif(dif>0))));
            FixOnOff(nn,:) = [condInit_all{1}(nn)+1 val];
        end
        FixOnOff(nn+1,:) = [condInit_all{1}(end)+1 condInit_all{1}(end)+1+diff(FixOnOff(nn,:))];
    end
    
    % AOM conditions
    
    TasksOnOff = [sort(([condInit_all{3};condInit_all{4};condInit_all{5};condInit_all{6}])+1) condInit_all{2}];
    TasksIndOnoff = cell(4,1);
    for cc=3:6 % cond0 - cond45 - cond90 - cond135
        TasksIndOnoff{cc-2} = TasksOnOff(ismember(TasksOnOff(:,1),condInit_all{cc}+1),:);
    end
    
    % Static/flickering condition [REST]
    
    FlickerOnoff = zeros(numel(condInit_all{2}),2);
    FlickerOnoff(1:end-1,:) = [condInit_all{2}(1:end-1)+1 TasksOnOff(2:end,1)-1];
    
    if size(FixOnOff,1)>1
        difVal = (FixOnOff(end,1)-1)-(condInit_all{2}(end)+1);
        FlickerOnoff(end,:) = [condInit_all{2}(end)+1 (condInit_all{2}(end)+1+difVal)];
    else
        FlickerOnoff(end,:) = [condInit_all{2}(end)+1 (condInit_all{2}(end)+1+diff(FlickerOnoff(end-1,:)))];
    end
    
    allCond = {FixOnOff, FlickerOnoff, TasksIndOnoff{1},TasksIndOnoff{2},TasksIndOnoff{3},TasksIndOnoff{4}, targetOnOff};
    
    % rename conditions for saving
    CondNames{2} = 'Flicker';
    CondNames{3} = 'Horizontal';
    CondNames{4} = 'Diag45';
    CondNames{5} = 'Vertical';
    CondNames{6} = 'Diag135';
    CondNames{7} = 'Targets';
    
    prtFile = xff('new:prt'); % create empty object
    
    % insert data
    prtFile.NrOfConditions = numel(allCond);
    prtFile.TimeCourseColor = [0 0 0];
    for nn=1:prtFile.NrOfConditions
        name  = CondNames{nn};
        prtFile.Cond(nn).ConditionName = {name};
        prtFile.Cond(nn).NrOfOnOffsets = size(allCond{nn},1);
        prtFile.Cond(nn).OnOffsets = allCond{nn};
        prtFile.Cond(nn).Color = colors(nn,:);
        prtFile.Cond(nn).Weights = zeros(size(allCond{nn},1),0);
        
    end
    prtFile.ResolutionOfTime = 'Volumes';
    prtFile.Experiment = [subj '_AOM_run0' num2str(rr)];
    prtFile.ParametricWeights =  0;
    prtFile.FileVersion = 2;
    prtFile.SaveAs(fullfile(outPath,[prtFile.Experiment '.prt']))
    
    if plotPRT % create prt plot
        figH = figure;
        set(gcf,'color','w')
        oo = prtFile.OnOffsets;
        uOO = unique(oo(:,1));
        for nn=1:numel(uOO)
            pos = oo(oo(:,1)==nn,2:3);
            
            for pp=1:size(pos,1)
                hold all,
                if pp==1
                    hB(nn) = area([pos(pp,1) pos(pp,2)], [1 1]);
                    hB(nn).FaceColor = colors(nn,:)./255;
                end
                hA(pp) = area([pos(pp,1) pos(pp,2)], [1 1]);
                hA(pp).FaceColor = colors(nn,:)./255;
            end
        end
        legend(hB,CondNames)
        xlabel('time in vol')
        title(['Run' num2str(rr)])
        exportgraphics(figH,fullfile(outPath,[prtFile.Experiment '.png']),'Resolution',300)
    end
    clear FlickerOnoff TasksIndOnoff TasksOnOff targetOnOff FixOnOff
end






