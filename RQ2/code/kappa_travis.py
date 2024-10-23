# C:\\paper\\co_evolution_analysis\\RQ2\\data\\RQ2_coevolution_taxonomy_travis.xlsx"

import pandas as pd
from sklearn.metrics import cohen_kappa_score

# Load the provided Excel file
file_path = "C:\\paper\\co_evolution_analysis\\RQ2\\data\\RQ2_coevolution_taxonomy_travis.xlsx"
excel_data = pd.ExcelFile(file_path)

# Extract the relevant sheets: rater_1, rater_2, and categories
rater_1_df = excel_data.parse('rater_1')
rater_2_df = excel_data.parse('rater_2')
categories_df = excel_data.parse('categories')

# Extract the categories from the 'categories' sheet
categories = categories_df['Category'].tolist()

# Merge rater_1 and rater_2 based on 'GitAuthor' and 'CommitID'
merged_df = pd.merge(rater_1_df, rater_2_df, on=['GitAuthor', 'CommitID'], suffixes=('_rater_1', '_rater_2'))

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
output_path = "C:\\paper\\co_evolution_analysis\\RQ2\\data\\RQ2_coevolution_taxonomy_travis_kappa_scores.xlsx"
kappa_df.to_excel(output_path, index=False, sheet_name='kappa_scores')

print(f"Kappa scores and overall Kappa, along with differing commits and counts, saved to: {output_path}")
