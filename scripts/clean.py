#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 07:47:27 2020

@author: patrickbradshaw
"""

# =============================================================================
# Packages 
# =============================================================================

import pandas as pd

# =============================================================================
# Load
# =============================================================================

df = pd.read_csv('data/winemag-data-130k-v2.csv')

# =============================================================================
# Inspect
# =============================================================================

df.head()
df.columns

df['Unnamed: 0']

# Check dups
cols = list(df.columns)
del cols[0] # subset on everything except first column (row number)

len(df) # 129971
len(df.drop_duplicates()) # 129971
len(df.drop_duplicates(subset = cols)) # 119988

# Drop complete dups
df = df.drop_duplicates(subset = cols)

# Drop the old index
del df['Unnamed: 0']

len(df.drop_duplicates()) # 119988 - good

# Vars
for var in cols:
    print('--------------------------------')
    print(df[var].value_counts(sort = True))
    
# =============================================================================
# Retain largest types of wine 
# =============================================================================

# Since we're using this for a training, let's make the dataset a little
# smaller / more manageable

top_varieties = df['variety'].value_counts(sort = True)

# Keep top 20
len(top_varieties[0:20])

top_varieties = list(top_varieties[0:20].index)

len(df[df['variety'].isin(top_varieties)]) # 86807

df_top = df[df['variety'].isin(top_varieties)]

del top_varieties

len(df_top) # 86807 - Good

# Now inspect again
for var in cols:
    print('--------------------------------')
    print(df_top[var].value_counts(sort = True))

# Reset the index and retain it as an explicit ID
df_top = df_top.reset_index(drop = True)

df_top = df_top.reset_index()
df_top = df_top.rename(columns = {'index': 'id'})

# =============================================================================
# Break off text and identify top words
# =============================================================================

df_top['description']

# Something like this would work
#df_new = pd.concat([pd.DataFrame({'description': doc, 'id': row['id']}, index=[0]) 
#           for _, row in df_top.iterrows() 
#           for doc in row['docs'].split('.') if doc != ''])
