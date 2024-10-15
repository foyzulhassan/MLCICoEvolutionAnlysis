import csv
from datetime import datetime
from git import Repo
import os

clonePath='/home/alaa/Research/Thesis/Alexis-dataset/clonedRepos/'
def find_oldest_and_earliest_commits(csv_file):
    oldest_commits = {}
    earliest_commits = {}
    minDate=datetime.today()
    minDate=minDate.replace(tzinfo=None)
    maxDate=datetime(1970,1,1)
    maxDate=maxDate.replace(tzinfo=None)
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            project_path = row['ProjectName']
            project_path=clonePath+project_path.replace("/","-")
            print(project_path)
            if(not os.path.exists(project_path)):
                continue
            commit_hash = row['CommitID']
            try:
                commit_date = get_commit_date(project_path, commit_hash)

                commit_date=commit_date.replace(tzinfo=None)
                if(commit_date<minDate):
                    minDate=commit_date
                if(commit_date>maxDate):
                    maxDate=commit_date
            except:
                continue

    return minDate, maxDate

def get_commit_date(project_path, commit_hash):
    repo=Repo(project_path)
    com=repo.commit(commit_hash)
    return com.committed_datetime

# Example usage:
csv_file = '/home/alaa/Research/Thesis/Alexis-dataset/ML-CommitsFrom-PythonProjects - ML-CommitsFrom-PythonProjects-filtered-from-deleted-projects.csv'
minDate, maxDate = find_oldest_and_earliest_commits(csv_file)

print("Oldest commits:"+minDate.strftime("%m/%d/%Y"))
print("elriest commit:"+maxDate.strftime("%m/%d/%Y"))
