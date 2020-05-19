import numpy as np
import networkx as nx
import itertools
import scipy.io as sio
import seaborn as sns
import matplotlib.pyplot as plt
plt.ion()

def largest_cluster(emph2, randh2, alpha_cluster=0.2, alpha=0.05):
    """
    Finds largest cluster of values that is greater than a cut-off test statistic
    (alpha_cluster) for both the empirical values and permuted values. The permuted
    values create a distribution of largest cluster for the null hypothesis ().
    Then tests whether the size of the clusters identified in the empirical data
    is larger than the significant.

    Parameters
    ==========
    emph2 : array
        symetric array of h2 values. h2 is in the range of [0,1] with h2 = 0 meaning no heritability.
    randh2 : array
        num_permutation x N x N. h2 matrices generated with permuted twin identity.
    alpha_cluster : float
        threshold of h2 for cluster derivation
    alpha : float
        "final" p value to compare empirical cluster against null distribution

    Returns
    ========
    sig_matrix : array
        binary matrix of edges that were above significance threshold
    permuted_sizes : array
        list of the largest cluster in each permutation
    """

    permutations = randh2.shape[0]
    h2_bin = np.zeros(emph2.shape)
    h2_bin[emph2>alpha_cluster] = 1 # Set values ABOVE threshold to 1.
    G = nx.Graph(h2_bin)
    # Actual index in permutation for cut off point
    threshold = int(permutations - np.ceil(permutations*alpha))
    # Get the empirical clusters
    clusters = sorted(nx.connected_components(G), key=len, reverse=True)
    empirical_lengths = np.array([len(c) for c in clusters])
    permuted_sizes = []
    # compute component size for h2 derived using permuted twin identity.
    for x in range(permutations):
        tmp_bin = np.zeros(emph2.shape)
        tmp_bin[randh2[x]>alpha_cluster] = 1
        p = nx.Graph(tmp_bin)
        # Add largest cluster to permutation distribution
        permuted_sizes.append(len(sorted(nx.connected_components(p), key=len, reverse=True)[0]))
    # sort distributin and test each empirical
    cutoff = sorted(permuted_sizes)[threshold]
    sig_cluster = empirical_lengths > cutoff
    # Return significance matrix by looping through significant clusters
    sig_matrix = np.zeros(emph2.shape)
    for sc in np.where(sig_cluster==True)[0]:
        print(sc)
        ind = list(itertools.permutations(clusters[sc],2))
        sig_matrix[ind] = h2_bin[ind]

    return sig_matrix, permuted_sizes



emph2 = np.reshape(sio.loadmat('~/AE_A_h2.mat')['AE_A_h2'],[400,400])
randh2 = sio.loadmat('~/randh2.mat')['net']

sig, distribution = largest_cluster(emph2,randh2, alpha_cluster=th, alpha=0.05)

# Save sig as .node and plot using BrainNet Viewer. 

# Compute largest component over several thresholds of h^2
thresholds = np.arange(0.2,0.34,0.001)
supermatrix = np.zeros([len(thresholds),400,400])
randh2 = np.reshape(randh2,[1000,400,400]) 
h2 = np.reshape(h2,[400,400])
for x,th in enumerate(thresholds):
    sig, distribution = largest_cluster(h2,randh2, alpha_cluster=round(th,3), alpha=0.05)
    supermatrix[x,:,:] = sig 

# Create df and plot 
dfs = [] 
for i,sig in enumerate(supermatrix):
    tmp = np.zeros([7])
    sumsig = np.sum(sig,axis=0)>0
    for x in range(7):
        tmp[x] = np.sum(sumsig[com==x])

        v = np.zeros([7])
        sumsig = np.sum(sigh2,axis=0)>0
        for x in range(7):
            v[x] = np.sum(sumsig[com==x])

    df1 = pd.DataFrame()
    df1['number_roi'] = tmp
    df1['Threshold'] = np.repeat(str(np.round(thresholds[i],2)),7)
    df1['communities'] = np.array(['Vis','SM','DA','SA/VA','Limbic','FP','DMN'])

    dfs.append(df1)

df = pd.concat(dfs)
ax = sns.barplot(x="communities", y="number_roi", hue='Threshold', data=df)
ax.set_ylabel('Number of ROIs')
ax.set_xlabel('Networks')
sns.despine()

