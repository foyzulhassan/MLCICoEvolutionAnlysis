import pandas as pd

# Load the original CSV file
df = pd.read_csv('C:\\paper\\empirical_analysis\\data\\RQ1\\new\\ML_Sampled_GHA_Projects_with_PR_details.csv')

# Remove the 'Status' column if it exists
if 'Status' in df.columns:
    df = df.drop('Status', axis=1)

# new empty column 'GHACategory'
df['GHACategory'] = ''

# Save the modified DataFrame to two new Excel files
df.to_excel('C:\\paper\\empirical_analysis\\data\\RQ1\\new\\rater_1.xlsx', index=False)
df.to_excel('C:\\paper\\empirical_analysis\\data\\RQ1\\new\\rater_2.xlsx', index=False)

final_row_count = len(df)
print(f"Number of rows after final cleaning: {final_row_count}")
print("Excel files for rater_1 and rater_2 have been created successfully.")
