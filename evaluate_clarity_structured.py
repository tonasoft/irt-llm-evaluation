import os
import openai
import pandas as pd
import time

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Load the dataset for structured issues
df = pd.read_csv("structured_issues_sample.csv")
df = df.dropna(subset=["body_anonymized"])

# GPT clarity scoring function using GPT-4
def get_clarity_score(issue_text):
    prompt = f"""Rate the clarity of the following GitHub issue on a scale from 1 to 5 (where 5 is very clear and 1 is very unclear). Only return the number.

Issue:
\"\"\"\n{issue_text}\n\"\"\"
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0
        )
        score = response.choices[0].message.content.strip()
        return int(score) if score.isdigit() else None
    except Exception as e:
        print("Error:", e)
        return None

# Iterate through each issue and apply GPT-4 scoring
scores = []
for i, row in df.iterrows():
    print(f"Scoring issue #{i+1}/{len(df)}")
    score = get_clarity_score(row["body_anonymized"])
    scores.append(score)
    time.sleep(1.5)  # Respect OpenAI rate limits

# Add scores and save results
df["clarity_score"] = scores
df.to_csv("structured_issues_scored.csv", index=False)
print("✅ GPT clarity scoring complete for structured issues. Results saved to structured_issues_scored.csv")
