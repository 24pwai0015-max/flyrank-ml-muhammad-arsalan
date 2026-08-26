# FL-02: Prompting Fundamentals on Real Tasks v2

**Author:** Muhammad Arsalan  
**Track:** General AI Fluency (Foundations)  
**Task Code:** FL-02  
**Target Task Selected from FL-01 Audit:** Task #8 (*Cleaning and exploring datasets*) & Task #3 (*Debugging code & auditing pipelines for data leakage*)  

---

## 1. Selected Task Context from FL-01 Audit

In my **FL-01 AI Workflow Audit**, I identified *Cleaning and Exploring Datasets* and *Debugging Code Errors & Pipeline Auditing* as core collaborative workflows. When working on tabular ML datasets (such as the 30,000-page FlyRank search dataset), a naive prompt yields generic Pandas code that overlooks subtle **data leakage** (e.g., including columns mathematically derived from the target) and fails to catch systematic missingness.

This assignment documents the step-by-step engineering of a prompt to audit an ML dataset schema for target leakage, classify features into a strict data contract, and generate executable validation code.

---

## 2. The Six Iterations (Naive Baseline + 5 Named Techniques)

---

### Iteration 0: Naive Baseline (No Engineering)

#### The Prompt
```text
Analyze this search dataset for errors and data leakage, and tell me what features to use to predict declining pages.
Dataset columns: content_id, client_id, search_volume, competition, word_count, impressions_90d, clicks_90d, impressions_last_30d, impressions_prev_30d, avg_position, trend_direction, trend_pct.
```

#### Output (Representative Excerpt)
```text
Here is an analysis of your dataset:

1. Target Variable: You can use `trend_direction` or `trend_pct` as your target.
2. Features to use:
   - `search_volume`, `competition`, `word_count` (content context)
   - `impressions_90d`, `clicks_90d` (traffic totals)
   - `impressions_last_30d`, `impressions_prev_30d` (recent momentum)
   - `trend_pct` (percentage change in traffic)
   - `avg_position` (ranking score)
3. Data Leakage Warning: Make sure not to use `trend_direction` if you are predicting `trend_direction`.
4. Code:
   ```python
   df = pd.read_csv('data.csv')
   X = df[['search_volume', 'competition', 'word_count', 'impressions_90d', 'clicks_90d', 'impressions_last_30d', 'impressions_prev_30d', 'trend_pct', 'avg_position']]
   y = df['trend_direction']
   ```
```

#### Notes on Iteration 0
- **What changed in the prompt:** Baseline naive prompt (1 sentence, no constraints, no role, no structure).
- **What actually happened in the output:** The AI gave dangerously flawed advice: it explicitly recommended including `impressions_last_30d`, `impressions_prev_30d`, and `trend_pct` as features to predict declining pages. Because `trend_direction` is directly calculated from those exact columns, this produces $100\%$ artificial accuracy via direct mathematical leakage.
- **What failed:** Complete blindness to mathematical proxy leakage; generic text formatting; no validation logic.
- **What to try next:** Apply **Role Assignment** to establish domain expertise in ML audit and data integrity.

---

### Iteration 1: + Named Technique 1 (Role Assignment)

#### The Prompt
```text
You are a Principal Machine Learning Engineer and Senior Data Integrity Auditor specializing in tabular ranking systems and search console analytics. Your primary obsession is preventing target leakage, detecting proxy variables, and ensuring honest offline validation.

Analyze this search dataset for errors and data leakage, and tell me what features to use to predict declining pages.
Dataset columns: content_id, client_id, search_volume, competition, word_count, impressions_90d, clicks_90d, impressions_last_30d, impressions_prev_30d, avg_position, trend_direction, trend_pct.
```

#### Output (Representative Excerpt)
```text
As a Data Integrity Auditor, I must flag critical leakage risks in your proposed setup:

1. CRITICAL LEAKAGE DETECTED:
   - `trend_pct` is derived directly from `(impressions_last_30d - impressions_prev_30d) / impressions_prev_30d`.
   - If your target is `trend_direction == 'down'`, using `trend_pct`, `impressions_last_30d`, or `impressions_prev_30d` as features represents catastrophic target leakage. A decision tree will simply split on `trend_pct < -0.20` and achieve 1.00 ROC-AUC without learning any real-world signal.

2. Safe Feature Whitelist:
   - `search_volume`, `competition`, `word_count`
   - `impressions_90d`, `clicks_90d`, `avg_position`

3. Recommended Next Step: Remove all 30-day comparison columns from the feature matrix `X`.
```

#### Notes on Iteration 1
- **What changed in the prompt:** Assigned the specific role of a *Principal ML Engineer & Senior Data Integrity Auditor obsessed with preventing target leakage*.
- **What actually improved in the output:** The tone shifted from agreeable assistant to strict code reviewer. It immediately identified `trend_pct` and the 30-day window columns as catastrophic leakage, correctly explaining that a decision tree would trivially memorize the $-20\%$ threshold.
- **What still failed:** The output remained high-level prose with no operational data contract, no handling of client grouping, and no structured schema.
- **What to try next:** Add **Context and Motivation** explaining the business decision and validation constraints.

---

### Iteration 2: + Named Technique 2 (Context and Motivation)

#### The Prompt
```text
You are a Principal Machine Learning Engineer and Senior Data Integrity Auditor specializing in tabular ranking systems and search console analytics. Your primary obsession is preventing target leakage, detecting proxy variables, and ensuring honest offline validation.

Context & Business Motivation:
We are building an editorial prioritization system for FlyRank. A content strategist manages 30,000 pages across 32 clients and has time to review only 50 pages per week. We are predicting `is_declining_label = (trend_direction == 'down')` to rank pages in descending order of decline risk. If our model has data leakage, editors will waste hundreds of hours reviewing false positives, and real declining pages will be missed.

Dataset Columns:
`content_id`, `client_id`, `search_volume`, `competition`, `word_count`, `impressions_90d`, `clicks_90d`, `impressions_last_30d`, `impressions_prev_30d`, `avg_position`, `trend_direction`, `trend_pct`.

Analyze this schema, enforce zero-leakage rules, and recommend a safe feature matrix and validation split.
```

#### Output (Representative Excerpt)
```text
### Engineering & Integrity Audit: FlyRank Editorial Prioritization

**Problem Framing Alignment:**
Because the strategist reviews only 50 pages/week, the optimization metric must be **Precision@50**, not accuracy or global ROC-AUC. 

**Data Leakage & Field Classification:**
- **Target Definition:** `is_declining_label = (trend_direction == 'down')` (observed threshold: $\le -20\%$ traffic drop).
- **Excluded (Direct Leakage):** `trend_direction`, `trend_pct`, `impressions_last_30d`, `impressions_prev_30d`. These contain future information relative to the pre-trend baseline.
- **Context Identifiers (Not Features):** `content_id` (row grain), `client_id` (grouping entity).
- **Safe Features:** `search_volume`, `competition`, `word_count`, `impressions_90d`, `clicks_90d`, `avg_position`.

**Validation Split Rule:**
Because pages belong to 32 clients, a random row split will leak client-specific domain patterns. You MUST use a **GroupShuffleSplit on `client_id`** (e.g. 20% held-out clients) to evaluate generalization.
```

#### Notes on Iteration 2
- **What changed in the prompt:** Provided the real operational context (FlyRank 30k pages, 32 clients, strategist capacity: 50 pages/week, cost of wrong decisions).
- **What actually improved in the output:** The AI connected the business constraint to ML design—it recommended `Precision@50` instead of accuracy and demanded a `GroupShuffleSplit` on `client_id` rather than a standard random split.
- **What still failed:** Lacked concrete examples of how to categorize borderline/derived signals (e.g. derived ratios like CTR or log-transforms), leaving room for interpretation.
- **What to try next:** Add **Few-Shot Examples** illustrating exact categorization and transformation patterns.

---

### Iteration 3: + Named Technique 3 (Few-Shot Examples)

#### The Prompt
```text
You are a Principal Machine Learning Engineer and Senior Data Integrity Auditor specializing in tabular ranking systems and search console analytics.

Context & Business Motivation:
Building an editorial prioritization system for FlyRank (30k pages, 32 clients). Target is `is_declining_label = (trend_direction == 'down')`. Primary evaluation metric is Precision@50 on 20% held-out clients (`GroupShuffleSplit` on `client_id`).

Here are examples of how you classify fields into four strict contract buckets:
<example>
Input field: `impressions_last_30d`
Bucket: EXCLUDED
Rationale: Directly used in computing `trend_pct = (last_30 - prev_30)/prev_30`. Mathematically leaks the target outcome window.

Input field: `impressions_90d`
Bucket: FEATURE
Rationale: Aggregate historical volume over 90 days. Knowable before the specific outcome window. Needs `np.log1p` transform due to heavy-tail distribution.

Input field: `client_id`
Bucket: CONTEXT
Rationale: Categorical entity identifier. Must never be an input feature (prevents overfitting to known domains), but required for GroupShuffleSplit.
</example>

Now classify all remaining columns:
`content_id`, `search_volume`, `competition`, `word_count`, `clicks_90d`, `impressions_prev_30d`, `avg_position`, `trend_direction`, `trend_pct`.
```

#### Output (Representative Excerpt)
```text
### Field Classification Audit

- **`content_id`** -> **CONTEXT**: Unique row key. Used for tracking, joining, and final queue generation; never as an input feature.
- **`search_volume`** -> **FEATURE**: Pre-existing keyword demand metric. Fill missing values with 0.
- **`competition`** -> **FEATURE**: Continuous keyword difficulty index [0.0, 1.0].
- **`word_count`** -> **FEATURE**: Structural content property. Fill missing with median or 0.
- **`clicks_90d`** -> **FEATURE**: 90-day search engagement total. Safe historical signal; recommend `np.log1p(clicks_90d)` and deriving `ctr = clicks_90d / impressions_90d`.
- **`impressions_prev_30d`** -> **EXCLUDED**: Denominator of the trend label formula; overlaps the target generation window.
- **`avg_position`** -> **FEATURE**: GSC ranking metric. Note: `0` indicates no ranking data, not top position.
- **`trend_direction`** -> **LABEL**: Ground truth source for `is_declining_label`.
- **`trend_pct`** -> **EXCLUDED**: Continuous representation of the label. Severe target leakage.
```

#### Notes on Iteration 3
- **What changed in the prompt:** Provided 3 few-shot XML-tagged exemplars demonstrating the exact reasoning format for `EXCLUDED`, `FEATURE`, and `CONTEXT`.
- **What actually improved in the output:** Every column was rigorously categorized into the 4 exact contract buckets without ambiguity. It also caught domain-specific nuances like `avg_position == 0` meaning "no data".
- **What still failed:** The output was delivered as a bulleted text list rather than a machine-readable data contract table or executable Python script.
- **What to try next:** Enforce **Output Structure** using a structured Markdown table and executable Python verification block.

---

### Iteration 4: + Named Technique 4 (Output Structure)

#### The Prompt
```text
You are a Principal Machine Learning Engineer and Senior Data Integrity Auditor.

Context:
FlyRank editorial prioritization (30,000 pages, 32 clients). Target: `is_declining_label = (trend_direction == 'down')`. Validation: `GroupShuffleSplit` on `client_id` (20% holdout). Metric: Precision@50.

Classify these columns:
`content_id`, `client_id`, `search_volume`, `competition`, `word_count`, `impressions_90d`, `clicks_90d`, `impressions_last_30d`, `impressions_prev_30d`, `avg_position`, `trend_direction`, `trend_pct`.

Output Structure Requirements:
1. Markdown Table with columns: | Field Name | Data Type | Contract Bucket (Feature / Label / Context / Excluded) | Leakage Risk Level (None / High) | Engineering / Imputation Rule |
2. Executable Python snippet defining `FEATURE_COLS`, `CONTEXT_COLS`, and `EXCLUDED_COLS` with an explicit `assert` statement proving zero leakage.
```

#### Output (Representative Excerpt)
```markdown
### 1. Search Intelligence Data Contract

| Field Name | Data Type | Contract Bucket | Leakage Risk Level | Engineering / Imputation Rule |
|---|---|---|---|---|
| `content_id` | String | Context | None | Identifier only; exclude from X |
| `client_id` | String | Context | None | Grouping key for GroupShuffleSplit |
| `search_volume` | Float | Feature | None | `fillna(0)`, apply `np.log1p` |
| `competition` | Float | Feature | None | `fillna(0)` (range 0.0 - 1.0) |
| `word_count` | Float | Feature | None | `fillna(0)` |
| `impressions_90d` | Float | Feature | None | `np.log1p(impressions_90d)` |
| `clicks_90d` | Float | Feature | None | `np.log1p(clicks_90d)` |
| `avg_position` | Float | Feature | None | `fillna(0)`; treat 0 as missing |
| `trend_direction` | String | Label | High (Target) | `(df['trend_direction'] == 'down').astype(int)` |
| `trend_pct` | Float | Excluded | High (Leakage) | Exclude: mathematically defines label |
| `impressions_last_30d` | Float | Excluded | High (Leakage) | Exclude: outcome window numerator |
| `impressions_prev_30d` | Float | Excluded | High (Leakage) | Exclude: outcome window denominator |

### 2. Python Verification Code
```python
FEATURE_COLS = ['search_volume', 'competition', 'word_count', 'impressions_90d', 'clicks_90d', 'avg_position']
CONTEXT_COLS = ['content_id', 'client_id']
LABEL_COL = 'is_declining_label'
EXCLUDED_COLS = ['trend_direction', 'trend_pct', 'impressions_last_30d', 'impressions_prev_30d']

# Assert zero leakage in feature matrix
assert all(col not in FEATURE_COLS for col in EXCLUDED_COLS), "Critical Error: Target leakage in features!"
```
```

#### Notes on Iteration 4
- **What changed in the prompt:** Mandated a strict Markdown schema (5-column table) and executable Python constants with assertion tests.
- **What actually improved in the output:** Output became directly usable in documentation and codebases. The table format makes code reviews instant, and the code snippet includes automated assertion guards.
- **What still failed:** The AI did not systematically explain its step-by-step reasoning for edge-case features (e.g. why derived rates like CTR need safe division, or how missingness patterns in categoricals should be handled).
- **What to try next:** Add **Step Decomposition** (chain-of-thought instructions) to force rigorous, auditable step-by-step execution.

---

### Iteration 5: + Named Technique 5 (Step Decomposition / Chain of Thought)

#### The Prompt
```text
You are a Principal Machine Learning Engineer and Senior Data Integrity Auditor.

Context:
FlyRank editorial prioritization (30,000 pages, 32 clients). Target: `is_declining_label = (trend_direction == 'down')`. Validation: `GroupShuffleSplit` on `client_id` (20% holdout). Metric: Precision@50.

Dataset Columns:
`content_id`, `client_id`, `search_volume`, `competition`, `word_count`, `impressions_90d`, `clicks_90d`, `impressions_last_30d`, `impressions_prev_30d`, `avg_position`, `trend_direction`, `trend_pct`.

Execute your analysis following these mandatory steps:
Step 1: Formalize Target & Outcome Window (Define the exact mathematical boundary of what is being predicted).
Step 2: Trace Dependency Graph & Flag Leakage (Identify all columns mathematically downstream of or overlapping the target window).
Step 3: Missingness & Distribution Audit (Analyze skewness, zero-flags, and imputation rules).
Step 4: Output Contract Table (Markdown table: Field, Type, Bucket, Leakage Risk, Imputation Rule).
Step 5: Production Python Pipeline (Modular functions: `prepare_features()`, `split_data()`, `evaluate_precision_at_50()`, with leakage assertion checks).
```

#### Output (Representative Excerpt)
```markdown
### Step 1: Formalize Target & Outcome Window
- **Target:** `is_declining_label = (trend_direction == 'down')`
- **Window Definition:** Measured across trailing days 1–30 (`last_30d`) vs days 31–60 (`prev_30d`). A page is positive if traffic dropped $> 20\%$.

### Step 2: Dependency Graph & Leakage Trace
- `trend_pct` $= \frac{\text{last\_30d} - \text{prev\_30d}}{\text{prev\_30d}} \times 100 \implies$ **Direct Mathematical Equivalent (EXCLUDED)**.
- `impressions_last_30d`, `impressions_prev_30d` $\implies$ **Direct Window Overlap (EXCLUDED)**.

### Step 3: Missingness & Distribution Audit
- `impressions_90d`, `clicks_90d`: Power-law distribution $\implies$ apply `np.log1p()`.
- `avg_position`: `0` indicates no recorded ranking $\implies$ impute with neutral/worst-case value.
- Derived CTR: $\frac{\text{clicks\_90d}}{\text{impressions\_90d}} \implies$ guard against zero-division using `.replace(0, np.nan).fillna(0)`.

### Step 4: Search Intelligence Data Contract Table
| Field Name | Type | Contract Bucket | Leakage Risk | Imputation & Transformation Rule |
|---|---|---|---|---|
| `content_id` | String | Context | None | Identifier only |
| `client_id` | String | Context | None | Group key for `GroupShuffleSplit` |
| `search_volume` | Float | Feature | None | `fillna(0)`, `np.log1p` |
| `competition` | Float | Feature | None | `fillna(0)` |
| `word_count` | Float | Feature | None | `fillna(0)` |
| `impressions_90d` | Float | Feature | None | `np.log1p(fillna(0))` |
| `clicks_90d` | Float | Feature | None | `np.log1p(fillna(0))` |
| `avg_position` | Float | Feature | None | `fillna(0)` |
| `trend_direction` | String | Label | High | Ground truth label source |
| `trend_pct` | Float | Excluded | High | Mathematical leakage |
| `impressions_last_30d` | Float | Excluded | High | Temporal outcome leakage |
| `impressions_prev_30d` | Float | Excluded | High | Temporal outcome leakage |

### Step 5: Production Python Pipeline
```python
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupShuffleSplit

def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Builds leakage-free feature matrix with log transforms."""
    # Label definition
    y = (df['trend_direction'].str.lower() == 'down').astype(int)
    groups = df['client_id']
    
    # Feature matrix (strictly historical signals)
    X = pd.DataFrame({
        'log_impressions_90d': np.log1p(df['impressions_90d'].fillna(0)),
        'log_clicks_90d': np.log1p(df['clicks_90d'].fillna(0)),
        'search_volume': np.log1p(df['search_volume'].fillna(0)),
        'competition': df['competition'].fillna(0),
        'word_count': df['word_count'].fillna(0),
        'avg_position': df['avg_position'].fillna(0),
        'ctr': (df['clicks_90d'] / df['impressions_90d'].replace(0, np.nan) * 100).fillna(0),
    })
    
    # Anti-leakage assertions
    banned = {'trend_direction', 'trend_pct', 'impressions_last_30d', 'impressions_prev_30d'}
    assert not banned.intersection(X.columns), "FATAL: Leakage columns detected in feature matrix!"
    return X, y, groups

def evaluate_precision_at_50(y_true: pd.Series, y_scores: np.ndarray) -> float:
    ranked = pd.DataFrame({'y': y_true.values, 'score': y_scores}).sort_values('score', ascending=False)
    return float(ranked.head(50)['y'].mean())
```
```

#### Notes on Iteration 5
- **What changed in the prompt:** Decomposed the prompt into 5 explicit chronological steps (Target formalization $\rightarrow$ Dependency trace $\rightarrow$ Missingness audit $\rightarrow$ Contract table $\rightarrow$ Production code).
- **What actually improved in the output:** The reasoning process became transparent and auditable. Every mathematical derivation was justified before code was written, resulting in a production-ready, fully verified ML pipeline.
- **Verdict:** Highly successful. Reached production-grade completeness.

---

## 3. Cross-Model Comparison: Claude vs ChatGPT (GPT-4o)

The final Iteration 5 prompt was executed on both **Claude 3.7 / 3.5 Sonnet** and **ChatGPT (GPT-4o)** to evaluate how different frontier models respond to the engineered instructions.

| Dimension | Claude (Sonnet) | ChatGPT (GPT-4o) | Specific Observed Difference |
|---|---|---|---|
| **Tone & Style** | Precise, cautious, engineering-first. Uses minimal fluff. | Conversational, structured, polite, slightly more verbose. | Claude jumped straight into Step 1; ChatGPT added an introductory preamble restating the objective. |
| **Leakage Detection** | Rigorous mathematical explanation of why ratio denominators leak target information. | Correctly identified leakage columns, but explained them as "high correlation" rather than strict mathematical equivalence. | Claude identified the mathematical derivation formula; GPT-4o framed it conceptually. |
| **Structural Compliance** | $100\%$ compliant with all 5 requested steps and exact markdown table columns. | $100\%$ compliant with the 5 steps; added extra explanatory bullet points under the table. | Both models followed formatting instructions perfectly when given explicit step decomposition. |
| **Code Quality & Edge Cases** | Handled `avg_position == 0` missingness nuance and used `.replace(0, np.nan)` for zero-division guard. | Used standard `fillna(0)` and basic division without explicit zero-division guard in the first code draft. | Claude wrote safer numerical code for rate calculation. |
| **Failure Points** | Tendency to assume all non-leaking columns should be included without checking cardinality. | Tendency to add unnecessary sklearn boilerplate (e.g. `GridSearchCV`) not requested in the prompt. | Claude stayed strictly within scope; ChatGPT over-engineered model tuning. |

---

## 4. Final Reusable Prompt Template

This generalized prompt template can be used by any data scientist or ML engineer auditing a new tabular dataset for leakage, data contracts, and production preparation:

```text
You are a Principal Machine Learning Engineer and Senior Data Integrity Auditor.

Task:
Perform a comprehensive data integrity, leakage audit, and feature contract definition for a tabular ML dataset.

Context & Business Motivation:
- Project Goal: <INSERT_GOAL_AND_DECISION_TYPE e.g. Ranking pages for content refresh>
- Dataset Scope: <INSERT_ROW_COUNT_AND_ENTITIES e.g. 30,000 rows across 32 clients>
- Target Variable: `<INSERT_TARGET_NAME>` defined as `<INSERT_TARGET_FORMULA_OR_CONDITION>`
- Key Operational Metric: <INSERT_DECISION_METRIC e.g. Precision@K, NDCG, or Cost-weighted Recall>
- Primary Entity / Group Column: `<INSERT_GROUP_ID_FOR_SPLIT>`

Dataset Schema:
<PASTE_ALL_COLUMN_NAMES_AND_DATA_TYPES>

Execution Steps:
Step 1: Formalize Target & Outcome Window — State the exact mathematical definition of the label and the temporal window it spans.
Step 2: Trace Dependency Graph & Flag Leakage — Audit every column for mathematical derivation from or temporal overlap with the target window. Categorize leakage risk (None vs High).
Step 3: Missingness, Skewness & Imputation Rules — Specify handling for heavy-tailed numerics (log-transforms), zero-flags, and categorical missingness.
Step 4: Search Intelligence Data Contract Table — Output a Markdown table with columns: `Field Name`, `Data Type`, `Contract Bucket (Feature / Label / Context / Excluded)`, `Leakage Risk Level`, and `Engineering / Imputation Rule`.
Step 5: Production Python Pipeline — Provide clean, modular Python functions (`prepare_features`, `split_data`, `evaluate_metric`) with strict assertion checks verifying zero leakage columns in the feature matrix.
```

---

## 5. Summary & Self-Check

- [x] Evaluated on a real task from FL-01 workflow audit (*Cleaning and exploring datasets / Pipeline debugging*).
- [x] Six total runs documented (Baseline + 5 distinct named iterations).
- [x] Each note explains observed output changes, not just prompt changes.
- [x] Honest cross-model comparison (Claude vs ChatGPT) with specific observed differences.
- [x] Reusable parameterized prompt template created for public sharing.
