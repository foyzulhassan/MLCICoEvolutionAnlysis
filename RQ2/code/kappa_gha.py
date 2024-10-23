# C:\\paper\\co_evolution_analysis\\RQ2\\data\\RQ2_coevolution_taxonomy_travis.xlsx"

import pandas as pd
from sklearn.metrics import cohen_kappa_score

from sklearn.metrics import multilabel_confusion_matrix
import numpy as np

# Load the provided Excel file
file_path = "..\\data\\RQ2_coevolution_taxonomy_gha_reformatted.xlsx"
excel_data = pd.ExcelFile(file_path)

# Extract the relevant sheets: rater_1, rater_2, and categories
rater_1_df = excel_data.parse('rater_1')
rater_2_df = excel_data.parse('rater_2')
categories_df = excel_data.parse('categories')

# Extract the categories from the 'categories' sheet
categories = categories_df['Category'].tolist()

# Merge rater_1 and rater_2 based on 'GitAuthor' and 'CommitID'
merged_df = pd.merge(rater_1_df, rater_2_df, on=['GitAuthor', 'CommitID'], suffixes=('_rater_1', '_rater_2'))
rater_1_list = merged_df['Categories_rater_1'].tolist()
rater_2_list = merged_df['Categories_rater_2'].tolist()

#convert all values of lists to string
rater_1_list = [str(x) for x in rater_1_list]
rater_2_list = [str(x) for x in rater_2_list]

#Binarize labels
rater1_bin = [[int(label in labels) for label in categories] for labels in rater_1_list]
rater2_bin = [[int(label in labels) for label in categories] for labels in rater_2_list]

# Generate multilabel confusion matrices
conf_matrices = multilabel_confusion_matrix(rater1_bin, rater2_bin)

# Function to calculate Cohen's kappa from confusion matrix
def kappa_from_conf_matrix(cm):
    total = np.sum(cm)
    po = np.trace(cm) / total
    pe = np.sum(np.sum(cm, axis=0) * np.sum(cm, axis=1)) / (total ** 2)
    return (po - pe) / (1 - pe)

# Calculate kappa for each label
kappa_scores = []
for cm in conf_matrices:
    kappa = kappa_from_conf_matrix(cm)
    kappa_scores.append(kappa)

# Average kappa score
avg_kappa = np.mean(kappa_scores)
print("Average Kappa score:", avg_kappa)

exit(0)


# Function to check if a category is present in a rater's category list
def check_category_presence(categories_column, category):
    return categories_column.apply(lambda x: category in x if isinstance(x, str) else False)



# Create new columns for each category based on presence in the 'Categories_rater_1' and 'Categories_rater_2'
for category in categories:
    merged_df[f"{category}_rater_1"] = check_category_presence(merged_df['Categories_rater_1'], category)
    merged_df[f"{category}_rater_2"] = check_category_presence(merged_df['Categories_rater_2'], category)

# Calculate Cohen's Kappa score for each category and store in a dictionary, along with differing commits
kappa_scores = {}
difference_details = []

for category in categories:
    col_rater_1 = f"{category}_rater_1"
    col_rater_2 = f"{category}_rater_2"
    
    # Calculate Cohen's Kappa score
    kappa_score = cohen_kappa_score(merged_df[col_rater_1], merged_df[col_rater_2])
    kappa_scores[f"{category}_kappa"] = kappa_score
    
    # Find commit rows with differences and count them
    differences = merged_df[merged_df[col_rater_1] != merged_df[col_rater_2]]['CommitID'].tolist()
    difference_count = len(differences)
    
    # Store details for each category
    difference_details.append({
        'Category': category, 
        'Kappa Score': kappa_score, 
        'Differing Commits': differences,
        'Difference Count': difference_count
    })

# Convert kappa scores and differences to a DataFrame and add an overall average Kappa score
kappa_df = pd.DataFrame(difference_details)
kappa_df.loc['average'] = ['Overall Kappa', kappa_df['Kappa Score'].mean(), 'N/A', kappa_df['Difference Count'].sum()]

# Save the Kappa scores and differences to a new Excel file
output_path = "..\\data\\RQ2_coevolution_taxonomy_gha_kappa_scores.xlsx"
kappa_df.to_excel(output_path, index=False, sheet_name='kappa_scores')

print(f"Kappa scores and overall Kappa, along with differing commits and counts, saved to: {output_path}")
