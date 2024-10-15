import requests
import pandas as pd
import os
import time


github_token = '' #Add your GitHub token here
headers = {'Authorization': f'token {github_token}'}

def get_pr_details(commit_sha, repo):
    """Fetch PR details for a given commit in a repository."""
    pr_details = {'isPR': False, 'PRTitle': None, 'PRDescription': None, 'Status': 'Success'}
    pr_search_url = f"https://api.github.com/search/issues?q=repo:{repo}+sha:{commit_sha}"
    response = requests.get(pr_search_url, headers=headers)
    
    print(f"Requesting {pr_search_url}") 
    if response.status_code == 200:
        search_results = response.json()
        print(f"Received {len(search_results['items'])} items")  
        if search_results['total_count'] > 0:
            pr = search_results['items'][0] 
            pr_details.update({
                'isPR': True,
                'PRTitle': pr['title'],
                'PRDescription': pr['body']
            })
            print(f"PR Found: Title - {pr['title']}") 
        else:
            print("No PRs found for this commit.")
    elif response.status_code == 403 and 'rate limit' in response.text.lower():
        rate_limit_reset = int(response.headers['X-RateLimit-Reset'])
        time_to_sleep = rate_limit_reset - time.time()
        print(f"Rate limit exceeded, waiting {abs(time_to_sleep)+5} seconds...")
        pr_details['Status'] = 'Rate Limit Exceeded'  
        # sleep until rate limit reset
        # rate_limit_reset = int(response.headers['X-RateLimit-Reset'])
        time.sleep(abs(time_to_sleep)+5)
        # time.sleep(5)
        return get_pr_details(commit_sha, repo) 
    else:
        print(f"Failed to fetch data: Status code {response.status_code}")  
        pr_details['Status'] = f'Failed: {response.status_code}'
    return pr_details


file_path = 'C:\\Users\\dhiarzig\\Documents\\VSCode Projects\\MLCICoEvolutionAnlysis\\RQ1\\data_backup\\ML_Sampled_GHA_Projects_2.csv'
df = pd.read_csv(file_path, encoding='utf-8')
print(df.columns)

df['isPR'] = False
df['PRTitle'] = None
df['PRDescription'] = None
df['Status'] = 'Pending'

# i = 0
for index, row in df.iterrows():
    # i+=1
    # if i > 5:
        # break
    repo = row['projectname']
    commit_sha = row['commitid']
    print(f"Processing repo: {repo}, commit SHA: {commit_sha}") 
    pr_details = get_pr_details(commit_sha, repo)
    for key, value in pr_details.items():
        df.at[index, key] = value

df.to_csv('C:\\Users\\dhiarzig\\Documents\\VSCode Projects\\MLCICoEvolutionAnlysis\\RQ1\\data_backup\\ML_Sampled_GHA_Projects_2_PR_details.csv', index=False)
print("Updated DataFrame saved.")  
