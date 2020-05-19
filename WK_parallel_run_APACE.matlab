% In this text I follow an outline based on example code given by Xu Chen et al
% that can be found at http://www.nisox.org/Software/APACE/
%
% Preparation
%
% This is code to reproduce the results seen in Figure 1. 
%_______________________________________________________________________
% Version: http://github.com/nicholst/APACE/tree/34ea883
%          2018-09-21 09:59:07 +0100

% % Uncomment this to hide figures (for the rest of your Matlab session!).
% % This is useful if you don't want to see the large number of figure
% % windows that get created.
set(0, 'DefaultFigureVisible', 'off');
addpath(genpath('~/APACE-0.1.4/')) % see http://www.nisox.org/Software/APACE/

base = '~/participants/';
con_paths = ''; % 'list_con4.txt';
kinship_list = 'zygosity.csv';
results_dir = '~/apace_output';
mask = ''; % '/output.nii';

%%% 1) Create a structure array specifying details of data
ACEfit_Par.Model     = 'ACE';             % Choose a model (AE or ACE) for
                                          % data fitting.


% in this case, each row in the txt is a path to a contrast (CS+US>CS+noUS)
% that was first masked using the Neurologic pain signature (Wager et al. 2013). N Engl J Med 2013; 368:1388-1397. DOI: 10.1056/NEJMoa1204471 
% Using canlab and the apply_mask(dat, nps) command where dat is one individuals contrast image. CANlab tools can be found here: https://canlab.github.io
ACEfit_Par.P_nm      =  fullfile('~/list_con4.txt'); % fullfile(base,conn_paths);
                                          % A list of images or other data
                                          % specification; see
                                          % FileFormats.txt

ACEfit_Par.InfMx     = fullfile('~/zygosity.csv');
                                          % Kinship information CSV file
                                          % with header row and exactly 4
                                          % columns: Subject ID, Mother ID,
                                          % Father ID, and Zygosity. Mother
                                          % ID and Father ID must be
                                          % positive integers, and Zygosity
                                          % is 'MZ', 'NotMZ' or 'NotTwin'.
                                          % The order of subjects must
                                          % match that of image paths or
                                          % subjects in ACEfit_Par.P_nm.

ACEfit_Par.ResDir    =  results_dir;
                                          % Set result folder

%%% The rest are optional; omit to use default values

ACEfit_Par.Subset    = [];                % Set equal to (a subset of)
                                          % subject indicies to be
                                          % considered in the analysis.
                                          % Empty (default) means "all
                                          % subjects".

ACEfit_Par.Pmask     = mask;              % Brain mask image (default:
                                          % whole volume)

ACEfit_Par.Dsnmtx    = '';                % Design matrix (default:
                                          % all-ones vector)

ACEfit_Par.Nlz       = 1;                 % Inverse Gaussian normalisation
                                          % options (applied to each
                                          % phenotype voxel/element)
                                          %  0 - None
                                          %  1 - Gaussian normalisation
                                          %      *before* forming residuals
                                          %      (default)
                                          %  2 - Gaussian normalisation
                                          %      *after* forming residuals;
                                          %      note, though, that after
                                          %      this Gaussian
                                          %      normalisation the
                                          %      residuals will be formed
                                          %      again to ensure
                                          %      orthognality of residuals
                                          %      to the design matrix.

ACEfit_Par.AggNlz    = 0;                 % Aggregate heritability
                                          % normalisation options (applied
                                          % to each phenotype
                                          % voxel/element)
                                          %  0 - Default, meaning that only
                                          %      determined by Nlz option.
                                          %      This always entails
                                          %      de-meaning and removal of
                                          %      any effects in Dsnmtx, but
                                          %      variance at each
                                          %      voxel/element unchanged.
                                          %  1 - Same as 0, but with
                                          %      variance normalisation;
                                          %      this is full
                                          %      'studentization'.
                                          %  2 - *Undo* mean centering of
                                          %      residual formation. (If
                                          %      Dsnmtx is empty or default
                                          %      value of an all-ones
                                          %      vector, this is equivalent
                                          %      to using the raw input
                                          %      data. If Dsnmtx contains
                                          %      nuisance regressors the
                                          %      residuals will be formed
                                          %      and the mean added back
                                          %      in.
                                          %  3 - Same as 2, but with
                                          %      variance normalisation;
                                          %      note that for each
                                          %      voxel/element, mean is
                                          %      first added back and then
                                          %      data are divided by stdev.

ACEfit_Par.ContSel   = [];                % Select a single contrast (a
                                          % volume in a 4D Nifti file
                                          % supplied for each subject, or
                                          % at the last dimension in a
                                          % cifti image; NOT compatible
                                          % with a single file containing
                                          % all subjects' data.)

ACEfit_Par.NoImg     = 0;                 % If 1, suppress image-wise
                                          % inference, and only compute
                                          % summaries.

ACEfit_Par.alpha_CFT = 0.05;                % Cluster-forming threshold
                                          % (default: 0.05)

ACEfit_Par.nPerm     = 1000;                % Number of permutations
                                          % (default: 1000)

ACEfit_Par.nBoot     = 1000;                % Number of bootstrap replicates
                                          % (default: 1000)

ACEfit_Par.nParallel = 10;                % Number of parallel runs
                                          % (default: 1, without
                                          % parallelization)

%%% 2) Update 'ACEfit_Par' with the input data information
ACEfit_Par = PrepData(ACEfit_Par);

%%% 3) Run the original data once
ACEfit_Par = ACEfit(ACEfit_Par);

%%% 4) Add permutation and bootstrapping information, and save
%%%    "ACEfit_Par.mat"
PrepParallel(ACEfit_Par);


%
% Permutation inference for computing FWE/FDR-corrected p-values
%

if ACEfit_Par.nPerm>0

    %%% 1)
    %%%%% The following code can be scripted or parallelized as you wish.
    %%%%% Please refer to "README_APACE_intro.pdf" for the example snippets
    %%%%% for parallelization.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    load(fullfile(ACEfit_Par.ResDir,'ACEfit_Par.mat'));

    parfor i=1:ACEfit_Par.nParallel
        RunID = i;
        ACEfit_Perm_Parallel(ACEfit_Par,RunID);
    end
    % Inside ResDir, it will create result sets, ACEfit_Parallel_XXXX.mat,
    % one for each RunID.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %%% 2) This will merge together all the results from the specified
    %%%    RunID's
    load(fullfile(ACEfit_Par.ResDir,'ACEfit_Par.mat'));
    ACEfit_Perm_Parallel_Results(ACEfit_Par);

    %%% 3)
    load(fullfile(ACEfit_Par.ResDir,'ACEfit_Par.mat'));
    ACEfit_Results(ACEfit_Par);

end


%
% Bootstrapping inference for constructing CIs
%

if ACEfit_Par.nBoot>0

    %%% 1)
    %%%%% The following code can be scripted or parallelized as you wish.
    %%%%% Please refer to "README_APACE_intro.pdf" for the example snippets
    %%%%% for parallelization.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    load(fullfile(ACEfit_Par.ResDir,'ACEfit_Par.mat'));

    parfor i=1:ACEfit_Par.nParallel
        RunID = i;
        ACEfit_Boot_Parallel(ACEfit_Par,RunID);
    end
    % Inside ResDir, it will create result sets, BootCI_Parallel_XXXX.mat,
    % one for each RunID.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %%% 2) This will merge together all the results from the specified RunID's
    load(fullfile(ACEfit_Par.ResDir,'ACEfit_Par.mat'));
    ACEfit_Boot_Parallel_Results(ACEfit_Par);

    %%% 3) Construct CIs
    load(fullfile(ACEfit_Par.ResDir,'ACEfit_Par.mat'));
    Boot_CIs(ACEfit_Par);

end


%
% Aggregate heritability (aka "Steve's method") for multiple phenotypes,
% with P-values via permutation and CI's via boostrapping.
%
% Note that permuation (steps 1-3) and bootstrapping (steps 1-3) can be
% skipped by setting ACEfit_Par.nPerm=0 and ACEfit_Par.nBoot=0 separately;
% the following code can be run immediately after "PrepParallel".
%

% load(fullfile(ACEfit_Par.ResDir,'ACEfit_Par.mat'));
% AgHe_Method(ACEfit_Par);

% % Once with no variance normalisation
% ACEfit_Par.AggNlz = 0; % de-meaning only
% AgHe_Method(ACEfit_Par,'_NoNorm');
%
% % Now, again, but with variance normalisation
% ACEfit_Par.AggNlz = 1; % de-meaning and scaling to have stdev of 1.0
% AgHe_Method(ACEfit_Par,'_Norm');


%
% Generate summary file
%

APACEsummary(ACEfit_Par,'ResultSummary'); % Save results to "ResultsSummary.csv"
APACEsummary(ACEfit_Par); % Print results to the screen
