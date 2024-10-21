import pandas as pd 

# open rater_1.xlsx and rater_2.xlsx, load sheet 1 into df1 and df2
#dhia
# df1 = pd.read_excel('C:\\Users\\dhiarzig\\Documents\\VSCode Projects\\MLCICoEvolutionAnlysis\\RQ1\\data\\labeled_rater_1.xlsx')
# df2 = pd.read_excel('C:\\Users\\dhiarzig\\Documents\\VSCode Projects\\MLCICoEvolutionAnlysis\\RQ1\\data\\rater_2.xlsx')

#rahul
df1 = pd.read_excel('C:\\paper\\co_evolution_analysis\\RQ1\\data\\labeled_rater_1.xlsx')
df2 = pd.read_excel('C:\\paper\\co_evolution_analysis\\RQ1\\data\\rater_2.xlsx')

# merge df1 and df2 on 'commitid' and 'gitauthor columns
df = pd.merge(df1, df2, on=['commitid', 'gitauthor'])

# print the columns of the merged dataframe
print(df.columns)

# remove projectname_y', 'commitmessage_y',  'lsof_modifiedfiles_y', 'isPR_y', 'Column1', 'PRTitle_y',  'PRDescription_y' columns
df = df.drop(['projectname_y', 'commitmessage_y',  'lsof_modifiedfiles_y', 'isPR_y', 'Column1', 'PRTitle_y',  'PRDescription_y'], axis=1)

# rename the columns of the dataframe to remove '_x' suffix
df.columns = df.columns.str.replace('_x', '')

#rename GHACategory_y to GHACategory_2
df.rename(columns={'GHACategory_y':'GHACategory_2'}, inplace=True)

# replace the values of Build Process Organization in GHACategory with Build Policy , and Build Policy with Build Process Organization
#df['GHACategory'] = df['GHACategory'].replace({'Build Process Organization': 'Build Policy', 'Build Policy': 'Build Process Organization'})

# convert GHAcategory and GHACategory_2 columns to string type
df['GHACategory'] = df['GHACategory'].astype(str)
df['GHACategory_2'] = df['GHACategory_2'].astype(str)

# calculate the kappa score between GHACategory and GHACategory_2 columns that contain the labels of the raters
from sklearn.metrics import cohen_kappa_score
kappa = cohen_kappa_score(df['GHACategory'], df['GHACategory_2'])

# kappa_score = cohen_kappa_score(df['GHACategory'], df['GHACategory_2'])
print('Kappa Score:', kappa)

# add a column 'difference' to the dataframe, which specifies if the values of GHACategory and GHACategory_2 columns are different
df['rq1_conflict'] = df['GHACategory'] != df['GHACategory_2']
# print how many conflicts are there
print('Number of conflicts RQ1:', df['rq1_conflict'].sum())

# save the dataframe to a new excel file
# df.to_excel('C:\\Users\\dhiarzig\\Documents\\VSCode Projects\\MLCICoEvolutionAnlysis\\RQ1\\data\\conflict_resolution.xlsx', index=False)

# df2 = pd.read_excel('C:\\Users\\dhiarzig\\Documents\\VSCode Projects\\MLCICoEvolutionAnlysis\\RQ2\\data\\coevolution_taxonomy.xlsx', sheet_name='rater_1')

df2 = pd.read_excel('C:\\paper\\co_evolution_analysis\\RQ2\\data\\coevolution_taxonomy.xlsx', sheet_name='rater_1')


# merge df and df2 on 'commitid' and 'gitauthor' columns

df_c = pd.merge(df, df2, on=['commitid', 'gitauthor'])

# remove projectname_y', 'commitmessage_y',  'lsof_modifiedfiles_y', 'isPR_y', 'Column1', 'PRTitle_y',  'PRDescription_y' columns
df_c = df_c.drop(['projectname_y', 'commitmessage_y',  'lsof_modifiedfiles_y', 'isPR_y', 'PRTitle_y',  'PRDescription_y'], axis=1)

# rename the columns of the dataframe to remove '_x' suffix
df_c.columns = df_c.columns.str.replace('_x', '')

# convert CoChangeCategory and Categories to string type, except for the 'rq1_conflict' column
df_c['CochangeCategory'] = df_c['CochangeCategory'].astype(str)
df_c['Categories'] = df_c['Categories'].astype(str)

# remove the [] from the labels in the Categories column
df_c['Categories'] = df_c['Categories'].str.replace('[', '').str.replace(']', '')

#remove the ' ' from the labels in the Categories column
df_c['Categories'] = df_c['Categories'].str.replace("'", "")

# compare the CochangeCategory and Categories columns. Each column is a comma separated list of labels. 
# If a label is in only one of the columns, the rq2_conflict column is set to True. Ignore spaces in the labels list. 
df_c['rq2_lab1_conflict'] = df_c.apply(lambda x: any([i.strip() not in x['CochangeCategory'].split(',') for i in x['Categories'].split(',')]), axis=1)
df_c['rq2_lab2_conflict'] = df_c.apply(lambda x: any([i.strip() not in x['Categories'].split(',') for i in x['CochangeCategory'].split(',')]), axis=1)
df_c['rq2_conflict'] = df_c['rq2_lab1_conflict'] | df_c['rq2_lab2_conflict']

# print how many conflicts are there
print('Number of conflicts RQ2:', df_c['rq2_conflict'].sum())


#drop the 'rq2_lab1_conflict' and 'rq2_lab2_conflict' columns
df_c = df_c.drop(['rq2_lab1_conflict', 'rq2_lab2_conflict'], axis=1)





# save the dataframe to a new excel file
df_c.to_excel('C:\\paper\\co_evolution_analysis\\RQ1\\data\\conflict_resolution_vrchavan.xlsx', index=False)
















