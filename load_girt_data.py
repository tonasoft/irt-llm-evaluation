import pandas as pd

# Load the dataset
df = pd.read_csv("characteristics_repo.csv")

# Filter for active repos (not archived) with at least 100 resolved issues
filtered_df = df[
    (df['closed_issues_countv2'] >= 100) &
    (df['is_archive'] == False)
]

# Split into structured and unstructured repos
structured_repos = filtered_df[filtered_df['has_IRT'] == True]
unstructured_repos = filtered_df[filtered_df['has_IRT'] == False]

# Save for downstream LLM use
structured_repos[['full_name']].to_csv("structured_repos.csv", index=False)
unstructured_repos[['full_name']].to_csv("unstructured_repos.csv", index=False)

print("Filtered structured and unstructured repo lists saved.")
