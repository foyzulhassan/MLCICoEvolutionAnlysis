import pandas as pd
from sklearn.metrics import cohen_kappa_score
import numpy as np
import re

# Load the data from rater 1 and rater 2
df1 = pd.read_excel('C:\\paper\\co_evolution_analysis\\RQ2\\data\\RQ2_coevolution_taxonomy_travis.xlsx', sheet_name='rater_1')
df2 = pd.read_excel('C:\\paper\\co_evolution_analysis\\RQ2\\data\\RQ2_coevolution_taxonomy_travis.xlsx', sheet_name='rater_2')

# Merge df1 and df2 on 'commitid' and 'gitauthor' columns
df = pd.merge(df1, df2, on=['CommitID', 'GitAuthor'])

# Clean up the column names by removing '_x' suffix
df.columns = df.columns.str.replace('_x', '')

# Convert CoChangeCategory and Categories to string type
df['Categories'] = df['Categories'].astype(str)
df['Categories_y'] = df['Categories_y'].astype(str)

# Remove unwanted characters like extra quotes and square brackets
def clean_labels(label_str):
    cleaned = re.sub(r'[\'\"\[\]]', '', label_str)
    return [label.strip() for label in cleaned.split(',') if label.strip()]

df['Categories'] = df['Categories'].apply(clean_labels)
df['Categories_y'] = df['Categories_y'].apply(clean_labels)

# Define the list of specific categories to check
categories = [
    'bug fixing', 'dependency management', 'feature development', 'code cleanup', 
    'refactoring', 'security', 'data and model versioning', 'testing', 'model training', 
    'documentation', 'pipeline automation', 'integration', 'performance optimization', 
    'deployment'
]

# Create separate columns for each label for both raters based on the defined categories
for label in categories:
    df[f'rater1_{label}'] = df['Categories'].apply(lambda x: 1 if label in x else 0)
    df[f'rater2_{label}'] = df['Categories_y'].apply(lambda x: 1 if label in x else 0)

# Calculate Cohen's Kappa score for each label and store them in a list, handling NaN results
kappa_scores = []
for label in categories:
    try:
        kappa = cohen_kappa_score(df[f'rater1_{label}'], df[f'rater2_{label}'])
    except ValueError:
        kappa = np.nan  # Assign NaN if there is a ValueError due to a lack of variability
    
    # Store the kappa score only if it's not NaN
    kappa_scores.append(kappa)
    print(f'Kappa Score for {label}: {kappa}')

# Calculate the average kappa score, ignoring NaN values
average_kappa = np.nanmean(kappa_scores)
print('Average Kappa Score for RQ2:', average_kappa)

# Select only the desired columns for the final output
final_columns = ['GitAuthor', 'ProjectName', 'CommitID', 'CommitMessage', 'Categories', 'Categories_y'] + \
                [f'rater1_{label}' for label in categories] + [f'rater2_{label}' for label in categories]

# Create the final DataFrame with the selected columns
df_final = df[final_columns]

# Save the resulting dataframe to a new Excel file
df_final.to_excel('C:\\paper\\co_evolution_analysis\\RQ2\\data\\conflict_resolution_rq2_travis.xlsx', index=False)
