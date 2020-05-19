import numpy as np 
import pandas as pd 
import os 
import matplotlib.pyplot as plt 
import matplotlib.patches as patches
import seaborn as sns 
import scipy.io as sio
plt.ion()


# The following is used to plot a heatmap of functional connectivity or other, along with network membership. (Figure 2A-C)

com = np.load('~/shaefer_community_id.npy') # [1x400 vector, 0,0,0,...,1,1,1, ... 6] representing network membership of nodes  
com_id = np.load('~/shaefer_communities.npy',allow_pickle=True) # 1x400 vector with names of networks. 

vec = np.concatenate([np.where(com==0)[0],np.where(com==1)[0],np.where(com==2)[0],np.where(com==3)[0],np.where(com==4)[0],np.where(com==5)[0],np.where(com==6)[0]])
C = ['purple','blue','green','violet','cornsilk','orange','crimson']
colors = np.array([C[x] for x in com])


v = {'Vis': 'purple',
'SM': 'blue',
'DA':'green',
'SA/VA':'violet',
'Limbic':'cornsilk',
'FP':'orange',
'DMN':'crimson',
'Pain':'black'
}

legend = [patches.Patch(color=v[x], label=x) for x in v]

plot_corr_matrix(net,com,colors,out_file=None,reorder=True,line=True,rectangle=False,draw_legend=True,legend=legend,colorbar=True)

def plot_corr_matrix(matrix,membership,colors,out_file=None,reorder=True,line=False,rectangle=False,draw_legend=False,legend=None,colorbar=False):
	"""
	Following plotting code was received some time ago (from github), and the original source is currently unknown but was not written by me, although I have modified the code slightly. 

	matrix: square, whatever you like
	membership: the community (or whatever you like of each node in the matrix)
	colors: the colors of each node in the matrix (same order as membership)
	out_file: save the file here, will supress plotting, do None if you want to plot it.
	line: draw those little lines to divide up communities
	rectangle: draw colored rectangles around each community
	draw legend: draw legend...
	colorbar: colorbar...
	"""
	if reorder == True:
		swap_dict = {}
		index = 0
		corr_mat = np.zeros((matrix.shape))
		names = []
		x_ticks = []
		y_ticks = []
		reordered_colors = []
		for i in np.unique(membership):
			for node in np.where(membership==i)[0]:
				swap_dict[node] = index
				index = index + 1
				names.append(membership[node])
				reordered_colors.append(colors[node])
		for i in range(len(swap_dict)):
			for j in range(len(swap_dict)):
				corr_mat[swap_dict[i],swap_dict[j]] = matrix[i,j]
				corr_mat[swap_dict[j],swap_dict[i]] = matrix[j,i]
		colors = reordered_colors
		membership = np.array(names)
	else:
		corr_mat = matrix
	# sns.set(style='white',context="paper",font='Helvetica',font_scale=1.2)
	std = np.nanstd(corr_mat)
	mean = np.nanmean(corr_mat)
	mask = np.zeros_like(corr_mat, dtype=np.bool)
	mask[np.triu_indices_from(mask, k=1)] = True
	
	# fig for h2 (Figure 2B)
	# fig = sns.clustermap(corr_mat,mask=mask,yticklabels=[''],xticklabels=[''],rasterized=True,col_colors=colors,row_colors=colors,row_cluster=False,col_cluster=False,**{'figsize':(10,9),'annot_kws':{"size": 12},'cbar_kws':{"orientation": "horizontal",'ticks':[0,0.5]}})
	
	# fig for cs+&US>cs- (Figure 2A)
	fig = sns.clustermap(corr_mat,mask=mask,yticklabels=[''],xticklabels=[''],cmap=sns.diverging_palette(260,10,sep=10, n=20,as_cmap=False),rasterized=True,col_colors=colors,row_colors=colors,row_cluster=False,col_cluster=False,**{'vmin':mean - (std*2),'vmax':mean + (std*2),'figsize':(10,9),'cbar_kws':{"orientation": "horizontal"}})
	ax = fig.fig.axes[4]
	# Use matplotlib directly to emphasize known networks
	if line == True or rectangle == True:
		if len(colors) != len(membership):
			colors = np.arange(len(membership))
		for i,network,color, in zip(np.arange(len(membership)),membership,colors):
			if i==0:
				continue
			if network != membership[i - 1]:
				if len(colors) != len(membership):
					color = 'white'
				if rectangle == True:
					ax.add_patch(patches.Rectangle((i+len(membership[membership==network]),400-i),len(membership[membership==network]),len(membership[membership==network]),facecolor="none",edgecolor=color,linewidth="2",angle=180))
				if line == True:
					ax.axhline(i, c='black',linewidth=.5,label=network)
					ax.axhline(i, c='black',linewidth=.5)
					ax.axvline(i, c='black',linewidth=.5)
	fig.ax_col_colors.add_patch(patches.Rectangle((0,0),400,1,facecolor="None",edgecolor='black',lw=2))
	fig.ax_row_colors.add_patch(patches.Rectangle((0,0),1,400,facecolor="None",edgecolor='black',lw=2))
	# col = fig.ax_col_colors.get_position()
	# fig.ax_col_colors.set_position([col.x0, col.y0, col.width*1, col.height*.35])
	# col = fig.ax_row_colors.get_position()
	# fig.ax_row_colors.set_position([col.x0+col.width*(1-.35), col.y0, col.width*.35, col.height*1])
	fig.ax_col_dendrogram.set_visible(False)
	fig.ax_row_dendrogram.set_visible(False)
	if draw_legend == True:
		leg = fig.ax_heatmap.legend(ncol=1,handles=legend,frameon=False,borderaxespad=-.5,handletextpad=0.2,labelspacing=0.2,handlelength=0.6,fontsize='large', loc=0, bbox_to_anchor=(-0.1, .99)) # loc='upper right', bbox_to_anchor=(0.5, 0.5)
		for legobj in leg.legendHandles:
			legobj.set_linewidth(1)
	fig.cax.set_position(pos=[0.7,0.5,0.1,0.03])
	fig.cax.tick_params(size=0,pad=5,labelsize='x-large')
	# fig.cax.set_title(r'Genetic effect, $h^2$',fontdict={'fontsize':'x-large'}) # for h^2 (Figure 2B & D)
	fig.cax.set_title(r'Nociceptive processing',fontdict={'fontsize':'x-large'}) # for figure 2A & C
	cbar = ax.collections[0].colorbar 
	cbar.set_ticks([mean - (std*2),0,mean+(std*2)]) # for figure 2A & C
	cbar.set_ticklabels([np.round(mean - (std*2),2),0, np.round(mean+(std*2),2)]) # for figure 2A & C
	# cbar.set_ticks([0,0.5]) # for h^2 (Figure 2B & D)
	# cbar.set_ticklabels([0,0.5]) # for h^2 (Figure 2B & D)
	if colorbar == False:
		fig.cax.set_visible(False)
	if out_file != None:
		plt.savefig(out_file,dpi=300)
		plt.close()
	if out_file == None:
		plt.show()
	return fig


#####################################################################
# Figure 2C & D. Compute & then use the function at the top to plot #
#####################################################################
# Display within/between network connectivity #
############################################### 
wfcavg = 'weighted functional connectivity averaged over subjects'
mat = np.zeros([7,7])
for x in np.unique(com):
	for y in np.unique(com):
		mat[x,y] = np.sum(wfcavg[com==x][:,com==y])/(len(wfcavg[com==x]) + len(wfcavg[com==y]))

# h2-component within/between
mat = np.zeros([7,7])
for x in np.unique(com):
	for y in np.unique(com):
		mat[x,y] = np.sum(sigh2[com==x][:,com==y])

cols = np.array(['purple','blue','green','violet','cornsilk','orange','crimson'], dtype='<U8')


#############
# Figure 2F #
#############
# count how many nodes within each network has at least one edge.
v = np.zeros([7])
sumsig = np.sum(sig,axis=0)>0
for x in range(7):
	v[x] = np.sum(sumsig[com==x])

h2com_int = np.array([15.,22.,18.,7.,7.,12.,24.])
npscom_int = np.array([8.,18.,12.,26.,0., 11.,7.]) # Use brain_network_overlap.py
plt.bar(range(7),npscom_int)

df1 = pd.DataFrame()
df1['number_roi'] = h2com_int
df1['Data'] = np.repeat('$h^2$',7)
df1['communities'] = np.array(['Vis','SM','DA','SA/VA','Limbic','FP','DMN'])

df2 = pd.DataFrame()
df2['number_roi'] = npscom_int
df2['Data'] = np.repeat('NPS',7)
df2['communities'] = np.array(['Vis','SM','DA','SA/VA','Limbic','FP','DMN'])

df = pd.concat([df1,df2])
plt.rcParams.update({'font.size': 24})
ax = sns.barplot(x="communities", y="number_roi", hue='Data', data=df)
ax.set_ylabel('Number of ROIs')
ax.set_xlabel('Networks')
sns.despine()
ax.legend(loc='upper left',title='Data')




