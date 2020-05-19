savepath = '/results_ACE/permutations/';
cd '~/results_ACE/';
for x=1:1000
    run WK_ParallelOutline_net_perm.m % outputs one (random) AE matrix (vectorized)
    
    load('~/results_ACE/permutations/ACE_A_h2.mat'); % load the ACE_A_h2 (generated above).
    newname = sprintf('ACE_A_h2_perm-%d.mat',x);
    save(fullfile(savepath,newname),'ACE_A_h2');
end

% when the above is done: run -> twin_permute.py