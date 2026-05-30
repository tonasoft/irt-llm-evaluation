import pandas as pd

# Load the top 500 repositories
top_repos = pd.read_csv("top_500_repositories.csv")
structured = top_repos[top_repos['has_irt'] == True]
unstructured = top_repos[top_repos['has_irt'] == False]

# Load the issue descriptions
issues = pd.read_csv("characteristics_irts_markdown.csv")
issues.columns = issues.columns.str.lower()

# Tag issues based on structured repos
issues['structured'] = issues['full_name'].isin(structured['full_name'])

# Filter out issues not part of the top 500 repos
issues_filtered = issues[issues['full_name'].isin(top_repos['full_name'])]

# Separate into structured and unstructured groups
structured_issues = issues_filtered[issues_filtered['structured'] == True]
unstructured_issues = issues_filtered[issues_filtered['structured'] == False]

# Save the result
structured_issues[['full_name', 'body_anonymized']].to_csv("structured_issues.csv", index=False)
unstructured_issues[['full_name', 'body_anonymized']].to_csv("unstructured_issues.csv", index=False)

print("Structured and unstructured issue files generated for the top 500 repositories.")
