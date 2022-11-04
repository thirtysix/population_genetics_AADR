#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python vers. 3.8.0 ###########################################################
# Libraries ####################################################################

from os.path import dirname, join
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput, Spinner, Legend, Range1d, DataTable, TableColumn, Button, CustomJS, MultiChoice
from bokeh.plotting import figure, output_file, output_notebook, show, save

################################################################################
# Description/Notes ############################################################
################################################################################
"""
Code adapted from Bokeh demo of interactive movie chart:
https://github.com/bokeh/bokeh/blob/branch-3.0/examples/server/app/movies/main.py

"""


################################################################################
# Base-level Functions #########################################################
################################################################################



################################################################################
# Task-specific Functions ######################################################
################################################################################
def select_individuals():
    subregion_val = subregion_input.value
    country_val = country_input.value
    country_multi_choice_val = country_multi_choice_input.value
    min_year_val = min_year_input.value
    max_year_val = max_year_input.value

    # select - by year values
    selected = dataset_df[(dataset_df['YBP']>=int(min_year_val)) &
                          (dataset_df['YBP']<=int(max_year_val))]

    # select - subregion if not "ALL"
    if (subregion_val != "ALL"):
        selected = selected[selected['Sub-region']==subregion_val]

    if ("ALL" not in country_multi_choice_val):
        selected = selected[selected['Country'].isin(country_multi_choice_val)]

    return selected


def update():
    df = select_individuals()
    p.title.text = "%d individuals selected" % len(df)        
    source.data = dict(
        x = df.x,
        y = df.y,
        subregion = df['Sub-region'],
        colors = df['colors'],
        GeneticID = df['Genetic ID'],
        Publication = df['Publication'],
        YBP = df['YBP'],
        GroupID = df['Group ID'],
        Country = df['Country'],
        Lat = df['Lat.'],
        Long = df['Long.'],
        Sex = df['Molecular Sex'])


################################################################################
# Initiating Variables #########################################################
################################################################################
# load - data
dataset_df = pd.read_csv('dataset.tsv', sep="\t")

################################################################################
# Execution ####################################################################
################################################################################
# load - html description
desc = Div(text=open(join(dirname(__file__), "description.html")).read(), sizing_mode="stretch_width")

# input - controls
subregion_input = Select(title="Subregion", value="ALL", options= ["ALL"] + sorted(dataset_df['Sub-region'].unique().tolist()))
country_input = Select(title="Country", value="ALL", options=["ALL"] + sorted(dataset_df['Country'].unique().tolist()))
min_year_input = Slider(title="Years before present start", start=dataset_df.YBP.min(), end=dataset_df.YBP.max(), value=dataset_df.YBP.min(), step=100)
max_year_input = Slider(title="Years before present end", start=dataset_df.YBP.min(), end=dataset_df.YBP.max(), value=dataset_df.YBP.max(), step=100)

country_multi_choice_input = MultiChoice(title="Country", value=["ALL"], options=["ALL"] + sorted(dataset_df['Country'].unique().tolist()), search_option_limit=10, sizing_mode="fixed", width=300)


# set - initial selection of all source data
source = ColumnDataSource(data=dict(
    x = dataset_df['x'],
    y = dataset_df['y'],
    subregion = dataset_df['Sub-region'],
    colors = dataset_df.colors,
    GeneticID = dataset_df['Genetic ID'],
    Publication = dataset_df['Publication'],
    YBP = dataset_df['YBP'],
    GroupID = dataset_df['Group ID'],
    Country = dataset_df['Country'],
    Lat = dataset_df['Lat.'],
    Long = dataset_df['Long.'],
    Sex = dataset_df['Molecular Sex']))

# set - hover data categories
TOOLTIPS = [
    ("subregion", "@subregion"),
    ("GeneticID", "@GeneticID"),
    ("Publication", "@Publication"),
    ("YBP", "@YBP"),
    ("GroupID", "@GroupID"),
    ("Country", "@Country"),
    ("Lat", "@Lat"),
    ("Long", "@Long"),
    ("Sex", "@Sex")]


# build - figure and plot
p = figure(width=1350, height=1350, title="", tooltips=TOOLTIPS, toolbar_location="below")
p.x_range = Range1d(-15,25)
p.y_range = Range1d(-15,25)
##p.add_layout(Legend(), 'right')
points = p.circle(x="x", y="y", source=source, size=3, color='colors', line_color=None, legend_field="subregion")

# build - user controls; circle size
spinner = Spinner(
    title="Circle size",  # a string to display above the widget
    low=1,  # the lowest possible number to pick
    high=20,  # the highest possible number to pick
    step=1,  # the increments by which the number can be adjusted
    value=points.glyph.size,  # the initial value to display in the widget
    width=200,  #  the width of the widget in pixels
    )
spinner.js_link("value", points.glyph, "size")

# build - data table
columns = [
    TableColumn(field="YBP", title="YBP", width=75),
    TableColumn(field="GeneticID", title="GeneticID", width=200),
    TableColumn(field="subregion", title="Sub-region", width=150),
    TableColumn(field="Country", title="Country", width=150),
    TableColumn(field="GroupID", title="GroupID", width=150),
    TableColumn(field="Sex", title="Sex", width=20),
    TableColumn(field="Lat", title="Lat.", width=75),
    TableColumn(field="Long", title="Long.", width=75),
    TableColumn(field="Publication", title="Publication")]
    
data_table = DataTable(source=source, columns=columns, width=900, height=1100)
button = Button(label="Download TSV", button_type="success")
button.js_on_click(CustomJS(args=dict(source=source),
                            code=open(join(dirname(__file__), "download.js")).read()))

# update - all controls
##controls = [subregion_input, country_input, min_year_input, max_year_input]
controls = [subregion_input, country_multi_choice_input, min_year_input, max_year_input, ]


for control in controls:
    control.on_change('value', lambda attr, old, new: update())

# set - layout
inputs = column(*controls, width=320, height=800)
##layout = column(desc, row(column(spinner, inputs), p, sizing_mode="inherit"), sizing_mode="stretch_width", height=1200)
layout = column(desc, row(column(spinner, inputs), p, column(button, data_table), sizing_mode="inherit"), height=1200)

# output
output_file(filename="umap.html", title="Individuals: "+str(len(dataset_df)))

# 
update()  # initial load of the data
curdoc().add_root(layout)
curdoc().title = "AADR_UMAP"









