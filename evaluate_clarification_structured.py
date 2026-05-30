import os
import openai
import pandas as pd
import time

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Load the structured issues dataset
df = pd.read_csv("structured_issues_sample.csv")
df = df.dropna(subset=["body_anonymized"])

# Clarification scoring function using GPT-4
def needs_clarification(issue_text):
    prompt = f"""You are a GitHub project maintainer. Would you need to ask the user for more information before resolving this issue?

Please respond only with "Yes" or "No".

Issue:
\"\"\"\n{issue_text}\n\"\"\""""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0
        )
        reply = response.choices[0].message.content.strip().lower()
        if "yes" in reply:
            return "Yes"
        elif "no" in reply:
            return "No"
        else:
            return "Unknown"
    except Exception as e:
        print("Error:", e)
        return "Error"

# Apply clarification scoring
clarification_results = []
for i, row in df.iterrows():
    print(f"Scoring clarification needed for issue #{i+1}/{len(df)}")
    result = needs_clarification(row["body_anonymized"])
    clarification_results.append(result)
    time.sleep(1.5)

# Save results
df["clarification_needed"] = clarification_results
df.to_csv("structured_clarification.csv", index=False)
print("✅ Clarification scoring complete. Results saved to structured_clarification.csv")
