import pandas as pd

# Load filtered repo lists
structured_repos = pd.read_csv("structured_repos.csv")
unstructured_repos = pd.read_csv("unstructured_repos.csv")

# Load the full issue dataset (markdown descriptions)
issues_df = pd.read_csv("characteristics_irts_markdown.csv")

# Normalize column names
structured_repos.columns = structured_repos.columns.str.lower()
unstructured_repos.columns = unstructured_repos.columns.str.lower()
issues_df.columns = issues_df.columns.str.lower()

# Match issues by repo full_name
issues_df['structured'] = issues_df['full_name'].isin(structured_repos['full_name'])

# Split the issues into two groups
structured_issues = issues_df[issues_df['structured'] == True]
unstructured_issues = issues_df[issues_df['structured'] == False]

# Save updated issue files
structured_issues[['full_name', 'body_anonymized']].to_csv("structured_issues.csv", index=False)
unstructured_issues[['full_name', 'body_anonymized']].to_csv("unstructured_issues.csv", index=False)

print("   Updated issue lists saved:")
print(" - structured_issues.csv")
print(" - unstructured_issues.csv")
