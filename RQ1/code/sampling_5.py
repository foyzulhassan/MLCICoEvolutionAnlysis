import pandas as pd
import random

sample_size = 357

readDataframe = pd.read_csv('C:\\Users\\dhiarzig\\Documents\\VSCode Projects\\MLCICoEvolutionAnlysis\\RQ1\\data_backup\\filtered_ml_gha_commits.csv')

# Shuffle 
sampled_df = readDataframe.sample(frac=1, random_state=42).head(sample_size)  # frac=1 shuffles the whole DataFrame

# Print 
print("Randomly selected rows:")
print(sampled_df.head())  


sampled_df.to_csv("C:\\Users\\dhiarzig\\Documents\\VSCode Projects\\MLCICoEvolutionAnlysis\\RQ1\\data_backup\\ML_Sampled_GHA_Projects_2.csv", index=False)

df = pd.read_csv('C:\\Users\\dhiarzig\\Documents\\VSCode Projects\\MLCICoEvolutionAnlysis\\RQ1\\data_backup\\ML_Sampled_GHA_Projects_2.csv')
print("Number of rows in the CSV file:", len(df))