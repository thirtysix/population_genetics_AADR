

## Interactive visualization of population genetics data for \~10,000 modern and ancient individuals.

# 1. Background
This repository provides scripts and results from an analysis of a starting set of 16,765 ancient and modern humans found at [AARD](https://reich.hms.harvard.edu/allen-ancient-dna-resource-aadr-downloadable-genotypes-present-day-and-ancient-dna-data).

Tools used to analyze the data:
 - [EigenSoft](https://github.com/DReichLab/EIG)
 - [PLINK2](https://www.cog-genomics.org/plink/2.0/)
 - [UMAP](https://github.com/lmcinnes/umap)

Library used to generate the interactive visualization:
 - [Bokeh](https://github.com/bokeh/bokeh)

Deployed app:
[https://umap-aadr.herokuapp.com/main_umap](https://umap-aadr.herokuapp.com/main_umap)

Run the app locally with bokeh serve:
`bokeh serve --show population_genetics_AADR/02.output/main_umap.py`


# 2. Analysis

# 2.1 Starting data
Genotype data was retrieved from the Allen Ancient DNA Resource (AADR):
[https://reich.hms.harvard.edu/allen-ancient-dna-resource-aadr-downloadable-genotypes-present-day-and-ancient-dna-data](https://reich.hms.harvard.edu/allen-ancient-dna-resource-aadr-downloadable-genotypes-present-day-and-ancient-dna-data)



