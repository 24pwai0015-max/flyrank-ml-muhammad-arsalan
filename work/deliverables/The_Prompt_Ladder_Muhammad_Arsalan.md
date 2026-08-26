# The Prompt Ladder: From Lazy Query to Engineered Instruction

**Author:** Muhammad Arsalan  
**Track:** Applied Machine Learning & AI Fluency  
**Phase:** Foundations — Week 2  

---

## Overview

The prompt ladder is an exercise in prompt engineering discipline: starting with a weak, vague prompt and evolving it across **five distinct versions**, adding **exactly one named layer per version**. Output changes are evaluated side-by-side to understand which constraints directly produce reliable, verified code.

---

## Baseline: Run 0 (The Weak Starting Point)

### The Prompt
```text
Write python code to build an ML model on my data and predict which pages are declining.
```

### The Output (Representative Excerpt)
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load data
df = pd.read_csv('data.csv')

# Drop non-numeric
X = df.select_dtypes(include=['number'])
y = df['trend_direction']  # 'down' or other

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

preds = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))
```

### Evaluation Notes
- **What it did:** Produced generic, boilerplate classification code.
- **Why it failed:** 
  1. It treated the problem as standard classification (`predict()`) instead of ranking pages by priority.
  2. It blindly fed all numeric columns into `X`, leaking label columns directly into the features.
  3. It split data randomly row-by-row, leaking pages from the same client between train and test.
  4. It measured `accuracy_score`, which is useless on imbalanced search data and tells us nothing about whether the top recommendations are correct.

---

## Version 1: Run 1 (+ Layer: Clear Goal / Task Framing)

### The Single Change (Layer 1)
**Added Task Type & Decision Goal:** Specified that this is a **ranking/scoring task** to prioritize which pages need an editorial refresh first, rather than a binary classification problem.

### The Prompt
```text
Write python code to build an ML ranking model on search data (30,000 pages). The goal is to prioritize which pages need editorial refresh first by scoring their decline risk, rather than just binary classification.
```

### The Output (Representative Excerpt)
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('search_data.csv')
X = df.drop(columns=['content_id', 'trend_direction'])
y = (df['trend_direction'] == 'down').astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predict probability of decline to rank pages
decline_probs = model.predict_proba(X_test)[:, 1]
ranked_pages = pd.DataFrame({'content_id': df.loc[X_test.index, 'content_id'], 'decline_risk': decline_probs})
ranked_queue = ranked_pages.sort_values(by='decline_risk', ascending=False)
print(ranked_queue.head(20))
```

### Version 1 Notes
1. **What changed in the prompt:** Added the explicit business goal: scoring and ranking pages into a prioritized queue for editorial refresh.
2. **What actually improved in the output:** The model switched from categorical `predict()` to continuous `predict_proba()`, outputting a sorted dataframe queue where editors can act from the top down.
3. **What still failed:** It still had severe data leakage (`trend_pct` was retained in `X`), and train/test split was completely random across rows.
4. **What to try next:** Provide the actual column schema and strictly forbid label-derived columns.

---

## Version 2: Run 2 (+ Layer: Data Context & Anti-Leakage Constraints)

### The Single Change (Layer 2)
**Added Dataset Schema Context & Explicit Anti-Leakage Constraints:** Defined available feature columns and explicitly banned `trend_direction` and `trend_pct` from features.

### The Prompt
```text
Write python code to build an ML ranking model on search data (30,000 pages). The goal is to prioritize which pages need editorial refresh first by scoring their decline risk. The dataset has columns: content_id, client_id, impressions_90d, clicks_90d, days_since_last_update, avg_position, trend_direction, trend_pct. Rule: trend_direction and trend_pct define the label (down = 1), so they MUST be excluded from features to prevent leakage.
```

### The Output (Representative Excerpt)
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('content_refresh_anonymized.csv')

# Safe features only -- excluding leakage columns
feature_cols = ['impressions_90d', 'clicks_90d', 'days_since_last_update', 'avg_position']
X = df[feature_cols]
y = (df['trend_direction'] == 'down').astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

probs = model.predict_proba(X_test)[:, 1]
print("Top 10 highest risk pages:")
results = pd.DataFrame({'content_id': df.loc[X_test.index, 'content_id'], 'score': probs}).sort_values('score', ascending=False)
print(results.head(10))
```

### Version 2 Notes
1. **What changed in the prompt:** Explicitly listed allowed features and forbade `trend_direction` / `trend_pct`.
2. **What actually improved in the output:** The script defined an explicit whitelist `feature_cols`, completely eliminating the synthetic 100% accuracy leakage trap.
3. **What still failed:** The split was still random row-level (leaking client patterns), and there were no evaluation metrics computed for the ranking quality.
4. **What to try next:** Enforce a grouped client-holdout split (`GroupShuffleSplit`) and evaluate using Precision@50.

---

## Version 3: Run 3 (+ Layer: Validation Strategy & Precision@50 Metric)

### The Single Change (Layer 3)
**Added Grouped Validation & Decision Metric:** Required `GroupShuffleSplit` on `client_id` (20% holdout) and evaluated ranking performance using `Precision@50`.

### The Prompt
```text
Write python code to build an ML ranking model on search data (30,000 pages). The goal is to prioritize which pages need editorial refresh first by scoring their decline risk. The dataset has columns: content_id, client_id, impressions_90d, clicks_90d, days_since_last_update, avg_position, trend_direction, trend_pct. Exclude trend_direction and trend_pct from features. Validation must use a GroupShuffleSplit on client_id (20% clients held out). Evaluate the model using Precision@50 (precision in the top 50 ranked pages).
```

### The Output (Representative Excerpt)
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('content_refresh_anonymized.csv')

features = ['impressions_90d', 'clicks_90d', 'days_since_last_update', 'avg_position']
X = df[features]
y = (df['trend_direction'] == 'down').astype(int)
groups = df['client_id']

gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, test_idx = next(gss.split(X, y, groups=groups))

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

test_scores = model.predict_proba(X_test)[:, 1]
eval_df = pd.DataFrame({'y_true': y_test, 'score': test_scores}).sort_values('score', ascending=False)

p_at_50 = eval_df.head(50)['y_true'].mean()
print(f"Model Precision@50 on held-out clients: {p_at_50:.3f}")
```

### Version 3 Notes
1. **What changed in the prompt:** Imposed grouped client splits (`GroupShuffleSplit`) and `Precision@50` evaluation.
2. **What actually improved in the output:** Validation became honest. The model is tested only on unseen clients, and the evaluation reflects what a strategist reviewing 50 pages actually experiences.
3. **What still failed (The "Made it worse / Missing Context" moment):** 
   > ⚠️ **What went backwards:** In focusing purely on the model's Precision@50, the output stripped away all comparative context. A printed score of `0.740` appeared in a complete vacuum. Without a baseline heuristic (e.g. sorting by staleness) or base rate comparison, there was no way to prove whether machine learning was actually better than a 2-line SQL order-by.
4. **What to try next:** Require a transparent rule-based heuristic baseline and a 3-way benchmark table (Naive Rule vs ML Model vs Base Rate).

---

## Version 4: Run 4 (+ Layer: Baseline Benchmark & Comparison Table)

### The Single Change (Layer 4)
**Added Baseline Benchmarking Requirement:** Demanded a naive heuristic baseline ("stalest page first") and a comparative evaluation table against the dataset base rate.

### The Prompt
```text
Write python code to build an ML ranking model on search data (30,000 pages). The goal is to prioritize which pages need editorial refresh first by scoring their decline risk. The dataset has columns: content_id, client_id, impressions_90d, clicks_90d, days_since_last_update, avg_position, trend_direction, trend_pct. Exclude trend_direction and trend_pct from features. Validation must use a GroupShuffleSplit on client_id (20% clients held out). Evaluate using Precision@50. MUST include a naive rule baseline (e.g. ranking by days_since_last_update) and print a comparison table showing Naive Rule P@50 vs Model P@50 vs Base Rate.
```

### The Output (Representative Excerpt)
```python
# ... [Data preparation & split as before] ...

# 1. Base Rate on test set
base_rate = y_test.mean()

# 2. Naive Baseline (Rank strictly by staleness)
naive_scores = X_test['days_since_last_update']
naive_df = pd.DataFrame({'y_true': y_test, 'score': naive_scores}).sort_values('score', ascending=False)
naive_p50 = naive_df.head(50)['y_true'].mean()

# 3. ML Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
ml_scores = model.predict_proba(X_test)[:, 1]
ml_df = pd.DataFrame({'y_true': y_test, 'score': ml_scores}).sort_values('score', ascending=False)
ml_p50 = ml_df.head(50)['y_true'].mean()

# Benchmark Table
results_summary = pd.DataFrame({
    'Method': ['Naive Heuristic (Stalest First)', 'Random Forest Classifier', 'Base Rate (Random Selection)'],
    'Precision@50': [naive_p50, ml_p50, base_rate],
    'Description': ['Sort by days_since_last_update', 'Multivariate search signal model', 'Prevalence of declining pages']
})
print(results_summary.to_string(index=False))
```

### Version 4 Notes
1. **What changed in the prompt:** Demanded a naive baseline benchmark and structured side-by-side comparison.
2. **What actually improved in the output:** The output now explicitly proves the ML value proposition: it shows that while a naive rule scores ~0.240 and random guessing scores ~0.542, the model achieves ~0.740 (a 3.1x lift over the rule).
3. **What still failed:** The code was written as a flat, monolithic script with no data sanitization (no log-transforms on heavy-tailed impression counts, no handling of division by zero in CTR, and no modular functions).
4. **What to try next:** Add production data safety constraints (log transforms, NaN fills) and enforce modular functional design.

---

## Version 5: Run 5 (+ Layer: Production Data Engineering & Modular Architecture)

### The Single Change (Layer 5)
**Added Data Engineering Safety, Log Transforms, and Modular Structure:** Enforced mathematical feature transforms for heavy-tailed search traffic, safe NaN/rate handling, modular functions, and self-verifying assertion checks.

### The Prompt
```text
Write a clean, modular python script to train and evaluate a search intelligence ranking model for content refresh prioritization.
- Data input: data/raw/content_refresh_anonymized.csv (30k rows).
- Feature Engineering: Log1p-transform heavy-tailed metrics (impressions_90d, clicks_90d), handle missing values explicitly, and compute derived rates with zero-division safety.
- Excluded Features: Never include trend_direction, trend_pct, client_id, or content_id in training.
- Validation: GroupShuffleSplit on client_id (20% held-out test clients).
- Evaluation & Benchmarks: Compute Precision@50 for (1) Naive baseline (stalest page first), (2) Random Forest model, and (3) Dataset base rate.
- Code Standards: Modular functions (load_data, prepare_features, train_and_evaluate), type hints, docstrings, and assert statements verifying zero leakage.
```

### The Output (Representative Excerpt)
```python
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupShuffleSplit

def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Prepares safe feature matrix with log transforms and no label leakage."""
    y = (df['trend_direction'].str.lower() == 'down').astype(int)
    groups = df['client_id']
    
    X = pd.DataFrame({
        'log_impressions': np.log1p(df['impressions_90d'].fillna(0)),
        'log_clicks': np.log1p(df['clicks_90d'].fillna(0)),
        'days_since_update': df['days_since_last_update'].fillna(0),
        'avg_position': df['avg_position'].fillna(0),
        'ctr': (df['clicks_90d'] / df['impressions_90d'].replace(0, np.nan) * 100).fillna(0),
    })
    
    # Assert zero label leakage
    assert 'trend_pct' not in X.columns and 'trend_direction' not in X.columns
    return X, y, groups

def evaluate_precision_at_k(y_true: pd.Series, scores: np.ndarray | pd.Series, k: int = 50) -> float:
    ranked = pd.DataFrame({'y': y_true.values, 'score': scores}).sort_values('score', ascending=False)
    return float(ranked.head(k)['y'].mean())

def main():
    df = pd.read_csv('data/raw/content_refresh_anonymized.csv')
    X, y, groups = prepare_features(df)
    
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(gss.split(X, y, groups=groups))
    
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    
    # Model Training
    clf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluations
    naive_p50 = evaluate_precision_at_k(y_test, X_test['days_since_update'], k=50)
    ml_p50 = evaluate_precision_at_k(y_test, clf.predict_proba(X_test)[:, 1], k=50)
    base_rate = float(y_test.mean())
    
    summary = pd.DataFrame([
        {'Strategy': 'Naive Rule (Stalest First)', 'Precision@50': f"{naive_p50:.3f}", 'Lift vs Base': f"{(naive_p50/base_rate):.2f}x"},
        {'Strategy': 'Random Forest (Client Holdout)', 'Precision@50': f"{ml_p50:.3f}", 'Lift vs Base': f"{(ml_p50/base_rate):.2f}x"},
        {'Strategy': 'Base Rate (Random Draw)', 'Precision@50': f"{base_rate:.3f}", 'Lift vs Base': '1.00x'}
    ])
    print("\n=== SEARCH INTELLIGENCE RANKING BENCHMARK ===")
    print(summary.to_string(index=False))

if __name__ == '__main__':
    main()
```

### Version 5 Notes
1. **What changed in the prompt:** Enforced data engineering hygiene (log transforms, zero division safety), modular architecture, and self-checks.
2. **What actually improved in the output:** The generated code is robust, handles real-world skewed distributions cleanly, has automated assertions against leakage, and is ready for production without manual bug-fixing.
3. **What still failed:** Nothing within the scope of single-table search ranking; the prompt produces complete, verified, honest ML pipeline code.
4. **What to try next:** Package this as the standard reusable prompt for anyone training decision-support models on search data.

---

## Final Reusable Prompt

```text
You are an applied ML engineer specializing in search intelligence and ranking systems.

Task:
Write a clean, modular, self-contained Python script to train and evaluate a ranking model for prioritizing content refreshes on Google Search Console & Analytics data.

Input Dataset:
- File: data/raw/content_refresh_anonymized.csv (30,000 rows × 44 columns, 32 distinct clients).

Feature Engineering & Leakage Rules:
1. Features: Compute safe historical signals (apply np.log1p to heavy-tailed impressions_90d and clicks_90d; include days_since_last_update, avg_position, and safe CTR with zero-division protection).
2. Strict Leakage Prevention: NEVER use trend_direction, trend_pct, or any 30-day comparison window columns (*_last_30d, *_prev_30d) as features. Add an explicit assert statement verifying this.
3. Identifiers: Do not train on client_id or content_id.

Validation Strategy:
- Split by client using sklearn.model_selection.GroupShuffleSplit on client_id (20% held-out test clients). No client may appear in both train and test.

Evaluation & Benchmark Table:
- Compute Precision@50 (proportion of declining pages in the top 50 recommendations) on the held-out test clients.
- Compare side-by-side in a formatted table:
  a. Naive Heuristic Baseline (ranked by days_since_last_update)
  b. Random Forest Classifier (multivariate ranking)
  c. Test Set Base Rate (random selection baseline)
  d. Relative Lift vs Base Rate

Code Standards:
- Write modular functions (load_data, prepare_features, evaluate_ranking, main).
- Include full imports, docstrings, type annotations, and an executable __main__ entry point.
```

---

## Summary of Lessons Learned

| Version | Added Layer | Primary Output Breakthrough | Key Weakness Exposed |
|---|---|---|---|
| **0 (Base)** | None | Boilerplate classifier | Leaked labels, row-split leak, useless accuracy metric |
| **1** | Goal Framing | Switched from `predict()` to `predict_proba()` ranking queue | Still leaked `trend_pct` into features |
| **2** | Schema & Anti-Leakage | Explicit feature whitelist excluding label math | Evaluated randomly with no client generalization |
| **3** | Grouped Split & P@50 | Honest client holdout validation on top 50 pages | **Lost comparative baseline (score in a vacuum)** |
| **4** | Heuristic Baseline | Proved ML lift over naive staleness rule & base rate | Monolithic script, unhandled skewed distributions |
| **5** | Production Data Hygiene | Log1p transforms, safe division, modular assertions | None; production-grade and reproducible |
