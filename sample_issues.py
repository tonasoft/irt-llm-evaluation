import pandas as pd

# Load the full datasets
structured_df = pd.read_csv("structured_issues.csv")
unstructured_df = pd.read_csv("unstructured_issues.csv")

# Drop rows with empty or null issue text
structured_df = structured_df.dropna(subset=["body_anonymized"])
unstructured_df = unstructured_df.dropna(subset=["body_anonymized"])

# Randomly sample exactly 1,000 rows from each
sampled_structured = structured_df.sample(n=1000, random_state=42)
sampled_unstructured = unstructured_df.sample(n=1000, random_state=42)

# Save the sampled CSVs
sampled_structured.to_csv("structured_issues_sample.csv", index=False)
sampled_unstructured.to_csv("unstructured_issues_sample.csv", index=False)

print("✅ Sampling complete. Files saved as:")
print("   → structured_issues_sample.csv")
print("   → unstructured_issues_sample.csv")
