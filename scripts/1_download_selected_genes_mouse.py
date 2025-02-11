import pandas as pd
from pathlib import Path
import numpy as np
import anndata

from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache
from abc_atlas_access.abc_atlas_cache.anndata_utils import get_gene_data

merfish_genes = pd.read_csv('../data/Xenium_V1_FF_Mouse_Brain_MultiSection_Input_gene_groups.csv')

download_base = Path('/data/gent/vo/000/gvo00070/vsc43831/spatial_datasets/ABA_data')
abc_cache = AbcProjectCache.from_s3_cache(download_base)
abc_cache.load_manifest('releases/20241130/manifest.json')

cell = abc_cache.get_metadata_dataframe(directory='WMB-10X', file_name='cell_metadata').set_index('cell_label')
cell

cell.dataset_label.value_counts()
gene = abc_cache.get_metadata_dataframe(directory='WMB-10X', file_name='gene').set_index('gene_identifier')
gene


# Let's try only the multimodal cells
cell = cell[cell.dataset_label.str.startswith('WMB-10Xv')]
cell.shape

# Get gene_names that are not in the gene dataframe
print(merfish_genes.index[~merfish_genes.index.isin(gene.index)])

# Is Hs3st2 in the gene dataframe?
print('Hs3st2' in gene.index)

# Replace Hs3St2 with Hs3st2
merfish_genes.index = merfish_genes.index.str.replace('Hs3St2', 'Hs3st2')

# Are all genes in the gene dataframe?
print(merfish_genes.index[merfish_genes.index.isin(gene.index)].all())

gene_data = get_gene_data(
    abc_atlas_cache=abc_cache,
    all_cells=cell,
    all_genes=gene,
    selected_genes=list(merfish_genes.index),
    data_type='raw'
)

# Create sparse matrix
adata = anndata.AnnData(
    X=gene_data,
    obs=cell,
    var=gene[gene.gene_symbol.isin(merfish_genes.index)].set_index('gene_symbol')
)

adata.write("/data/gent/vo/000/gvo00070/vsc43831/spatial_datasets/ABA_data/WMB-10Xv3_subset_merfish_genes.h5ad")