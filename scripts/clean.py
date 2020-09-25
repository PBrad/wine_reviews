#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 07:47:27 2020

@author: patrickbradshaw

Clean / filter wine review dataset for Tableau training.

Break off separate dataset of top words used to describe
wine variety / wines from different countries.
"""

# =============================================================================
# Packages 
# =============================================================================

import pandas as pd
import spacy

nlp = spacy.load('en_core_web_sm', parser = False, entity = False)

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

# Tokenize
df_top['tokens'] = df_top['description'].str.lower().apply(lambda x: x.split(' '))

# Convert each set of tokens to individual rows (one per token), while retaining index
df_text = df_top['tokens'].explode()

# Remove punctuation
df_text = df_text.str.replace('[^\w\s]','')

# Remove stopwords
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS       

df_text = df_text[~df_text.isin(spacy_stopwords)] 
df_text = df_text[~df_text.isin(['wine', 'wines'])]

# Move index to explicit id column
df_text = df_text.reset_index()
df_text = df_text.rename(columns = {'index': 'id'})

# Rejoin info about each wine from df_top
df_top.columns
del df_top['tokens']

df_text = pd.merge(df_text, df_top, how = 'left', on = 'id')

# Get top 50 words for each variety and country
df_top_words = pd.DataFrame()

for var in ['variety', 'country']:
    print(var) 
    tmp_df = df_text.groupby(var)['tokens'].value_counts(sort = True)
    tmp_df = tmp_df.groupby(var).head(50) 
    tmp_df = pd.DataFrame(tmp_df)
    tmp_df = tmp_df.rename(columns = {'tokens': 'count'}).reset_index()
    tmp_df = tmp_df.rename(columns = {'variety': 'variable', 'country': 'variable'})
    tmp_df['tag'] = var
    
    df_top_words = df_top_words.append(tmp_df, ignore_index = True)

df_top_words.groupby(['tag'])['variable'].value_counts()

# TODO
# Could also look at top words for most expensive / least expensive; 
# and best rated / worst rated

# =============================================================================
# Best/Worst Review Examples
# =============================================================================

df_best = df_top.sort_values(by = 'points', ascending = False).groupby(['variety']).head(5)
df_best = df_best[['description', 'points', 'price', 'variety', 'country']]
df_best['tag'] = 'best reviews'

df_worst = df_top.sort_values(by = 'points', ascending = False).groupby(['variety']).tail(5)
df_worst = df_worst[['description', 'points', 'price', 'variety', 'country']]
df_worst['tag'] = 'worst reviews'

df_best_worst = df_best.append(df_worst, ignore_index = True)

# =============================================================================
# Write out
# =============================================================================

# Main review dataset
del df_top['description'] # drop full text descriptions
df_top.to_csv('res/wine_main.csv')

# Top words
df_top_words.to_csv('res/wine_top_words.csv')

# Best/Worst Review Examples
df_best_worst.to_csv('res/wine_best_worst.csv')