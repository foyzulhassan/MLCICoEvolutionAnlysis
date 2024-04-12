import pandas as pd
from git import Repo
import os
#This is the repo that will contain all of our cloned repos
clonegetpy = Repo('C:\\projects\\Prof.Hassan_Foyzul_Research_Work\\Analysis\\CloneWithGetPy')
clone_repo_path = 'C:\\projects\\Prof.Hassan_Foyzul_Research_Work\\ClonedRepos'

#The file path is hard coded, but it could be done dynamically by using os
dataframe = pd.read_csv('C:\\projects\\Prof.Hassan_Foyzul_Research_Work\\Analysis\\primary_ds_csv_v1.csv')
reponame = dataframe['RepoName']
repoURL = dataframe['GitHubURL']

export = dataframe.values.T[0].tolist()
for cell in range(len(export)): #add in len(export) when ready to pull all
    #need to add in try/catch so if a repo fails, add that cell to a dni list
    if cell == 190 or cell == 210 or cell == 391 or cell == 417:
        print("Repository", reponame[cell], "has a long file path or doesn't exist.")
        continue
    print("Row: ", cell) #displayed this to make sure all rows were read properly
    print("Cloning Repository name:", reponame[cell])
    print( "Cloning Repository URL:", repoURL[cell])
    file_path = os.path.join(clone_repo_path, reponame[cell])
    is_created = os.path.isdir(file_path)
    if(is_created):
        print("Already cloned", reponame[cell])
    else:
        cloned_repo = Repo.clone_from(repoURL[cell], file_path)
        print("Done cloning", reponame[cell], "repository.")
print("Cloned all repositories.")