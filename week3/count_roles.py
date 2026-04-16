#!/usr/bin/env python3
"""Count how many times each role appears in responses.csv."""

import argparse
import csv
from collections import Counter
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "csv_path",
        nargs="?",
        default=Path(__file__).resolve().parent / "responses.csv",
        type=Path,
        help="Path to CSV (default: responses.csv next to this script)",
    )
    parser.add_argument(
        "--sort",
        choices=("count", "role"),
        default="count",
        help="Sort by descending count or alphabetically by role name",
    )
    args = parser.parse_args()

    if not args.csv_path.is_file():
        raise SystemExit(f"File not found: {args.csv_path}")

    counts: Counter[str] = Counter()
    with args.csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or "role" not in reader.fieldnames:
            raise SystemExit('Expected a "role" column in the CSV header.')
        for row in reader:
            role = (row.get("role") or "").strip()
            if role:
                counts[role] += 1

    items = list(counts.items())
    if args.sort == "count":
        items.sort(key=lambda x: (-x[1], x[0]))
    else:
        items.sort(key=lambda x: x[0].lower())

    total = sum(counts.values())
    print(f"Rows with a non-empty role: {total}\n")
    print(f"{'Role':<40} {'Count':>6}")
    print("-" * 48)
    for role, n in items:
        print(f"{role:<40} {n:>6}")
    print("-" * 48)
    print(f"{'Total':<40} {total:>6}")


if __name__ == "__main__":
    main()
