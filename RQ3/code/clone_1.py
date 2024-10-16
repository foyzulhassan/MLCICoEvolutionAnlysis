import csv
import os

# Paths for input and output
input_csv_path = '../../RQ3/data/repo_list_partial.csv'
clone_dir = 'C:\\Users\\dhiarzig\\Documents\\temp_repos'
output_csv_path = '..\\..\\RQ3\\data\\validated_clonedProjects.csv'

# Reading the repo list and preparing the local paths with validation
clonedProjects = []
header = ['RepoName', 'path', 'Exists']
#print current directory
print(os.getcwd())

with open(input_csv_path, 'r', newline='', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for line in csv_reader:
        # Replace forward slash in RepoName with dash for Windows file paths
        pathToRepo = os.path.join(clone_dir, line['RepoName'].replace('/', '\\'))
        
        # Check if the directory exists at the path
        exists = os.path.isdir(pathToRepo)
        
        # Append RepoName, path, and existence status to the list
        clonedProjects.append({"RepoName": line['RepoName'], "path": pathToRepo, "Exists": 'Yes' if exists else 'No'})

# Writing the validated local paths to the output CSV
with open(output_csv_path, 'w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=header)
    csv_writer.writeheader()
    csv_writer.writerows(clonedProjects)

print(f"Validated CSV with local paths saved to {output_csv_path}")
