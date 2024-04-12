import pandas as pd
import os
from git import Repo
import csv

def get_file_name(info):
    lsofNames = []
    for n, dict_ in info.items():
        lsofNames.append(n)
    return lsofNames

def check_for_ml_keywords(filename):
    keywords = ['data', 'model', 'train', 'training', 'test', 'pipeline', 'predict', 'correctness', 'deploy', 'inference', 'preprocess']
    return any(keyword in filename for keyword in keywords)

# Define the path where repositories are cloned
clone_repo_path = 'C:\\projects\\Prof.Hassan_Foyzul_Research_Work\\ClonedRepos'

# Open or create the CSV file for writing commit data
with open("C:\\projects\\Prof.Hassan_Foyzul_Research_Work\\Analysis\\commits_list_gha_projects_filtered_csv", "a", newline='', encoding='utf-8') as write_file:
    header = ['GitAuthor', 'ProjectName', 'CommitID', 'CommitMessage', 'Lsof ModifiedFiles']
    writer = csv.writer(write_file)
    writer.writerow(header)

    # Read the dataframe containing repository names
    readDataframe = pd.read_csv('C:\\projects\\Prof.Hassan_Foyzul_Research_Work\\Analysis\\primary_ds_csv_v1.csv')
    for index, row in readDataframe.iterrows():
        repo_name = row['RepoName']
        file_path = os.path.join(clone_repo_path, repo_name)
        
        if os.path.isdir(file_path):
            # Check if the .github/workflows folder exists in the repository
            workflows_path = os.path.join(file_path, '.github/workflows')
            if os.path.isdir(workflows_path):
                print(f"Reading from Repository with workflows: {repo_name}")
                try:
                    local_repo = Repo(file_path)
                    branch = local_repo.active_branch.name
                    commits = list(local_repo.iter_commits(branch))

                    for commit in commits:
                        commitFiles = get_file_name(commit.stats.files)
                        python_files = [file for file in commitFiles if file.endswith('.py')]
                        ml_related_files = [file for file in python_files if check_for_ml_keywords(file)]

                        if python_files and ml_related_files:
                            new_row = [commit.author, repo_name, commit.hexsha, commit.message, commitFiles]
                            writer.writerow(new_row)
                except Exception as e:
                    print(f"Error processing repository {repo_name}: {e}")
            else:
                print(f"Repository {repo_name} does not have a .github/workflows directory.")
        else:
            print(f"Directory for {repo_name} does not exist.")
