# Week 5 — Competency claim (A5): **C5 — Data Analysis with Pandas**

## What C5 means (for this assignment)

Using **pandas** to answer a **real question** about a dataset: filtering rows, grouping, aggregating, handling missing values, choosing the **right operation** for what I want to know, and **interpreting** the output—not only printing it.

---

## Evidence

| Requirement | Where it shows up |
|-------------|-------------------|
| **Loads a dataset** | `week5_Pandas_Analysis.ipynb` reads `artworks.csv` (50-object extract from The Met Collection API for MP1; [API docs](https://metmuseum.github.io/)). |
| **At least one specific analytical question** | I answer **three**: (1) distribution across `department`, (2) missing values in key fields (`objectDate`, `medium`; no `classification` column in this export), (3) how `medium` varies by `department`. |
| **At least two pandas operations** | Examples: `value_counts`, boolean row filtering (`df[...]`), `isnull().sum()`, `groupby(...).nunique()`, `groupby(...).mean()` on a derived column (medium string length). |
| **Written interpretation** | See **Interpretation** below and the **`#` comments** in the notebook after each code cell. |

---

## Interpretation (what the results mean)

**1 — Department distribution.** In this 50-row extract, **`European Paintings` has the most objects (14 rows, 28% of the sample)**, followed by **`Asian Art` and `European Sculpture and Decorative Arts` (9 each, 18%)**. That tells me the sample is **not evenly spread** across curatorial departments; any MP1 comparison “by department” should mention this imbalance or stratify if I pull more data later.

**2 — Missing values.** On `objectDate`, `medium`, and `department`, **`medium` and `department` are complete here**; **`objectDate` is missing once** (object **436885**, European Paintings). So for MP1 I should **not assume dates are always present**—I may need a rule for display or analysis when `objectDate` is blank, even if it is rare in this slice.

**3 — Medium by department.** **`groupby('department')['medium'].nunique()`** shows several departments with **many distinct medium strings in a tiny sample** (e.g. **Asian Art** and **European Paintings** each with **9** distinct `medium` values in this file). That suggests **material diversity is high within those departments**; for MP1 I flagged **checking whether long “medium” text needs normalization** (splitting materials vs. one free-text blob) when I scale up beyond 50 rows.

---

## Strong competency claim (C5)

I used pandas on my Met extract to **group and count by `department`**, **quantify missing `objectDate` / `medium`**, **filter to rows with gaps**, and **group by `department` to summarize how many distinct media appear**. The pattern that stood out: **the sample skews heavily toward European Paintings**, **almost all dates and media are present except one missing date**, and **medium diversity within departments is already large at *n* = 50**. I recorded those interpretations here and noted **stratified sampling and date-cleaning** as next steps for MP1—not just “I ran pandas and got tables.”
