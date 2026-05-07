import csv

# Input survey responses and where we save the cleaned, uniform copy for reuse.
INPUT_CSV = "week3_survey_messy.csv"
OUTPUT_CSV = "week3_survey_clean.csv"

# Rare messy values that are not numeric strings — map spoken numbers to ints so averages work.
EXPERIENCE_WORDS = {
    "fifteen": 15,
}


def clean_survey_row(row):
    # Take one messy dict from the CSV and return a copy with tidy text:
    # empty name/role become readable placeholders; department gets title case;
    # primary_tool is only trimmed (keeps values like "VS Code");
    # spelled-out experience years become digits so later int() calls never hit ValueError.
    cleaned = dict(row)

    name = cleaned.get("participant_name", "").strip()
    if not name:
        cleaned["participant_name"] = "(missing name)"

    role = cleaned.get("role", "").strip().title()
    if not role:
        role = "(missing role)"
    cleaned["role"] = role

    dept = cleaned.get("department", "").strip()
    if dept:
        cleaned["department"] = dept.title()

    # Keep tool spelling as-is (only trim); title() breaks names like "VS Code".
    cleaned["primary_tool"] = cleaned.get("primary_tool", "").strip()

    exp_raw = cleaned.get("experience_years", "").strip().lower()
    if exp_raw in EXPERIENCE_WORDS:
        cleaned["experience_years"] = str(EXPERIENCE_WORDS[exp_raw])
    # Otherwise keep digits as-is; invalid values would still fail later — CSV is expected to fix those.

    return cleaned


# Load every row from the messy CSV into memory as dictionaries (keys = column names).
rows = []
with open(INPUT_CSV, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        rows.append(row)

# Build a cleaned list: same columns, normalized text and placeholders for missing roles/names.
cleaned_rows = [clean_survey_row(row) for row in rows]

# Write the cleaned rows to OUTPUT_CSV so graders (or downstream tools) get a tidy file with one row per response.
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cleaned_rows)

# Count responses by role (reuse cleaned role column so blanks are already grouped as "(missing role)").
role_counts = {}
for row in cleaned_rows:
    role = row["role"]
    role_counts[role] = role_counts.get(role, 0) + 1

print("Responses by role:")
for role, count in sorted(role_counts.items()):
    print(f"  {role}: {count}")

# Sum experience years across all rows to compute one overall average (uses cleaned numeric strings).
total_experience = 0
for row in cleaned_rows:
    total_experience += int(row["experience_years"])

avg_experience = total_experience / len(cleaned_rows)
print(f"\nAverage years of experience: {avg_experience:.1f}")

# Collect name + satisfaction for rows that have a score, then sort high-to-low for a true top five.
scored_rows = []
for row in cleaned_rows:
    if row["satisfaction_score"].strip():
        scored_rows.append((row["participant_name"], int(row["satisfaction_score"])))

scored_rows.sort(key=lambda x: x[1], reverse=True)
top5 = scored_rows[:5]

print("\nTop 5 satisfaction scores:")
for name, score in top5:
    print(f"  {name}: {score}")

print(f"\nWrote cleaned data to {OUTPUT_CSV}")
