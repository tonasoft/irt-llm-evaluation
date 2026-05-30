import os
import openai
import pandas as pd
import time

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Load unstructured issues file
df = pd.read_csv("unstructured_issues_sample.csv")
df = df.dropna(subset=["body_anonymized"])  # Drop rows without issue text

# Function to generate clarity score using GPT
def get_clarity_score(issue_text):
    prompt = f"""Rate the clarity of the following GitHub issue on a scale from 1 to 5 (where 5 is very clear and 1 is very unclear). Only return the number.\n\nIssue:\n\"\"\"\n{issue_text}\n\"\"\""""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0
        )
        score = response.choices[0].message.content.strip()
        return int(score) if score.isdigit() else None
    except Exception as e:
        print("Error:", e)
        return None

# Score all issues with GPT
scores = []
for i, row in df.iterrows():
    print(f"Scoring issue #{i+1}/{len(df)}")
    score = get_clarity_score(row["body_anonymized"])
    scores.append(score)
    time.sleep(1.5)  # Respect API rate limits

# Save the results
df["clarity_score"] = scores
df.to_csv("unstructured_issues_scored.csv", index=False)
print("✅ GPT scoring complete for unstructured issues.")
