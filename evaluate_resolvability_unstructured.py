import os
import openai
import pandas as pd
import time

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Load unstructured issues
df = pd.read_csv("unstructured_issues_sample.csv")
df = df.dropna(subset=["body_anonymized"])

# Define the resolvability prompt
def is_resolvable(issue_text):
    prompt = f"""You are a GitHub project maintainer. Can you resolve the following issue report based on the information provided?

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

# Score each issue
resolvability = []
for i, row in df.iterrows():
    print(f"Scoring issue #{i+1}/{len(df)}")
    answer = is_resolvable(row["body_anonymized"])
    resolvability.append(answer)
    time.sleep(1.5)

# Save results
df["is_resolvable"] = resolvability
df.to_csv("unstructured_resolvability.csv", index=False)
print("✅ Resolvability scoring complete. Results saved to unstructured_resolvability.csv")
