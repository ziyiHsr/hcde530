"""Load messy survey CSV, clean fields, export a cleaned CSV, and print analysis."""

from __future__ import annotations

import csv
from pathlib import Path

# Map English number words (0–19 and tens) without listing every key-value pair
_ONES = (
    "zero one two three four five six seven eight nine "
    "ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen"
).split()
_NUMBER_WORDS: dict[str, int] = {w: i for i, w in enumerate(_ONES)}
_TENS_WORDS = "twenty thirty forty fifty".split()
for i, w in enumerate(_TENS_WORDS):
    _NUMBER_WORDS[w] = (i + 2) * 10
_TENS_PREFIX = {w: _NUMBER_WORDS[w] for w in _TENS_WORDS}


def parse_experience_years(raw: str) -> int:
    """Parse digits or English words (e.g. fifteen -> 15, twenty-one -> 21)."""
    t = (raw or "").strip()
    if not t:
        raise ValueError("empty experience_years")
    try:
        return int(t)
    except ValueError:
        pass
    key = t.lower().replace(" ", "-")
    if key in _NUMBER_WORDS:
        return _NUMBER_WORDS[key]
    if "-" in key:
        left, right = key.split("-", 1)
        if left in _TENS_PREFIX and right in _NUMBER_WORDS:
            ones = _NUMBER_WORDS[right]
            if 1 <= ones <= 9:
                return _TENS_PREFIX[left] + ones
    raise ValueError(f"cannot parse experience_years: {raw!r}")


def load_survey_csv(path: Path) -> list[dict[str, str]]:
    """Read a survey CSV and return one dict per row (all values as strings)."""
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def clean_survey_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """
    Return a new list of rows with normalized text fields and numeric experience_years.

    Empty roles are stored as \"(missing role)\" so exports stay consistent with counts.
    """
    cleaned: list[dict[str, str]] = []
    for row in rows:
        out = dict(row)
        out["participant_name"] = (out.get("participant_name") or "").strip()
        role = (out.get("role") or "").strip().title()
        if not role:
            role = "(missing role)"
        out["role"] = role
        out["department"] = (out.get("department") or "").strip()
        out["age_range"] = (out.get("age_range") or "").strip()
        years = parse_experience_years(out.get("experience_years") or "")
        out["experience_years"] = str(years)
        out["satisfaction_score"] = (out.get("satisfaction_score") or "").strip()
        out["primary_tool"] = (out.get("primary_tool") or "").strip()
        out["response_text"] = (out.get("response_text") or "").strip()
        cleaned.append(out)
    return cleaned


def write_survey_csv(rows: list[dict[str, str]], path: Path) -> None:
    """Write survey rows to a new CSV file using the keys from the first row."""
    if not rows:
        raise ValueError("no rows to write")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize_data(rows: list[dict[str, str]]) -> str:
    """
    Build a short plain-language summary of cleaned survey data.

    Reports total rows, distinct role values, and how many participant names are empty.
    """
    n = len(rows)
    roles = {row["role"] for row in rows}
    empty_names = sum(1 for row in rows if not row.get("participant_name", "").strip())
    lines = [
        f"The dataset has {n} row{'s' if n != 1 else ''}.",
        f"The role column has {len(roles)} distinct value{'s' if len(roles) != 1 else ''}: "
        f"{', '.join(sorted(roles))}.",
        f"There are {empty_names} row{'s' if empty_names != 1 else ''} with an empty participant name.",
    ]
    return "\n".join(lines)


def main() -> None:
    base = Path(__file__).resolve().parent
    messy_path = base / "week3_survey_messy.csv"
    cleaned_path = base / "week3_survey_cleaned.csv"

    rows = load_survey_csv(messy_path)
    cleaned = clean_survey_rows(rows)
    write_survey_csv(cleaned, cleaned_path)
    print(f"Wrote cleaned data to {cleaned_path}\n")

    print(summarize_data(cleaned))
    print()

    role_counts: dict[str, int] = {}
    for row in cleaned:
        r = row["role"]
        role_counts[r] = role_counts.get(r, 0) + 1

    print("Responses by role:")
    for role, count in sorted(role_counts.items()):
        print(f"  {role}: {count}")

    total_experience = sum(int(row["experience_years"]) for row in cleaned)
    avg_experience = total_experience / len(cleaned)
    print(f"\nAverage years of experience: {avg_experience:.1f}")

    scored_rows: list[tuple[str, int]] = []
    for row in cleaned:
        if row["satisfaction_score"]:
            scored_rows.append((row["participant_name"], int(row["satisfaction_score"])))

    scored_rows.sort(key=lambda x: (-x[1], x[0]))
    top5 = scored_rows[:5]

    print("\nTop 5 satisfaction scores:")
    for name, score in top5:
        label = name if name else "(no name)"
        print(f"  {label}: {score}")


if __name__ == "__main__":
    main()
