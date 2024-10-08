import pandas as pd
import csv

#  keywords related to ML

ml_keywords = ['data', 'model', 'train', 'training', 'test', 'pipeline', 'predict', 'correctness', 'deploy', 'inference', 'preprocess']

def check_ml_keywords(file_path):
    # Check if  keyword - part of the file path
    return any(keyword in file_path for keyword in ml_keywords)


df = pd.read_csv('C:\\paper\\empirical_analysis\\data\\RQ1\\cleaned_ci_modifying_commits.csv')
print(df.columns)

filtered_rows = []

for index, row in df.iterrows():
    # Strip whitespace/ ignore empty strings
    modified_files = [file.strip() for file in row['lsof_modifiedfiles'].split(',') if file.strip()]

    has_python_file = any(file.endswith('.py') for file in modified_files)
    has_ml_keyword_file = any(check_ml_keywords(file) for file in modified_files if file.endswith('.py'))

    if has_python_file and has_ml_keyword_file:
        filtered_rows.append(row)
filtered_df = pd.DataFrame(filtered_rows)
final_row_count = len(filtered_df)
print(f"Number of rows after final cleaning: {final_row_count}")

filtered_df.to_csv('C:\\paper\\empirical_analysis\\data\\RQ1\\filtered_ml_gha_commits.csv', index=False)
