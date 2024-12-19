# %%
# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Purpose
        Draw beeswarm plot of prison assaults data
    Inputs
        - xlsx: 'prison_annualvariation_v3.xlsx'
        - pkl: 'data/ifg_palette.pkl'
            - IfG colour palette
    Outputs
        None
    Parameters
        - dataset_parameters
            - file_path: Path to dataset
            - time_period: Time period to use
            - geographic_level: Geographic level to use
            - gender: Gender to use
            - value_metric: Metric to use
            - group_by: Group by column
        - dataset: Dataset to use
        - average: Type of average to display overlaid onto beeswarm
    Notes
        - Categories are ordered by
            - Average, where averages are applied
            - Lowest value, where they are not
"""

import warnings

import pandas as pd

from functions import draw_beeswarm, load_colours

# %%
# SET UP
# Turn seaborn UserWarnings into exceptions
warnings.filterwarnings("error", category=UserWarning, module="seaborn")

# %%
# LOAD DATA
# Data
df = pd.read_excel(
    'C:/Users/nyep/Institute for Government/' +
    'Research - Public services/Projects/Performance Tracker' +
    '/PT2024/1. Lit review and analysis/9. Prisons and probation/Stata work/' +
    'prison_annualvariation_v3.xlsx',
    sheet_name='prisonerprisonerassault2023',
    usecols='M:P'
).dropna()

# Rename column
df = df.rename(
    columns={
        'Prison Name.1': 'Prison Name',
    }
)

# Rename categories
df['Category'] = df['Category'].replace(
    {
        'Highsecurity': 'High security',
        'CatB': 'Category B',
        'CatC_trainer': 'Category C trainer',
        'CatC_resettle': 'Category C resettlement',
        'CatC_both': 'Category C both',
        'Open': 'Open',
        'Reception': 'Reception',
        'female': 'Female',
    }
)

# %%
# df_points['Category'].unique()

# %%
# Colours
df_colours = load_colours()

# Drop 'darker_50%', 'darker_25%', 'lighter_40%' rows
df_colours = df_colours[
    ~df_colours['colour_shade'].str.contains('|'.join(['darker_50%', 'darker_25%', 'lighter_40%']))
]

# Drop 'dark_grey' rows
df_colours = df_colours[
    ~df_colours['colour_shade'].str.contains('dark_grey')
]

# %%
# EDIT DATA
# Copy df
df_points = df.copy()

# %%
# Convert size metric to numeric
df_points.loc[
    :,
    'Population'
] = pd.to_numeric(df_points['Population'], errors='raise')

# %%
# Convert value metric to numeric
df_points.loc[
    :,
    'Assaults'
] = pd.to_numeric(df_points['Assaults'], errors='raise')

# %%
# CALCULATE AVERAGES
df_avgs = df_points.groupby(
    'Category'
)['Assaults'].agg("median").reset_index()

# %%
# PRODUCE CHART
ax = draw_beeswarm(
    data=df_points,
    value_metric='Assaults',
    group_by='Category',
    orientation='horizontal',
    ax_min=0,
    ax_max=900,
    order=[
        'High security',
        'Category B',
        'Category C trainer',
        'Category C resettlement',
        'Category C both',
        'Open',
        'Reception',
        'Female',
    ],
    averages=df_avgs,
    average_label='Median',
    palette=df_colours.head(
        df_points['Category'].nunique()
    )['colour_hex'].tolist(),
)

# %%
ax.figure.savefig(
    'test.png',
    bbox_inches='tight',
)
