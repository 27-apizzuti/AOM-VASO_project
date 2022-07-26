clear;

fileID = fopen('NT.txt','r');
nTRs = fscanf(fileID, '%f'); %contiene il n. di volumi per ciascun file 

files=dir(['Basis' '*_*.nii']);

allFiles=[]; allFiles_a=[]; allFiles_b=[];
for runs=1:length(files) %8 volte complessivamente, 4a e 4b

    nTR=nTRs(runs);
    if mod(nTR,2) ==1 %se sono dispari, li rendo pari considerando un volume in meno
        nTR=nTR-1; %make it to be even number
    end
    if mod(runs,2) ==1
        base=files(runs).name;
        for TR= 1:nTR
            inst={[base ',' num2str(TR)]};
            allFiles_a=[allFiles_a; inst];
        end
    elseif mod(runs,2)==0
        base=files(runs).name;
         for TR= 1:nTR
            inst={[base ',' num2str(TR)]};
            allFiles_b=[allFiles_b; inst];
        end
    end


end
allFiles_a = allFiles_a(1:2:end,:);  % odd matrix
allFiles_b = allFiles_b(2:2:end,:);  % even matrix

allFiles_a={allFiles_a};
allFiles_b={allFiles_b};



for bases=1:2
    if bases ==1
        Dataprefix=['Not_Nulled_'];
        allFiles=allFiles_a;
    elseif bases==2
        Dataprefix=['Nulled_'];
        allFiles=allFiles_b;
    end
    matlabbatch{bases}.spm.spatial.realign.estwrite.data = allFiles;
    matlabbatch{bases}.spm.spatial.realign.estwrite.eoptions.quality = 1;
    matlabbatch{bases}.spm.spatial.realign.estwrite.eoptions.sep = 1.2;
    matlabbatch{bases}.spm.spatial.realign.estwrite.eoptions.fwhm = 1;
    % if you want to use the first, use rtm = 0, if you want to use the mean use rtm = 1
    matlabbatch{bases}.spm.spatial.realign.estwrite.eoptions.rtm = 0;
    matlabbatch{bases}.spm.spatial.realign.estwrite.eoptions.interp = 4; %% 4
    matlabbatch{bases}.spm.spatial.realign.estwrite.eoptions.wrap = [0 0 0];
%     matlabbatch{bases}.spm.spatial.realign.estwrite.eoptions.weight = {'moma.nii'};
    matlabbatch{bases}.spm.spatial.realign.estwrite.roptions.which = [2 1];
    matlabbatch{bases}.spm.spatial.realign.estwrite.roptions.interp = 4; %% 4
    matlabbatch{bases}.spm.spatial.realign.estwrite.roptions.wrap = [0 0 0];
    matlabbatch{bases}.spm.spatial.realign.estwrite.roptions.mask = 1;
    matlabbatch{bases}.spm.spatial.realign.estwrite.roptions.prefix = Dataprefix;


end



spm('defaults','FMRI')
spm_jobman('initcfg');
spm_jobman('run',matlabbatch);


% Plot
rp_basis_0a = importdata('rp_Basis_0a.txt');
rp_basis_0b = importdata('rp_Basis_0b.txt');

figure('units','normalized','outerposition',[0 0 1 1]);
sgtitle('Motion across timesteps-Translation','FontSize', 20)

plot(rp_basis_0a(:,1),'g' ,'LineWidth',2)
hold on
plot(rp_basis_0a(:,2),'r' ,'LineWidth',2)
hold on
plot(rp_basis_0a(:,3),'b' ,'LineWidth',2)
hold on
plot(rp_basis_0b(:,1),'m','LineWidth',2)
hold on
plot(rp_basis_0b(:,2), 'c' ,'LineWidth',2)
hold on
plot(rp_basis_0b(:,3),'k' ,'LineWidth',2)
legend({'Not nulled x', 'Not nulled y', 'Not nulled z', 'Nulled x', 'Nulled y', 'Nulled z'})
xlabel('Time [TR]','FontSize', 20)
ylabel('Displacement in mm', 'FontSize', 20)
saveas(gcf,'Motion across timesteps_Translation.jpg');
saveas(gcf,'Motion across timesteps_Translation.fig');
close all;

figure('units','normalized','outerposition',[0 0 1 1]);
sgtitle('Motion across timesteps-Rotation','FontSize', 20)

plot(rp_basis_0a(:,4),'g' ,'LineWidth',2)
hold on
plot(rp_basis_0a(:,5),'r' ,'LineWidth',2)
hold on
plot(rp_basis_0a(:,6),'b' ,'LineWidth',2)
hold on
plot(rp_basis_0b(:,4),'m','LineWidth',2)
hold on
plot(rp_basis_0b(:,5), 'c' ,'LineWidth',2)
hold on
plot(rp_basis_0b(:,6),'k' ,'LineWidth',2)
legend({'Not nulled pitch (x)', 'Not nulled roll (y)', 'Not nulled yaw (z)','Nulled pitch (x)', 'Nulled roll (y)', 'Nulled yaw (z)'})
xlabel('Time [TR]','FontSize', 20)
ylabel('Displacement in degrees', 'FontSize', 20)
saveas(gcf,'Motion across timesteps_Rotation.jpg');
saveas(gcf,'Motion across timesteps_Rotation.fig');


exit
