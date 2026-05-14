# Metadata Completeness in The Met Collection: An Exploratory Random Sample Analysis

## Project title

**Metadata Completeness in The Met Collection: An Exploratory Random Sample Analysis**

## Dataset and scope

- **Source:** The Metropolitan Museum of Art **Collection API**  
  https://metmuseum.github.io/  
- **Scope:** Public catalog metadata for collection objects, accessed via:
  - `GET /public/collection/v1/objects` — full list of `objectID`s  
  - `GET /public/collection/v1/objects/{id}` — detail record for one object  
- **Fields analyzed:** `objectID`, `title`, `department`, `objectDate`, `culture`, `medium`, `classification`, `artistDisplayName`, `country`, `period`, `objectBeginDate`, `objectEndDate`  
- **Missing data:** Any absent key in JSON, `None`, empty string, or whitespace-only string is counted as missing after loading into pandas.

## Sampling strategy

I used a reproducible random sample of 500 objects from The Met Collection API using **seed=42**. I sampled object IDs first, then fetched details **only** for those sampled objects. This avoids fetching the full collection while still allowing exploratory analysis of metadata completeness.

The sample is saved as `met_metadata_random_sample.csv` in the MP1 folder alongside the analysis notebook.

## Three analytical questions

1. **Q1 — Which metadata fields are most often missing in the random sample?**  
   *Chart:* Missing Metadata Percentage by Field (`missing_metadata_by_field.png`)

2. **Q2 — Which departments have higher or lower average metadata completeness?**  
   *Chart:* Average Metadata Completeness by Department (`completeness_by_department.png`)

3. **Q3 — How complete are individual object records overall?**  
   *Chart:* Distribution of Metadata Completeness Scores Across Sampled Objects (`completeness_score_distribution.png`)

**Completeness score (per object):** Among the eleven content fields (all columns except `objectID`), the score is the percentage of those fields that are non-missing.

## Chart justification for each chart

- **Missing Metadata Percentage by Field**  
  A **horizontal bar chart** is appropriate because the fields are categorical and label text can be long. Bar length encodes the **percent of the 500 rows** where that field is missing, which directly answers Q1 and is easy to compare across fields.

- **Average Metadata Completeness by Department**  
  **Department** is a nominal grouping variable; **mean completeness** is a numeric summary per group. Horizontal bars sort departments by mean score so readers quickly see which departments in *this sample* tend to have more filled facets on average (Q2).

- **Distribution of Metadata Completeness Scores Across Sampled Objects**  
  The per-object completeness score is essentially a **numeric distribution** (in discrete steps of 1/11). A **histogram** shows central tendency, spread, and tails—answering Q3 by describing how “full” typical records are versus rare sparse records.

## Competency claims

- **C3 — Data cleaning and file handling**  
  I built the dataset by calling the Collection API with **retries and delays** to reduce failures from rate limiting, used **`.get()`** for safe JSON parsing, normalized **empty strings and missing values** into a consistent missing representation in pandas, and saved the result as **`met_metadata_random_sample.csv`** for reproducible analysis.

- **C5 — Data analysis with pandas**  
  I computed **missing percentages by field**, **mean completeness by department** with `groupby`, and **summary statistics** for the per-object completeness score to support the three research questions in **`week6_mp1_metadata_quality.ipynb`**.

- **C6 — Data visualization**  
  I created three **Plotly** figures aligned to Q1–Q3, with **clear titles and axis labels**, and exported them as **PNG** files in the MP1 folder (`missing_metadata_by_field.png`, `completeness_by_department.png`, `completeness_score_distribution.png`).

- **C7 — Critical evaluation and professional judgment**  
  I treated this work as **exploratory**: a single random sample does not represent every curatorial workflow, **completeness is not accuracy**, and API behavior (e.g. throttling) can affect individual rows. Findings should inform **priorities and UX expectations**, not automatic judgments about institutional quality.
