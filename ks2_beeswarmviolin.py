# %%
import pandas as pd
import seaborn as sns

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
sns.swarmplot(
    x='pt_rwm_met_expected_standard',
    y='region_name',
    data=df.sort_values('pt_rwm_met_expected_standard'),
    dodge=True,
    hue='region_name',
    size=8,
)

# %%
sns.violinplot(
    x='pt_rwm_met_expected_standard',
    y='region_name',
    data=df.sort_values('pt_rwm_met_expected_standard'),
    hue='region_name',
)

# %%
