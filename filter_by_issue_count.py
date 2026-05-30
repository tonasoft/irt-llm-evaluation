import pandas as pd

# Load structured and unstructured issue datasets
structured = pd.read_csv("structured_issues.csv")
unstructured = pd.read_csv("unstructured_issues.csv")

# Count number of issues per repository
structured_counts = structured['full_name'].value_counts()
unstructured_counts = unstructured['full_name'].value_counts()

# Filter repos with 100 to 150 issues
valid_structured_repos = structured_counts[(structured_counts >= 100) & (structured_counts <= 150)].index
valid_unstructured_repos = unstructured_counts[(unstructured_counts >= 100) & (unstructured_counts <= 150)].index

# Filter the issues
filtered_structured = structured[structured['full_name'].isin(valid_structured_repos)]
filtered_unstructured = unstructured[unstructured['full_name'].isin(valid_unstructured_repos)]

# Save the filtered data
filtered_structured.to_csv("structured_issues_filtered.csv", index=False)
filtered_unstructured.to_csv("unstructured_issues_filtered.csv", index=False)

print("Filtering complete.")
print(f"structured_issues_filtered.csv: {len(filtered_structured)} issues")
print(f"unstructured_issues_filtered.csv: {len(filtered_unstructured)} issues")
