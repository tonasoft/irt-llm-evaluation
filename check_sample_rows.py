import pandas as pd

# Load the sampled files
structured = pd.read_csv("structured_issues_sample.csv")
unstructured = pd.read_csv("unstructured_issues_sample.csv")

print("✅ Structured rows:", len(structured))
print("✅ Unstructured rows:", len(unstructured))
