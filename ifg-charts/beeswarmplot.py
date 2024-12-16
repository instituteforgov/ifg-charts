# %%
import os
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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
# Restrict to 202223
df = df[df['time_period'] == dataset_parameters[dataset]['time_period']]

# %%
# Restrict to LA-level
df = df[df['geographic_level'] == dataset_parameters[dataset]['geographic_level']]

# %%
# Restrict to Total gender
df = df[df['gender'] == dataset_parameters[dataset]['gender']]

# %%
# Merge Inner London and Outer London
if dataset == 'ks4_revised_2023':
    df.loc[
        df['region_name'] == 'Inner London',
        'region_name'
    ] = 'London'

    df.loc[
        df['region_name'] == 'Outer London',
        'region_name'
    ] = 'London'

# %%
# Convert metric to numeric
df.loc[
    :,
    dataset_parameters[dataset]['value_metric']
] = pd.to_numeric(df[dataset_parameters[dataset]['value_metric']], errors='raise')

# %%
# CALCULATE AVERAGES
df_avgs = df.groupby(
    dataset_parameters[dataset]['group_by']
)[dataset_parameters[dataset]['value_metric']].agg("median").reset_index()

# %%
# CHECKS
# Check number of averages matches number of groups
assert \
    df_avgs.shape[0] == df[dataset_parameters[dataset]['group_by']].nunique(), \
    "Number of averages does not match number of groups"

# %%
# PRODUCE CHART
dot_size = 10

while dot_size > 0:
    try:

        # Set axis min and max
        plt.xlim(0, 100)

        # Add vertical gridlines
        plt.grid(axis='x')

        # Remove axis tick marks
        plt.tick_params(
            axis='both',
            which='both',
            bottom=False,
            left=False,
        )

        # Remove border
        plt.box(False)

        # Draw averages
        if df_avgs is not None:
            ax = sns.scatterplot(
                x=dataset_parameters[dataset]['value_metric'],
                y=dataset_parameters[dataset]['group_by'],
                marker='|',
                linewidth=2,
                color='#333F48',
                s=250,
                zorder=4,
                legend=False,
                data=df_avgs
            )
        else:
            ax = plt.gca()

        # Produce plot
        sns.swarmplot(
            x=dataset_parameters[dataset]['value_metric'],
            y=dataset_parameters[dataset]['group_by'],
            data=df.sort_values(dataset_parameters[dataset]['value_metric']),
            hue=dataset_parameters[dataset]['group_by'],
            palette=df_colours.head(
                df[dataset_parameters[dataset]['group_by']].nunique()
            )['colour_rgb'].tolist(),
            size=dot_size,
            ax=ax
        )

        # Set axis label
        # NB: This needs to be after creation of the plot,
        # otherwise default labels are added
        plt.xlabel('')
        plt.ylabel('')

    except UserWarning:
        dot_size -= 0.5
        plt.clf()
        pass

    else:
        print(f"Dot size: {dot_size}")
        break

# %%
