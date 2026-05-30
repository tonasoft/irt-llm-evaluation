import pandas as pd

# Load the GIRT-DATA repo characteristics
df = pd.read_csv("characteristics_repo.csv")

# Filter for active repos (not archived) with at least 100 closed issues
filtered_df = df[
    (df['closed_issues_countv2'] >= 100) &
    (df['is_archive'] == False)
]

# Filter structured and unstructured groups
structured_repos = filtered_df[filtered_df['has_IRT'] == True]
unstructured_repos = filtered_df[filtered_df['has_IRT'] == False]

# Save clean lists for further use
structured_repos[['full_name']].to_csv("structured_repos.csv", index=False)
unstructured_repos[['full_name']].to_csv("unstructured_repos.csv", index=False)

print("Filtered structured and unstructured repo lists saved.")
