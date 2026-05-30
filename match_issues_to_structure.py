import pandas as pd

# Load issue markdown file
issues_df = pd.read_csv("characteristics_irts_markdown.csv")

# Load structured and unstructured repo lists
structured_repos = pd.read_csv("structured_repos.csv")
unstructured_repos = pd.read_csv("unstructured_repos.csv")

# Ensure consistent column naming
structured_repos.columns = structured_repos.columns.str.lower()
unstructured_repos.columns = unstructured_repos.columns.str.lower()
issues_df.columns = issues_df.columns.str.lower()

# Label each issue
issues_df['structured'] = issues_df['full_name'].isin(structured_repos['full_name'])

# Separate into two datasets
structured_issues = issues_df[issues_df['structured'] == True]
unstructured_issues = issues_df[issues_df['structured'] == False]

# Save for LLM input
structured_issues[['full_name', 'body_anonymized']].to_csv("structured_issues.csv", index=False)
unstructured_issues[['full_name', 'body_anonymized']].to_csv("unstructured_issues.csv", index=False)

print(" Matching complete. Saved:")
print(" - structured_issues.csv")
print(" - unstructured_issues.csv")
