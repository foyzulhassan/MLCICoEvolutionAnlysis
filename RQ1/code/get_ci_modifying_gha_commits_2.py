import pandas as pd
import os
from git import Repo
import csv

def contains_workflow_yml_files(modified_files):
    # This function checks if any .yml file within the .github/workflows directory was modified
    workflow_dir = '.github/workflows/'
    for file_path in modified_files:
        if file_path.startswith(workflow_dir) and file_path.endswith('.yml'):
            return True
    return False

# Define the path where repositories are cloned
clone_repo_path = 'C:\\paper\\empirical_analysis\\data\\repos'

# Open or create the CSV file for writing commit data
output_path = "C:\\paper\\empirical_analysis\\data\\RQ1\\ci_modifying_commits.csv"
with open(output_path, "w", newline='', encoding='utf-8') as write_file:
    header = ['GitAuthor', 'ProjectName', 'CommitID', 'CommitMessage', 'Lsof ModifiedFiles']
    writer = csv.writer(write_file)
    writer.writerow(header)

    # Read the dataframe containing repository names
    input_csv_path = 'C:\\paper\\empirical_analysis\\data\\RQ1\\repo_list.csv'
    readDataframe = pd.read_csv(input_csv_path)
    for index, row in readDataframe.iterrows():
        repo_name = row['RepoName']
        file_path = os.path.join(clone_repo_path, repo_name)

        if os.path.isdir(file_path):
            print(f"Reading from Repository: {repo_name}")
            try:
                local_repo = Repo(file_path)
                commits = list(local_repo.iter_commits())
                for commit in commits:
                    if contains_workflow_yml_files(commit.stats.files.keys()):
                        # Collect commit data
                        author = commit.author.name
                        commit_id = commit.hexsha
                        message = commit.message.strip().replace('\n', ' ')  # Clean up newlines in commit message
                        modified_files = ', '.join(commit.stats.files.keys())  # Get all modified files as a string
                        writer.writerow([author, repo_name, commit_id, message, modified_files])
            except Exception as e:
                print(f"Error processing repository {repo_name}: {e}")
        else:
            print(f"Directory for {repo_name} does not exist.")