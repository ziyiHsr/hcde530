#!/usr/bin/env python3
"""Read responses.csv, drop rows with empty name, uppercase role, write responses_cleaned.csv."""

import csv
from pathlib import Path


INPUT_PATH = Path(__file__).resolve().parent / "responses.csv"
OUTPUT_PATH = Path(__file__).resolve().parent / "responses_cleaned.csv"


def main() -> None:
    with INPUT_PATH.open(newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        if reader.fieldnames is None:
            raise SystemExit("CSV has no header row.")

        fieldnames = list(reader.fieldnames)
        if "name" not in fieldnames:
            raise SystemExit("CSV must include a 'name' column.")
        if "role" not in fieldnames:
            raise SystemExit("CSV must include a 'role' column.")

        rows_out = []
        for row in reader:
            name = (row.get("name") or "").strip()
            if not name:
                continue
            row = dict(row)
            row["name"] = name
            role_val = row.get("role") or ""
            row["role"] = role_val.upper()
            rows_out.append(row)

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"Wrote {len(rows_out)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
