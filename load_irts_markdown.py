import pandas as pd

# Load the issue report markdown data
file_path = "characteristics_irts_markdown.csv"
df = pd.read_csv(file_path)

# Display all column names
print("Column names:\n", df.columns)

# Show the first 5 rows
print("\nSample rows:\n", df.head())
