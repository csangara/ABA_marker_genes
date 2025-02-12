import pandas as pd
from pathlib import Path
import numpy as np
import anndata
import sys
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache
from abc_atlas_access.abc_atlas_cache.anndata_utils import get_gene_data

merfish_genes = pd.read_csv('../data/Xenium_V1_FF_Mouse_Brain_MultiSection_Input_gene_groups.csv')
download_base = Path('/home/chananchidas/data/ABA_data')

abc_cache = AbcProjectCache.from_cache_dir(download_base)
abc_cache.load_manifest('releases/20241130/manifest.json')

cell = abc_cache.get_metadata_dataframe(directory='WMB-10X', file_name='cell_metadata').set_index('cell_label')
print('Loaded cell dataframe')
print(cell.shape)
print(cell.dataset_label.value_counts())

gene = abc_cache.get_metadata_dataframe(directory='WMB-10X', file_name='gene').set_index('gene_identifier')
print('Loaded gene dataframe')
print(gene.shape)

cell = cell[cell.dataset_label.str.startswith('WMB-10Xv')]
print('Subset cells to only v2 and v3')
print(cell.shape)

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
print("Subsetted to genes of interest, saving file...")

# Convert gene_data to integer type
gene_data = gene_data.astype(int)

# Save the sparse DataFrame to a parquet file
gene_data.to_parquet('/home/chananchidas/data/ABA_data/WMB-10X_subset_merfish_genes.parquet')
print("Saved parquet file")