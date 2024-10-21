import csv
from collections import Counter
import re
#read csv file in ../chris-analysis/Output/
with open("C:\\paper\\co_evolution_analysis\\RQ3\\data\\code_generated\\gha_output_statistical_analysis_expanded_keys_v3_test.csv", "r", encoding='utf-8') as f:
    reader = csv.reader(f)
    # Skip the header
    next(reader)
    print(next(reader))
    listOfCommands = list(reader)


lifecycleKeys = [
    'jobs', 'steps', 'run', 'env', 'name', 'on', 'uses',
    'with', 'if', 'timeout-minutes', 'permissions', 'secrets', 'strategy', 'matrix',
    'continue-on-error', 'working-directory', 'concurrency', 'outputs',
    'deploy', 'environment', 'cache', 'restore-keys', 'save-keys'
]

normalizedData=[]
for elem in listOfCommands:
    temp=[]
    key=elem[1]
    label=elem[2]

    #if the label starts with key then delete the key part from the label
    if(label.startswith(key+':')):
        label=label[len(key)+1:]
    #if the label starts with key: then delete the key part from the label
    if(len(label.split(' '))>1):
        command=label.split(' ',1)[0]
        params=label.split(' ',1)[1]
    else:
        command=label
        params=''

    #if command is python and param looks like x.y then normalize to python ver
    if((key.lower() == 'python' or key.lower() == 'python-version' or key.lower()=='python_version') and re.match(r'\d+\.\d+',command)):
        command='PYTHON-VERSION'
    normalizedData.append((elem[0],key,command,params,elem[4],elem[5]))


print("len of original data: "+str(len(listOfCommands)))
print("len of normalized data: "+str(len(normalizedData)))


#write result to most_frequent_env_map_changes.csv
with open('C:\\paper\\co_evolution_analysis\\RQ3\\data\\code_generated\\normalized_commands_v3.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # Optional: Add a header row if needed
    writer.writerow(['action', 'key', 'command', 'params', 'projectName', 'commitId'])
    writer.writerows(normalizedData)

print("len of original data: " + str(len(listOfCommands)))
print("len of normalized data: " + str(len(normalizedData)))