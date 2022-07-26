
mainPath = '/Volumes/Elements/AOM/P02_Pilot/';
file = uigetfile('*.log');
fid = fopen(fullfile(mainPath,'Stim/Logging', file));
tmp = textscan(fid,'%s','delimiter','\n');%This just reads every line
hdr_str = tmp{1};
fclose(fid);

% extract on-offset info from each condition

keyword = 'CondStat';
pos = find(contains(hdr_str,keyword)==1);
posTR = pos-1;
tmp = hdr_str(posTR);

statInit = zeros(numel(posTR),1);
for ff=1:numel(tmp)
   posSpace = find(isspace(tmp{ff})==1);
   statInit(ff) = str2double(tmp{ff}(posSpace(end):end));  
end

keyword = 'CondCenter';
pos = find(contains(hdr_str,keyword)==1);
posTR = pos-1;
tmp = hdr_str(posTR);

centerInit = zeros(numel(posTR),1);
for ff=1:numel(tmp)
    posSpace = find(isspace(tmp{ff})==1);
    centerInit(ff) = str2double(tmp{ff}(posSpace(end):end));  
end

statInit(2:end) = statInit(2:end)+1;
statOnOff = [statInit(1:end-1) centerInit];
statOnOff = [statOnOff; statInit(end) statInit(end)+diff(statOnOff(end,:))];
centerOnOff = [centerInit+1 statInit(2:end)-1];


keyword = 'Keypress: 1'; % target
pos = find(contains(hdr_str,keyword)==1);
posTR = pos-1;
tmp = hdr_str(posTR);
targetInit = zeros(numel(posTR),1);
for ff=1:numel(tmp)
    if isempty(tmp{ff})
        tmp(ff) = hdr_str(posTR(ff)-2);
    end
    posSpace = find(isspace(tmp{ff})==1);
    targetInit(ff) = str2double(tmp{ff}(posSpace(end):end));  
end

targetOnOff = [targetInit targetInit+1];


% for saving as prt file
allCond = {statOnOff, centerOnOff, targetOnOff};
condNames = {'Static','Center','Target'};
colors = [192 192 192;
          255 0 0;
          0 255 255];
      
prtFile = xff('new:prt'); % create empty object
% insert data
prtFile.NrOfConditions = numel(allCond);
for nn=1:prtFile.NrOfConditions
    name = condNames{nn};
    prtFile.Cond(nn).ConditionName = {name};
    prtFile.Cond(nn).NrOfOnOffsets = size(allCond{nn},1);
    prtFile.Cond(nn).OnOffsets = allCond{nn};
    prtFile.Cond(nn).Color = colors(nn,:);
    prtFile.Cond(nn).Weights = zeros(size(allCond{nn},1),0);
end
prtFile.ResolutionOfTime = 'Volumes';
prtFile.Experiment = 'MT_Localizer';
prtFile.ParametricWeights =  0;
prtFile.FileVersion = 2;
prtFile.SaveAs(fullfile(mainPath,[prtFile.Experiment '.prt']))

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
legend(hB,condNames)
xlabel('time in vol')
title('Run1')
exportgraphics(figH,fullfile(mainPath, 'P02_Pilot_MT_Localizer.png'),'Resolution',300)

