# Week 3 — Competency claim (A3 revision): **C3 — Data Cleaning and File Handling**

## What C3 means (for this assignment)

**Loading messy real-world data with Python**, figuring out **what is broken** (from errors and from bad-looking output), **fixing it so the script runs cleanly** on the messy CSV, **using error messages as diagnostics**, and **writing predictable output** — a cleaned file and summaries I can reproduce by re-running the script, not by hand-editing spreadsheets each time.

---

## What counts as evidence (mapping to this submission)

| C3 evidence item | Where it shows up |
|------------------|-------------------|
| **Python script reads from a CSV (not hardcoded data)** | `week3_analysis_buggy.py` uses `csv.DictReader` on **`week3_survey_messy.csv`** (`INPUT_CSV`). |
| **At least one real data problem handled** | **Non-numeric value:** spoken number `fifteen` in **`experience_years`** (would break `int()`). **Inconsistent formatting:** mixed-case roles/departments; **`clean_survey_row`** applies consistent casing where safe (`role`/`department`) and trims fields. **Missing entries:** blank **`participant_name`** / **`role`** — replaced with **`(missing name)`** / **`(missing role)`** so downstream counts and CSV exports stay interpretable. |
| **Traceback read and diagnosed** | See section below (**what the error was pointing to**). |
| **Commit history: found → understood → fixed** | Git commits with specific messages for the **`fifteen` / ValueError**, the **mis-sorted “top 5” satisfaction**, **empty role labeling**, plus a commit adding the **cleaning pipeline + `week3_survey_clean.csv`** artifact and inline documentation. |

---

## Traceback: what the error was pointing to

When the original script totaled experience, Python raised:

`ValueError: invalid literal for int() with base 10: 'fifteen'`.

That traceback means **`int(...)` received a string that is not digits** (`'fifteen'`). Reading the traceback line pointed at the loop that summed **`row["experience_years"]`**, which told me the **survey row with a spelled-out value in the experience column** was the offender — not a bug in CSV parsing itself.

**How I fixed it (without hiding the messy pattern):**

- Corrected **`week3_survey_messy.csv`** so R009 stores **`15`** as digits for grading / reproducibility.
- Kept **`EXPERIENCE_WORDS`** in **`clean_survey_row`** so the same spelled-out wording is **converted to `'15'`** before any `int()` on experience — deliberate normalization instead of crashing on “almost numeric” entries.

(This differs from the course’s *example* solution using **`try`/`except` and skipping rows**; I chose **explicit mapping + source correction** so no row is dropped and the clean file stays complete.)

---

## Strong competency claim (C3)

**The script crashed with `ValueError: invalid literal for int() with base 10: 'fifteen'` because one row had the word `fifteen` in `experience_years` instead of a numeric string.** I used the traceback to locate the failing **`int(...)`**, confirmed it was bad cell content from the messy CSV (not CSV structure), fixed the source row to **`15`**, and added **`EXPERIENCE_WORDS` in `clean_survey_row`** so spelled-out years become digits before summaries run. Separately I fixed **misleading “top 5” satisfaction** (sort direction) and **missing `role` / name** placeholders so aggregates and **`week3_survey_clean.csv` are repeatable and readable.** My commits name each defect and fix so history matches diagnostics.
