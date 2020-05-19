import numpy as np 
import pandas as pd 
import scipy.io as sio
import numpy.linalg as npl
import nibabel as nib
from nibabel.affines import apply_affine

# Networks (400 nodes, 7 networks)
community_id = np.load('~/schaefer_community_id.npy',allow_pickle=True) # vector of integers [0,6] of size 1x400
communities = np.load('~/schaefer_communities.npy',allow_pickle=True)   # vector of network names (1x400)

# Can load either 1mm and 2mm Shaefer brain parcellation. 

schaefer_coords_path = '~/schaefer400_7nets_coords.csv'
schaefer_nii = '~/schaefer2018_400Parcels_7Networks_order_FSLMNI152_2mm.nii'

# Read in the coordinates 
# these are in world coordinates in RAS space
coords = pd.read_csv(schaefer_coords_path,';')[['R','A','S']]
coords = coords.values[1:]

schaefer_img = nib.load(schaefer_nii)
schaefer_data = nib.load(schaefer_nii).get_fdata()
schaefer_aff = schaefer_img.affine

# read in your data
h2_path = '/h2_ace_lrt_clust_fwe.nii'
h2_img  = nib.load(h2_path)
h2_data = h2_img.get_fdata()

aff = h2_img.affine #  affine transformation of the neurosynth pain mask to move from voxel space to MNI (mm) space

# read in NPS 
img = nib.load('~/NPS_share/weights_NSF_grouppred_cvpcr.img')
nps_data = img.get_fdata()

# union between neurosynth pain mask and brain parcellation 
vec = np.zeros([400]) # if pain mask and brain parcellation overlap set vec[x] to 1 
save_roi = []
for coord in coords:
	vox_coords = apply_affine(npl.inv(aff),coord) # inv takes affine to move from RAS/worldspace to voxel space
	x = int(vox_coords[0])
	y = int(vox_coords[1])
	z = int(vox_coords[2])

	# RAS to parcellation space
	vox_coords = apply_affine(npl.inv(schaefer_aff),coord) # inv takes affine to move from scanner RAS+ (worldspace) to voxel space in the image 
	
	xa = int(vox_coords[0])
	ya = int(vox_coords[1])
	za = int(vox_coords[2])

	# RAS to NPS space
	vox_coords = apply_affine(npl.inv(img.affine),coord) 
	
	xab = int(vox_coords[0])
	yab = int(vox_coords[1])
	zab = int(vox_coords[2])

	# or 
	if nps_data[xab,yab,zab]!=0: # where the nps is not zero AT coordinates defined by the parcellation
		print('network at coord: ' + str(coord) + ' ' + communities[int(schaefer_data[xa,ya,za])-1] + ' ' + str(int(schaefer_data[xa,ya,za])-1))
		vec[int(schaefer_data[xa,ya,za])-1] = 1

		save_roi.append(int(schaefer_data[xa,ya,za]))

save_roi = np.array(save_roi)



