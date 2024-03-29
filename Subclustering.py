import numpy as np
import pandas as pd
import scanpy.api as sc
import seaborn as sb

sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
sc.logging.print_versions()

from matplotlib import rcParams

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('default')  
sc.settings.set_figure_params(dpi=80)

#-- create directories 
!mkdir DE meta H5AD

#--- load processed and batch corrected object:

corrected=sc.read('you_path/corrected.h5ad')
corrected

#-- Extract cell of interest (using louvain ids)

cells_of_interest =corrected.obs.loc[corrected.obs["louvain"].isin(["1","14"]), :].index
SC = corrected[cells_of_interest, :]
SC

#-- runing Louvain clustering 
sc.tl.louvain(SC, resolution=0.6) #default , resolution = 1

#-- runing UMAP
sc.tl.umap(SC, min_dist=0.3, n_components=3)


#-----------  save Object + meta data 

#--- Umap embbedings 
Emb =SC.obsm.to_df()[['X_umap1', 'X_umap2', 'X_umap3']]
Emb.index =SC.obs.index

#-- Meta Data 
meta =SC.obs
Mat = meta.join(Emb)

Mat.to_csv('your_path/meta/Meta_SC_102119.csv')
mono.write('your_path/H5AD/SC.h5ad')



#--- Differentially expressed genes (Subcluster vs. rest of the cells )

#-- Finding marker genes
matplotlib.style.use('ggplot') 
rcParams['figure.figsize'] = (8,6)
sc.tl.rank_genes_groups(SC, 'louvain', method='t-test')
sc.pl.rank_genes_groups(SC, n_genes=45, sharey=False,ncols=3)

#--- save DEG- t-test
result = SC.uns['rank_genes_groups']
groups = result['names'].dtype.names
pd.DataFrame({group + '_' + key[:1]: result[key][group]
    for group in groups for key in ['names', 'pvals']}).to_csv('your_path/DE/SC_DE_louv_t-Test.csv')

    
matplotlib.style.use('ggplot') 
rcParams['figure.figsize'] = (8,6)
sc.tl.rank_genes_groups(SC, 'louvain', method='wilcoxon')
sc.pl.rank_genes_groups(SC, n_genes=45, sharey=False)

#--- save DEG- t-test
result = SC.uns['rank_genes_groups']
groups = result['names'].dtype.names
pd.DataFrame({group + '_' + key[:1]: result[key][group]
    for group in groups for key in ['names', 'pvals']}).to_csv('your_path/DE/SC_DE_louv_wilcoxon.csv')
    
