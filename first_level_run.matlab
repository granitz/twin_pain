%-----------------------------------------------------------------------
% Job saved on 22-Apr-2020 07:29:16 by cfg_util (rev $Rev: 6460 $)
% spm SPM - SPM12 (6685)
% cfg_basicio BasicIO - Unknown
% During habituation, there was four presentation of CS+ and four of CS- 
% The first and second regressor refers to these two. 
% During acqusition there were 16 presentation of CS+ (with 50% reinforcement) and 16 of CS-. 
% Regressor 3 is the CS+ when it is not followed by the US (shock) (= 8 presentations).
% Regressor 4 is the CS- (16 presentations).
% Regressor 5 is the US. 
% Regressor 6 is the CS+ when it is followed by the US (n=8). 
%-----------------------------------------------------------------------
matlabbatch{1}.cfg_basicio.file_dir.dir_ops.cfg_named_dir.name = 'Subject directory';
matlabbatch{1}.cfg_basicio.file_dir.dir_ops.cfg_named_dir.dirs = {'<UNDEFINED>'};
matlabbatch{2}.cfg_basicio.file_dir.dir_ops.cfg_cd.dir(1) = cfg_dep('Named Directory Selector: Subject directory(1)', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','dirs', '{}',{1}));
matlabbatch{3}.cfg_basicio.file_dir.dir_ops.cfg_mkdir.parent(1) = cfg_dep('Named Directory Selector: Subject directory(1)', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','dirs', '{}',{1}));
matlabbatch{3}.cfg_basicio.file_dir.dir_ops.cfg_mkdir.name = 'acq_csp_us_vs_csp_no_us';
matlabbatch{4}.spm.stats.fmri_spec.dir(1) = cfg_dep('Make Directory: Make Directory ''acq_csp_us_vs_csp_no_us''', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','dir'));
matlabbatch{4}.spm.stats.fmri_spec.timing.units = 'secs';
matlabbatch{4}.spm.stats.fmri_spec.timing.RT = 2.396;
matlabbatch{4}.spm.stats.fmri_spec.timing.fmri_t = 47;
matlabbatch{4}.spm.stats.fmri_spec.timing.fmri_t0 = 1;
matlabbatch{4}.spm.stats.fmri_spec.sess.scans = '<UNDEFINED>';
matlabbatch{4}.spm.stats.fmri_spec.sess.cond = struct('name', {}, 'onset', {}, 'duration', {}, 'tmod', {}, 'pmod', {}, 'orth', {});
matlabbatch{4}.spm.stats.fmri_spec.sess.multi = '<UNDEFINED>';
matlabbatch{4}.spm.stats.fmri_spec.sess.regress = struct('name', {}, 'val', {});
matlabbatch{4}.spm.stats.fmri_spec.sess.multi_reg = '<UNDEFINED>';
matlabbatch{4}.spm.stats.fmri_spec.sess.hpf = 128;
matlabbatch{4}.spm.stats.fmri_spec.fact = struct('name', {}, 'levels', {});
matlabbatch{4}.spm.stats.fmri_spec.bases.hrf.derivs = [0 0];
matlabbatch{4}.spm.stats.fmri_spec.volt = 1;
matlabbatch{4}.spm.stats.fmri_spec.global = 'None';
matlabbatch{4}.spm.stats.fmri_spec.mthresh = 0.8;
matlabbatch{4}.spm.stats.fmri_spec.mask = {''};
matlabbatch{4}.spm.stats.fmri_spec.cvi = 'AR(1)';
matlabbatch{5}.spm.stats.fmri_est.spmmat(1) = cfg_dep('fMRI model specification: SPM.mat File', substruct('.','val', '{}',{4}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','spmmat'));
matlabbatch{5}.spm.stats.fmri_est.write_residuals = 0;
matlabbatch{5}.spm.stats.fmri_est.method.Classical = 1;
matlabbatch{6}.spm.stats.con.spmmat(1) = cfg_dep('Model estimation: SPM.mat File', substruct('.','val', '{}',{5}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','spmmat'));
matlabbatch{6}.spm.stats.con.consess{1}.tcon.name = 'CS+noUS > CS-';
matlabbatch{6}.spm.stats.con.consess{1}.tcon.weights = [0 0 1 -1];
matlabbatch{6}.spm.stats.con.consess{1}.tcon.sessrep = 'none';
matlabbatch{6}.spm.stats.con.consess{2}.tcon.name = 'CS- > CS+noUS';
matlabbatch{6}.spm.stats.con.consess{2}.tcon.weights = [0 0 -1 1];
matlabbatch{6}.spm.stats.con.consess{2}.tcon.sessrep = 'none';
matlabbatch{6}.spm.stats.con.consess{3}.tcon.name = 'Shocks';
matlabbatch{6}.spm.stats.con.consess{3}.tcon.weights = [0 0 0 0 1];
matlabbatch{6}.spm.stats.con.consess{3}.tcon.sessrep = 'none';
matlabbatch{6}.spm.stats.con.consess{4}.tcon.name = 'CS+US > CS+NoUS';
matlabbatch{6}.spm.stats.con.consess{4}.tcon.weights = [0 0 -1 0 1 1];
matlabbatch{6}.spm.stats.con.consess{4}.tcon.sessrep = 'none';
matlabbatch{6}.spm.stats.con.delete = 0;
