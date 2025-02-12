# Allen Brain Atlas marker genes in Xenium panel

This repository contains `scripts/` for:

<ol type="a">
  <li>Downloading the mouse scRNA-seq datasets from the Allen Brain Atlas (~4 million cells)</li>
  <li>Subsetting the dataset to the 248 genes in the Xenium panel</li>
  <li>Calculating the log-fold change of these genes among the 34 classes</li>
</ol>

The scores and log-fold changes of each gene can be downloaded at `data/WMB-10X_class_marker_genes*.csv`. Note that some of the groups cannot be distinguished with the existing marker genes, as seen in [this dotplot](scripts/figures/dotplot_marker_genes_class.png).

The AnnData objects have also been deposited at https://zenodo.org/records/14859461. There was minimal preprocessing of the data, e.g., there was no batch correction performed at all (and neither did the original authors, I think).

### Other resources:
* [Interactive visualizer](https://knowledge.brain-map.org/abcatlas): select the "10x scRNAseq whole brain" dataset to color the UMAP with gene expression and metadata information
* [Allen Brain Cell Atlas - Data Access](https://alleninstitute.github.io/abc_atlas_access/intro.html): a collection of Jupyter notebooks on how to access the different Allen Brain Atlas datasets
* [MapMyCells](https://knowledge.brain-map.org/mapmycells/process/): a service by the Allen Brain Atlas to annotate your cells - could be interesting to compare with Sparrow.
