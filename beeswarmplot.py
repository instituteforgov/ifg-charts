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
fig, ax = plt.subplots()

# Produce chart
dot_size = 10

while dot_size > 0:
    try:
        plt.clf()
        sns.swarmplot(
            x=dataset_parameters[dataset]['value_metric'],
            y='region_name',
            data=df.sort_values(dataset_parameters[dataset]['value_metric']),
            hue='region_name',
            size=dot_size,
        )
    except UserWarning:
        dot_size -= 0.5
        pass
    else:
        print(f"Dot size: {dot_size}")
        break

# Set axis min and max
ax.set_xlim(0, 100)

# Set axis label
ax.set_ylabel('')

# Add vertical gridlines
ax.xaxis.grid(True)

# Remove axis tick marks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')

# Remove border
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# %%
