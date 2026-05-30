from sklearn.metrics import precision_score, recall_score, f1_score

# Sample labels (1 = Yes, 0 = No)
# Replace these with your actual labels from GPT and human annotations

# 👤 Human labels (ground truth)
# Example clarification labels
human_labels_clarification = [1, 1, 0, 1, 0, 1, 0, 1, 1, 1,
                              1, 1, 0, 1, 1, 1, 0, 1, 1, 1,
                              1, 1, 0, 1, 1]

gpt_labels_clarification =   [1, 1, 0, 1, 1, 1, 0, 1, 1, 1,
                              1, 1, 0, 1, 1, 1, 0, 1, 1, 1,
                              1, 1, 0, 1, 1]

precision = precision_score(human_labels_clarification, gpt_labels_clarification)
recall = recall_score(human_labels_clarification, gpt_labels_clarification)
f1 = f1_score(human_labels_clarification, gpt_labels_clarification)

print("\n Clarification Needed Evaluation:")
print("Precision:", round(precision, 2))
print("Recall:", round(recall, 2))
print("F1 Score:", round(f1, 2))
