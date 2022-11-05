

## Interactive visualization of population genetics data for \~10,000 modern and ancient individuals.

# 0. App
Deployed on Heroku: [https://umap-aadr.herokuapp.com/main_umap](https://umap-aadr.herokuapp.com/main_umap)

Can also run the app locally with bokeh serve:

`bokeh serve --show population_genetics_AADR/02.output/main_umap.py`


![screen](https://raw.githubusercontent.com/thirtysix/population_genetics_AADR/master/main_umap.png)

# 1. Background
This repository provides scripts and results from an analysis of a starting set of 16,765 ancient and modern humans found at [AARD](https://reich.hms.harvard.edu/allen-ancient-dna-resource-aadr-downloadable-genotypes-present-day-and-ancient-dna-data).

Tools used to analyze the data:
 - [ADMIXTOOLS 2](https://github.com/uqrmaie1/admixtools)
 - [PLINK2](https://www.cog-genomics.org/plink/2.0/)
 - [UMAP](https://github.com/lmcinnes/umap)

Library used to generate the interactive visualization:
 - [Bokeh](https://github.com/bokeh/bokeh)



# 2. Analysis

## 2.1 Starting data
Genotype data was retrieved from the Allen Ancient DNA Resource (AADR).  This data can be downloaded but is not included here due to size (2.4GB), but are not needed as downstream results are present.
[https://reich.hms.harvard.edu/allen-ancient-dna-resource-aadr-downloadable-genotypes-present-day-and-ancient-dna-data](https://reich.hms.harvard.edu/allen-ancient-dna-resource-aadr-downloadable-genotypes-present-day-and-ancient-dna-data)

## 2.2 Converted from PACKEDANCESTRYMAP format to PLINK2 format (LARGE MEM REQUIREMENT)
The [ADMIXTOOLS 2](https://github.com/uqrmaie1/admixtools) R library was used to convert the binary PACKEDANCESTRYMAP format to "bfile" format suitable for PCA analysis in PLINK2.
These files are not included here due to size, but are not needed as downstream results are present.
```
library("admixtools")
future::plan('multicore')
data_dn <- "00.raw_data/v52.2_HO_public/"
data_set_name <- "v52.2_HO_public"
packed_ancestry_data_prefix = paste0(data_dn, data_set_name)
plink_data_prefix = paste0(data_dn, data_set_name, "_PLINK")
#convert from packed ancestry to PLINK files
packedancestrymap_to_plink(packed_ancestry_data_prefix, plink_data_prefix)
```

## 2.3 Run PCA analysis in PLINK
The PLINK2 executable can be downloaded here: [https://www.cog-genomics.org/plink/2.0/](https://www.cog-genomics.org/plink/2.0/)

Convert from early PLINK format (bfile) to current format (pfile):
`/PATH/TO/plink2 --bfile v52.2_1240K_public_PLINK --make-pgen --out v52.2_1240K_public_PLINK_PGEN`

Filter variants by genotype count and samples by genotype count:
`/PATH/TO/plink2 --pfile v52.2_1240K_public_PLINK_PGEN --geno 0.1 --mind 0.3 --make-pgen --out v52.2_1240K_public_PLINK_PGEN_GENO10MIND30`

Run PCA:
`/PATH/TO/plink2 --pfile v52.2_1240K_public_PLINK_PGEN_GENO10MIND30 --pca 20 approx biallelic-var-wts --threads 12 --out PCA_OUT`


## 2.4 Run UMAP analysis
UMAP analysis done with UMAP Python library [https://github.com/lmcinnes/umap](https://github.com/lmcinnes/umap)

See: [01.code/umap_run.py](https://github.com/thirtysix/population_genetics_AADR/blob/master/01.code/umap_run.py)

## 2.5 Bokeh interactive visualization
See: [02.output/UMAP_bokeh](https://github.com/thirtysix/population_genetics_AADR/blob/master/02.output/UMAP_bokeh/main_umap.py)

Run locally: `bokeh serve --show 02.output/main_umap.py`

Visit deployed version on Heroku: [https://umap-aadr.herokuapp.com/main_umap](https://umap-aadr.herokuapp.com/main_umap)


