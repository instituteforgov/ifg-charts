# %%
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# %%
# LOAD DATA
df = pd.read_csv(
    'C:/Users/nyep/Institute for Government/Data - General/Public services/Schools/' +
    'DfE, Key stage 4 performance/2023, revised/2223_la_data_revised.csv'
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
# Merge Inner London and Outer London
df.loc[
    df['region_name'] == 'Inner London',
    'region_name'
] = 'London'

df.loc[
    df['region_name'] == 'Outer London',
    'region_name'
] = 'London'

# %%
# Convert pt_l2basics_94 to numeric
df.loc[
    :,
    'pt_l2basics_94'
] = pd.to_numeric(df['pt_l2basics_94'], errors='raise')

# %%
# PRODUCE CHART
fig, ax = plt.subplots()

# Produce chart
sns.swarmplot(
    x='pt_l2basics_94',
    y='region_name',
    data=df.sort_values('pt_l2basics_94'),
    dodge=True,
    hue='region_name',
    size=5,
)

# Set axis min and max
ax.set_xlim(0, 100)

# Set axis label
ax.set_ylabel('')

# Add vertical gridlines
ax.xaxis.grid(True)

# %%
