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
# LOAD DATA
df = pd.read_csv(
    'C:/Users/nyep/Institute for Government/Data - General/Public services/Schools/' +
    'DfE, Key stage 2 performance/2023, revised/' +
    'ks2_regional_and_local_authority_2016_to_2023_revised.csv'
)

# %%
# EDIT DATA
# Restrict to 202223
df = df[df['time_period'] == 202223]

# %%
# Restrict to LA-level
df = df[df['geographic_level'] == 'Local authority']

# %%
# Restrict to Total gender
df = df[df['gender'] == 'Total']

# %%
# Convert pt_rwm_met_expected_standard to numeric
df.loc[
    :,
    'pt_rwm_met_expected_standard'
] = pd.to_numeric(df['pt_rwm_met_expected_standard'], errors='raise')

# %%
# PRODUCE CHART
fig, ax = plt.subplots()

# %%
# Produce chart
dot_size = 10

while dot_size > 0:
    try:
        plt.clf()
        sns.swarmplot(
            x='pt_rwm_met_expected_standard',
            y='region_name',
            data=df.sort_values('pt_rwm_met_expected_standard'),
            hue='region_name',
            size=dot_size,
        )
    except UserWarning:
        dot_size -= 0.5
        pass
    else:
        print(f"Dot size: {dot_size}")
        break

# %%
