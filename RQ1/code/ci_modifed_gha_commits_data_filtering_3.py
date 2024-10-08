import pandas as pd


input_file_path = "C:\\paper\\empirical_analysis\\data\\RQ1\\ci_modifying_commits.csv"
df = pd.read_csv(input_file_path)
initial_row_count = len(df)
print(f"Number of rows before cleaning: {initial_row_count}")
#duplicates
df = df.drop_duplicates()
#rows with any missing values
df = df.dropna()
# column names 
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
#Trim whitespace
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
final_row_count = len(df)
print(f"Number of rows after final cleaning: {final_row_count}")
output_file_path = "C:\\paper\\empirical_analysis\\data\\RQ1\\cleaned_ci_modifying_commits.csv"
df.to_csv(output_file_path, index=False)
print("Data cleaning complete. Cleaned data saved to:", output_file_path)
