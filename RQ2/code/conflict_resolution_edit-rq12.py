import pandas as pd
from sklearn.metrics import cohen_kappa_score

# Load the data from rater 1 and rater 2
df1 = pd.read_excel('C:\\paper\\co_evolution_analysis\\RQ2\\data\\coevolution_taxonomy.xlsx', sheet_name='rater_1')
df2 = pd.read_excel('C:\\paper\\co_evolution_analysis\\RQ2\\data\\rater_2.xlsx')

# Merge df1 and df2 on 'commitid' and 'gitauthor' columns
df = pd.merge(df1, df2, on=['commitid', 'gitauthor'])

# Drop unnecessary columns
df = df.drop(['projectname_y', 'commitmessage_y','GHACategory' ,  'lsof_modifiedfiles_y', 'isPR_y', 'PRTitle_y', 'PRDescription_y'], axis=1)

# Clean up the column names by removing '_x' suffix
df.columns = df.columns.str.replace('_x', '')

# Convert CoChangeCategory and Categories to string type
df['CochangeCategory'] = df['CochangeCategory'].astype(str)
df['Categories'] = df['Categories'].astype(str)


# Convert the Categories and CochangeCategory columns into sets of labels, ignoring order
df['Categories_set'] = df['Categories'].apply(lambda x: set([i.strip() for i in x.split(',')]))
df['CochangeCategory_set'] = df['CochangeCategory'].apply(lambda x: set([i.strip() for i in x.split(',')]))

# Identify conflicts between CochangeCategory_set and Categories_set
df['rq2_conflict'] = df.apply(lambda x: x['Categories_set'] != x['CochangeCategory_set'], axis=1)

# Print the number of conflicts for RQ2
print('Number of conflicts RQ2:', df['rq2_conflict'].sum())

# Calculate the Cohen's Kappa score between the two raters' labels
# We first convert the sets back into sorted comma-separated strings for compatibility with kappa
df['Categories_sorted'] = df['Categories_set'].apply(lambda x: ','.join(sorted(x)))
df['CochangeCategory_sorted'] = df['CochangeCategory_set'].apply(lambda x: ','.join(sorted(x)))

kappa = cohen_kappa_score(df['Categories_sorted'], df['CochangeCategory_sorted'])
print('Kappa Score for RQ2:', kappa)

# Drop the intermediate set columns
df = df.drop(['Categories_set', 'CochangeCategory_set'], axis=1)

# Save the resulting dataframe to a new Excel file
df.to_excel('C:\\paper\\co_evolution_analysis\\RQ2\\data\\conflict_resolution_rq2.xlsx', index=False)
