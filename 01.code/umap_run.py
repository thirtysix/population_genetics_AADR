#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python vers. 3.8.0 ###########################################################
# Libraries ####################################################################

import numpy as np
import pandas as pd
import os
import pathlib

from datetime import datetime
import timeit

from math import ceil
import umap

import seaborn as sns
################################################################################
# Description/Notes ############################################################
################################################################################
"""
OUTLINE
Input:
    PLINK2 PCA results: (02.output/PCA/v52.2_HO_public_PLINK_PGEN_filtered_PCA.eigenvec)
    Genotype sample annotations: (00.raw_data/v52.2_HO_public/v52.2_HO_public.anno)
    UN Geoscheme: (00.raw_data/UN_geoscheme.tsv)

Process:
    Generate UMAP results (x,y coordinates)

Output:
    Combined sample metadata and UMAP (02.output/UMAP_bokeh/dataset.tsv)
    

"""

################################################################################
# Base-level Functions #########################################################
################################################################################
def metadata_rename():
    rename_d = {"Year data from this individual was first published [for a present-day individuals we give the data of the data reported here; missing GreenScience 2010 (Vi33.15, Vi33.26), Olalde2018 (I2657), RasmussenNature2010 (Australian)]":"Pub. Year",
                "Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]":"YB1950",
                "mtDNA haplogroup if >2x or published":"mtDNA haplogroup"}
                
    metadata_df.rename(columns=rename_d, inplace=True)

################################################################################
# Task-specific Functions ######################################################
################################################################################
def load_pca_data():
    """
    PCA data from PLINK2 '--pca' run.  Expected to be of the format:
    2 ID columns + n PCA data columns
    """

    pca_data_array = []
    
    # Make sure the number of components is >= the number of PCs
    if pcs < nc:
        print('ERROR: Number of PCs is less than request dimensions.')
        
    else:
        print('Beginning import of data')
        print('Parameters: ', '\n PCs:', str(pcs), '\n NC:', str(nc), '\n NN:', str(nn), '\n MD:', str(md),
            '\n Metric:', met)

        # load - PCA data
        try:
            pca_data_array = np.array(pca_df.iloc[:,2:].values.tolist())
            
        except Exception as e:
            print(e)
            print('Error during data import')

        # preamble for log
        print()
        print("Using UMAP version: " + umap.__version__)
        print("Reducing to " + str(nc) + " components")
        print("Using " + str(nn) + " neighbours")
        print("Using minimum distance of " + str(md))
        print("Using metric: " + met)
        print("Using " + str(pcs) + " PCs")
        print()
        print("Input data shape: ", pca_data_array.shape)

    return pca_data_array


def run_UMAP():
    """
    Using PLINK2 PCA data, run UMAP analysis using set parameters.
    """

    try:
        start = timeit.default_timer()

        # run - UMAP analysis
        umap_proj_fit = umap.UMAP(n_components=nc, n_neighbors=nn,min_dist=md,metric=met,
            verbose=True).fit_transform(pca_data_array[:,:pcs])     
        stop = timeit.default_timer()

        # print - run details
        print("UMAP runtime: ", stop - start)

        # print - runtime
        print("Finished successfully! UMAP runtime: ", stop - start)

        return umap_proj_fit

    except Exception as e:
        print(e)
        print('Error during UMAP')

    
def subregion_color_mapping():
    """
    Make grouped color scheme based on region:subregion.
    """

    color_key_d = {}
    color_key_hex_d = {}
    
    # mapping - subregion
    subregion_mapping_d = {'africa': ['Africa Northern', 'Africa Sub-Saharan'],
                           'americas': ['America Northern', 'America Latin and the Caribbean'],
                           'asia': ['Asia Central', 'Asia Eastern', 'Asia South-eastern', 'Asia Southern', 'Asia Western'],
                           'europe': ['Europe Eastern', 'Europe Northern', 'Europe Southern', 'Europe Western'],
                           'oceania': ['Australia and New Zealand', 'Melanesia', 'Micronesia']}

    # mapping - subregion colors
    color_d = {'africa':'Reds',
               'americas':'Blues',
               'asia':'Greens',
               'europe':'Purples',
               'oceania':'Oranges'}

    # mapping - color bindings for subregions
    for region, subregions in subregion_mapping_d.items():
        col_pal_name = color_d[region]
        col_pal = sns.color_palette(col_pal_name, len(subregions))
        subregions_col_pal_d = dict(zip(subregions, col_pal))
        subregions_col_pal_hex_d = dict(zip(subregions, col_pal.as_hex()))
        color_key_d.update(subregions_col_pal_d)
        color_key_hex_d.update(subregions_col_pal_hex_d)

    # set - black dots for unknown regions
    color_key_d['..'] = (0,0,0) 

    return color_key_d, color_key_hex_d

################################################################################
# Initiating Variables #########################################################
################################################################################
# name - raw data dn
rawdata_dn = "../00.raw_data"
rawdata_genotype_dn = os.path.join(rawdata_dn, "v52.2_HO_public")

# name - overall output dir
output_dn = "../02.output"
output_umap_bokeh_dn = os.path.join(output_dn, "UMAP_bokeh")
output_PCA_dn = os.path.join(output_dn, "PCA")
for dn in [output_dn, output_umap_bokeh_dn]:
    pathlib.Path(dn).mkdir(parents=True, exist_ok=True)
    
# name - PCA data; exists from previous run of PLINK2 PCA
pca_fn = os.path.join(output_PCA_dn, "v52.2_HO_public_PLINK_PGEN_filtered_PCA.eigenvec")

# name - sample metadata
metadata_fn = os.path.join(rawdata_genotype_dn, "v52.2_HO_public.anno")

# name - UN geoscheme
geo_fn = os.path.join(rawdata_dn, "UN_geoscheme.tsv")

# set - parameters
pcs = 5
nn = 50
md = 0.01
nc = 2
met = "euclidean"

# name - outfiles
dataset_fn = os.path.join(output_umap_bokeh_dn, "dataset.tsv")

################################################################################
# Execution ####################################################################
################################################################################

if not os.path.exists(dataset_fn):
    
    # load - PLINK2 PCA data file
    pca_df = pd.read_csv(pca_fn, sep="\t")
    pca_data_array = load_pca_data()

    # load - metadata
    metadata_df = pd.read_csv(metadata_fn, sep="\t")
    metadata_df['Country'] = [x.strip() for x in metadata_df['Country']]
    metadata_rename()

    # load - sample metadata
    geo_df = pd.read_csv(geo_fn, sep="\t")
    geo_df.fillna("..", inplace=True)
    geo_df['Sub-region'] = [" ".join(x.split(" ")[::-1]) if len(x.split(" ")) == 2 else x for x in geo_df['Sub-region']]
    geo_df.replace("Latin America and the Caribbean", "America Latin and the Caribbean", inplace=True)

    # merge - continent to metadata
    metadata_df = metadata_df.merge(geo_df, how="left", left_on="Country", right_on="Country or Area")
    missing_countries = sorted(list(set(metadata_df[metadata_df['Sub-region'].isna()]['Country'].tolist())))
    for x in missing_countries:
        print(x)

    if len(pca_data_array) > 0:

        # run - umap analysis
        umap_proj_fit = run_UMAP()

        # merge - pca with metadata = dataset
        dataset_df = pca_df.merge(metadata_df, how="left", left_on="IID", right_on="Genetic ID")
        dataset_df.fillna("..", inplace=True)
    
        # set - years before present (YBP) values
        dataset_df.replace({'YB1950':".."}, 0, inplace=True)
        dataset_df['YBP'] = [-1*(x + 72) if x!=0 else x for x in dataset_df['YB1950']]

        # set - color dict for subregions
        color_key_d, color_key_hex_d = subregion_color_mapping()

        # set - colors; subregions
        dataset_df["colors"] = dataset_df["Sub-region"].map(color_key_hex_d)
        print(dataset_df["colors"])

        # reduce - target columns
        keep_cols = ['Sub-region', "colors", "Genetic ID", "Publication",
                     "YBP", "Group ID", "Country", "Lat.",
                     "Long.", "Molecular Sex"]
        dataset_df = dataset_df[keep_cols]

        # set - x,y coords
        umap_xy = pd.DataFrame(umap_proj_fit, columns=['x','y'])
        dataset_df['x'] = umap_xy['x']
        dataset_df['y'] = umap_xy['y']
        dataset_df['colors'].fillna("#000000", inplace=True)
        dataset_df.sort_values(by=["Sub-region"], inplace=True)
        
        # save - dataset with metadata
        dataset_df.to_csv(dataset_fn, sep="\t", index=False)

