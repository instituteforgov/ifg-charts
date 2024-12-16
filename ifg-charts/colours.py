# %%
# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Purpose
        Read in IfG palette
    Inputs
        - xlsx: 'IfG colour palette.xlsx'
    Outputs
        None
    Parameters
        None
    Notes
        None
"""

import os

import pandas as pd

# %%
# READ IN DATA
file_path = os.path.join(
    'C:/Users/',
    os.getlogin(),
    'Institute for Government/Resources - General/'
    'Data visualisation guides and templates',
    'IfG colour palette.xlsx'
)

df = pd.read_excel(
    file_path,
    sheet_name='Core',

)

# %%
# EDIT DATA
# Forward fill Colour column
df['Colour'] = df['Colour'].ffill()

# %%
# Merge rows by Colour, turning columns into an 'rgh(x, y, z)' string
df = df.groupby('Colour').agg(
    {
        'Darker 50%': lambda x: f"rgb({x.iloc[0]}, {x.iloc[1]}, {x.iloc[2]})",
        'Darker 25%': lambda x: f"rgb({x.iloc[0]}, {x.iloc[1]}, {x.iloc[2]})",
        'ACCENT': lambda x: f"rgb({x.iloc[0]}, {x.iloc[1]}, {x.iloc[2]})",
        'Lighter 40%': lambda x: f"rgb({x.iloc[0]}, {x.iloc[1]}, {x.iloc[2]})",
        'Lighter 60%': lambda x: f"rgb({x.iloc[0]}, {x.iloc[1]}, {x.iloc[2]})",
        'Lighter 80%': lambda x: f"rgb({x.iloc[0]}, {x.iloc[1]}, {x.iloc[2]})",
    }
).reset_index()

# %%
# Remove colour string (e.g. #00a8e1) from Colour column
df['Colour'] = df['Colour'].str.replace(
    r'\s#.{6}',
    '',
    regex=True
).str.replace(
    r'\s',
    '_',
    regex=True
).str.lower()

# %%
df.columns = df.columns.str.replace(
    r'\s',
    '_',
    regex=True
).str.lower()

# %%
df

# %%
# Convert to dictionary
df.set_index('colour').to_dict(orient='index')

# %%
