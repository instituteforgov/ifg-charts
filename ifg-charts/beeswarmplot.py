# %%
# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Purpose
        Draw a beeswarm plot
    Inputs
        - csv: 'ks2_regional_and_local_authority_2016_to_2023_revised.csv'
            - 2022-23 KS2 results data
        - csv: '2223_la_data_revised.csv'
            - 2022-23 KS4 results data
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

import os
import warnings

import pandas as pd

from functions import draw_beeswarm

# %%
# SET UP
# Turn seaborn UserWarnings into exceptions
warnings.filterwarnings("error", category=UserWarning, module="seaborn")

# %%
# SET PARAMETERS
dataset_parameters = {
    'ks2_revised_2023': {
        'file_path':
            'C:/Users/nyep/Institute for Government/Data - General/Public services/Schools/' +
            'DfE, Key stage 2 performance/2023, revised/' +
            'ks2_regional_and_local_authority_2016_to_2023_revised.csv',
        'time_period': 202223,
        'geographic_level': 'Local authority',
        'gender': 'Total',
        'value_metric': 'pt_rwm_met_expected_standard',
        'group_by': 'region_name',
    },
    'ks4_revised_2023': {
        'file_path':
            'C:/Users/nyep/Institute for Government/Data - General/Public services/Schools/' +
            'DfE, Key stage 4 performance/2023, revised/' +
            '2223_la_data_revised.csv',
        'time_period': 202223,
        'geographic_level': 'Local authority',
        'gender': 'Total',
        'value_metric': 'pt_l2basics_94',
        'group_by': 'region_name',
    },
}

# %%
# dataset = 'ks2_revised_2023'
dataset = 'ks4_revised_2023'

# %%
# average = None
# average = 'median'
average = 'data'

# %%
# LOAD DATA
# Data
df = pd.read_csv(dataset_parameters[dataset]['file_path'])

# %%
# Colours
df_colours = pd.read_pickle(
    os.path.join(
        '../',
        os.path.dirname(os.getcwd()),
        'data/',
        'ifg_palette.pkl'
    )
)

# Reshape
df_colours = df_colours.melt(
    id_vars='colour',
    var_name='shade',
    value_name='colour_rgb'
)

# Merge colour, shade columns
df_colours.insert(0, 'colour_shade', pd.NA)
df_colours['colour_shade'] = df_colours['colour'].str.cat(df_colours['shade'], sep='_')

# Drop 'darker_50%' and 'darker_25%' rows
df_colours = df_colours[
    ~df_colours['shade'].isin([
        'darker_50%',
        'darker_25%',
        'lighter_40%',
    ])
]

# Drop colour and shade columns
df_colours.drop(columns=['colour', 'shade'], inplace=True)

# Convert colours to hex code
df_colours['colour_rgb'] = df_colours['colour_rgb'].apply(
    lambda x: x.replace('rgb(', '').replace(')', '').replace(' ', '').split(',')
).apply(
    lambda x: f"#{int(x[0]):02x}{int(x[1]):02x}{int(x[2]):02x}"
)

# %%
# EDIT DATA
# Copy df
df_points = df.copy()

# Restrict to selected time period
df_points = df_points[df_points['time_period'] == dataset_parameters[dataset]['time_period']]

# %%
# Restrict to selected geographic level
df_points = df_points[
    df_points['geographic_level'] == dataset_parameters[dataset]['geographic_level']
]

# %%
# Restrict to Total gender
df_points = df_points[df_points['gender'] == dataset_parameters[dataset]['gender']]

# %%
# Merge Inner London and Outer London
if dataset == 'ks4_revised_2023':
    df_points.loc[
        df_points['region_name'] == 'Inner London',
        'region_name'
    ] = 'London'

    df_points.loc[
        df_points['region_name'] == 'Outer London',
        'region_name'
    ] = 'London'

# %%
# Convert metric to numeric
df_points.loc[
    :,
    dataset_parameters[dataset]['value_metric']
] = pd.to_numeric(df_points[dataset_parameters[dataset]['value_metric']], errors='raise')

# %%
# CALCULATE AVERAGES
if average == 'median':
    df_avgs = df_points.groupby(
        dataset_parameters[dataset]['group_by']
    )[dataset_parameters[dataset]['value_metric']].agg("median").reset_index()

elif average == 'data':
    df_avgs = df.copy()
    df_avgs = df_avgs[df_avgs['time_period'] == dataset_parameters[dataset]['time_period']]
    df_avgs = df_avgs[
        df_avgs['geographic_level'] == 'Regional'
    ]
    df_avgs = df_avgs[df_avgs['gender'] == dataset_parameters[dataset]['gender']]

    # Handle KS4 data
    # NB: London comes pre-calculated at regional level (just all LAs are recorded
    # against either Inner or Outer London)
    if dataset == 'ks4_revised_2023':
        df_avgs = df_avgs[
            ~df_avgs['region_name'].isin(['Inner London', 'Outer London'])
        ]

    # Convert metric to numeric
    df_avgs.loc[
        :,
        dataset_parameters[dataset]['value_metric']
    ] = pd.to_numeric(df_avgs[dataset_parameters[dataset]['value_metric']], errors='raise')

else:
    df_avgs = None

# %%
# CHECKS
# Check number of averages matches number of groups
if average is not None:
    assert \
        df_avgs.shape[0] == df_points[dataset_parameters[dataset]['group_by']].nunique(), \
        "Number of averages does not match number of groups"

# %%
# PRODUCE CHART
draw_beeswarm(
    data=df_points,
    value_metric=dataset_parameters[dataset]['value_metric'],
    group_by=dataset_parameters[dataset]['group_by'],
    orientation='horizontal',
    averages=df_avgs,
    palette=df_colours.head(
        df_points[dataset_parameters[dataset]['group_by']].nunique()
    )['colour_rgb'].tolist(),
)

# %%
