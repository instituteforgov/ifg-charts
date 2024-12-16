# %%
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
df = pd.read_csv(dataset_parameters[dataset]['file_path'])

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

        # Produce plot
        sns.swarmplot(
            x=dataset_parameters[dataset]['value_metric'],
            y=dataset_parameters[dataset]['group_by'],
            data=df.sort_values(dataset_parameters[dataset]['value_metric']),
            hue=dataset_parameters[dataset]['group_by'],
            size=dot_size,
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
