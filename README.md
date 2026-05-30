# Using LLMs to Evaluate the Impact of Structured Issue Templates on Open-Source Software Projects

> Obinna OkeKe, Sailesh Kafle, Sushant Nepal — Bowling Green State University

## Overview

This repository contains the code and data for a research study that uses GPT-4 as a surrogate maintainer to evaluate whether GitHub repositories that use structured **Issue Report Templates (IRTs)** produce higher-quality issue reports than those that do not.

We evaluated 1,000 structured and 1,000 unstructured issue reports across three quality dimensions:

| Metric | Structured | Unstructured |
|---|---|---|
| **Clarity Score** (1–5) | 3.57 | 1.43 |
| **Resolvability** (% Yes) | 49.3% | 3.5% |
| **Clarification Needed** (% Yes) | 6.2% | 96.6% |

Human validation confirmed GPT-4's reliability with F1 scores of up to 1.00 for unstructured issues.

---

## Research Question

> *Do repositories using structured issue templates resolve issues more effectively than those without?*

---

## Pipeline

```
characteristics_repo.csv (GIRT-DATA)
        │
        ▼
1. filter_active_repos.py          → structured_repos.csv, unstructured_repos.csv
        │
        ▼
2. match_filtered_issues.py        → structured_issues.csv, unstructured_issues.csv
        │
        ▼
3. sample_issues.py                → structured_issues_sample.csv, unstructured_issues_sample.csv
        │
        ├── 4a. evaluate_clarity_structured.py      → structured_issues_scored.csv
        ├── 4b. evaluate_clarity_unstructured.py    → unstructured_issues_scored.csv
        ├── 4c. evaluate_clarification_structured.py   → structured_clarification.csv
        ├── 4d. evaluate_clarification_unstructured.py → unstructured_clarification.csv
        ├── 4e. evaluate_resolvability_structured.py   → structured_resolvability.csv
        └── 4f. evaluate_resolvability_unstructured.py → unstructured_resolvability.csv
        │
        ▼
5. evaluate_f11_score.py           → Precision, Recall, F1 (GPT vs. human labels)
```

### Step-by-step

| Step | Script | Description |
|---|---|---|
| 1 | `filter_active_repos.py` | Filters GIRT-DATA repos: ≥100 closed issues, not archived. Splits into structured (`has_IRT=True`) and unstructured (`has_IRT=False`) lists. |
| 2 | `match_filtered_issues.py` | Joins filtered repo lists with issue bodies from `characteristics_irts_markdown.csv`. |
| 3 | `sample_issues.py` | Randomly samples 1,000 issues from each group (`random_state=42`). |
| 4a–4b | `evaluate_clarity_*.py` | GPT-4 rates each issue's clarity on a 1–5 scale. |
| 4c–4d | `evaluate_clarification_*.py` | GPT-4 judges whether a maintainer would need to ask for more information (Yes/No). |
| 4e–4f | `evaluate_resolvability_*.py` | GPT-4 judges whether an issue can be resolved as written (Yes/No). |
| 5 | `evaluate_f11_score.py` | Computes Precision, Recall, and F1 by comparing GPT outputs against human labels. |

---

## Dataset

This project uses [GIRT-DATA](https://github.com/kargaranamir/girt-data) — the GitHub Issue Report Template Dataset (MSR 2023). The three raw data files are **not included** in this repository due to their size. Download them from the [GIRT-DATA releases page](https://github.com/kargaranamir/girt-data/releases):

```bash
wget https://github.com/kargaranamir/girt-data/releases/download/msr23-v1.0/characteristics_repo.csv
wget https://github.com/kargaranamir/girt-data/releases/download/msr23-v1.0/characteristics_irts_markdown.csv
wget https://github.com/kargaranamir/girt-data/releases/download/msr23-v1.0/characteristics_irts_yaml.csv
```

Place them in the project root before running the pipeline.

### Processed data files (included)

| File | Description |
|---|---|
| `structured_repos.csv` | Filtered list of repos with IRTs |
| `unstructured_repos.csv` | Filtered list of repos without IRTs |
| `structured_issues.csv` | Issue bodies from structured repos |
| `unstructured_issues.csv` | Issue bodies from unstructured repos |
| `structured_issues_sample.csv` | 1,000 sampled structured issues |
| `unstructured_issues_sample.csv` | 1,000 sampled unstructured issues |
| `structured_issues_scored.csv` | GPT-4 clarity scores — structured |
| `unstructured_issues_scored.csv` | GPT-4 clarity scores — unstructured |
| `structured_clarification.csv` | GPT-4 clarification judgments — structured |
| `unstructured_clarification.csv` | GPT-4 clarification judgments — unstructured |
| `structured_resolvability.csv` | GPT-4 resolvability judgments — structured |
| `unstructured_resolvability.csv` | GPT-4 resolvability judgments — unstructured |
| `structured_clarification_Human_evaluation.csv` | Human labels — clarification, structured |
| `unstructured_clarification_Human_Evaluation.csv` | Human labels — clarification, unstructured |
| `structured_resolvability_Human_evalutaion.csv` | Human labels — resolvability, structured |
| `unstructured_resolvability_Human_evaluation.csv` | Human labels — resolvability, unstructured |

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/irt-llm-evaluation.git
cd irt-llm-evaluation
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your OpenAI API key

```bash
cp .env.example .env
# Edit .env and add your key:
# OPENAI_API_KEY=sk-...
```

Then load it before running scripts:

```bash
# Linux / macOS
export OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d '=' -f2)

# Windows PowerShell
$env:OPENAI_API_KEY = "sk-..."
```

### 4. Download raw data

Follow the [Dataset](#dataset) instructions above to place the three GIRT-DATA CSVs in the project root.

### 5. Run the pipeline

```bash
python filter_active_repos.py
python match_filtered_issues.py
python sample_issues.py

# Run all six evaluation scripts
python evaluate_clarity_structured.py
python evaluate_clarity_unstructured.py
python evaluate_clarification_structured.py
python evaluate_clarification_unstructured.py
python evaluate_resolvability_structured.py
python evaluate_resolvability_unstructured.py

# Compute F1 scores vs. human labels
python evaluate_f11_score.py
```

---

## GPT-4 Prompts

**Clarity Score (1–5)**
> *"You are a senior developer triaging GitHub issues. Please evaluate the following issue report and assign a clarity score from 1 to 5... Only respond with a number from 1 to 5."*

**Resolvability (Yes/No)**
> *"You are a GitHub project maintainer reviewing a newly submitted issue. Based on the issue description, determine if the issue is actionable as written, without needing additional information. Answer with only one word: Yes or No."*

**Clarification Needed (Yes/No)**
> *"You are a software maintainer reviewing GitHub issues. Would you need to ask the user for clarification or more information before you can resolve the issue described below? Please answer with only Yes or No."*

---

## Results

### Clarity Score
Structured issues scored significantly higher (mean = 3.57, SD = 1.89) vs. unstructured (mean = 1.43, SD = 1.20). A two-tailed independent t-test produced p < 0.00001.

### Resolvability
49.3% of structured issues were deemed resolvable vs. only 3.5% of unstructured issues — a 45.8 percentage point difference.

### Clarification Needed
Only 6.2% of structured issues required clarification vs. 96.6% of unstructured issues — a 90.4 percentage point difference.

### Human Validation (F1 Scores)

| Metric | Structured | Unstructured |
|---|---|---|
| Resolvability | 0.84 | 1.00 |
| Clarification Needed | 0.18 | 0.93 |

---

## Citation

If you use this work, please cite:

```bibtex
@article{okeke2025irt,
  title={Using LLMs to Evaluate the Impact of Structured Issue Templates on Open-Source Software Projects},
  author={OkeKe, Obinna and Kafle, Sailesh and Nepal, Sushant},
  institution={Bowling Green State University},
  year={2025}
}
```

This project builds on the GIRT-DATA dataset:

```bibtex
@inproceedings{nikeghbal2023girt,
  title={GIRT-Data: Sampling GitHub Issue Report Templates},
  author={Nikeghbal, Nafiseh and Kargaran, Amir Hossein and Heydarnoori, Abbas and Sch{\"u}tze, Hinrich},
  booktitle={2023 IEEE/ACM 20th International Conference on Mining Software Repositories (MSR)},
  pages={104--108},
  year={2023}
}
```

---

## License

This project is for academic research purposes.
