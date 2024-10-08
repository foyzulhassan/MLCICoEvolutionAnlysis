import pandas as pd
from git import Repo
import os

# Base path
clone_repo_path = 'C:\\paper\\empirical_analysis\\data\\repos'

# Read the CSV file 
dataframe = pd.read_csv('C:\\paper\\empirical_analysis\\data\\RQ1\\repo_list.csv')
reponame = dataframe['RepoName']
repoURL = dataframe['GitHubURL']

# df to list
export = dataframe.values.T[0].tolist()

# Loop 
for cell in range(len(export)):
    print("Row: ", cell)  
    print("Cloning Repository name:", reponame[cell])
    print("Cloning Repository URL:", repoURL[cell])

    # dest repo file path
    file_path = os.path.join(clone_repo_path, reponame[cell])
    is_created = os.path.isdir(file_path)

    if is_created:
        print("Already cloned", reponame[cell])
    else:
        try:
            # Clone 
            cloned_repo = Repo.clone_from(repoURL[cell], file_path)
            print("Done cloning", reponame[cell], "repository.")
        except Exception as e:
            print(f"Failed to clone {reponame[cell]}. Error: {str(e)}")

print("Cloned all repositories.")
