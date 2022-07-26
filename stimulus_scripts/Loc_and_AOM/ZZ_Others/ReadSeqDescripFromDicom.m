pathFile = '/Volumes/Elements/AOM/P02_Pilot/DICOM';
coreName = 'RENHUB_20201202.MR.RENZOHUBER_AMAIA.';

temp = dir(fullfile(pathFile, [coreName  '*.IMA']));  
NrOfSets = str2double(temp(end).name(numel(coreName)+1:numel(coreName)+4)); % extract number from last .IMA in directory
nameSeries = cell(NrOfSets,1);
NrOfVol = zeros(NrOfSets,1);
for ff=1:NrOfSets
    if ff<10
        d = dir(fullfile(pathFile, [coreName '000' num2str(ff) '*.IMA']));       
    else
        d = dir(fullfile(pathFile, [coreName '00' num2str(ff) '*.IMA']));
    end
    info = dicominfo(fullfile(pathFile,d(1).name)); %only get info from first file per acquisition

    nameSeries{ff} = [num2str(ff) ' - ' info.SeriesDescription];
    NrOfVol(ff) = numel(d);
end

T = table(nameSeries, NrOfVol);
disp(T)