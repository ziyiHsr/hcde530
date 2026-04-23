# Fetches research-tool reviews from the HCDE 530 week 4 API, summarizes by category, saves CSV.
import csv
import json
from collections import defaultdict
from pathlib import Path
import urllib.error
import urllib.request

# Service root: https://hcde530-week4-api.onrender.com/  — review data: /reviews
API_REVIEWS_URL = "https://hcde530-week4-api.onrender.com/reviews?limit=10"
OUTPUT_CSV = Path(__file__).resolve().parent / "reviews_summary_by_category.csv"


def summarize_by_category(reviews):
    """Group reviews by research category: counts, average rating, helpful-vote totals and means."""
    stats = defaultdict(lambda: {"n": 0, "rating_sum": 0, "helpful_sum": 0})
    for r in reviews:
        cat = r.get("category") or "(unknown)"
        s = stats[cat]
        s["n"] += 1
        s["rating_sum"] += int(r.get("rating", 0) or 0)
        s["helpful_sum"] += int(r.get("helpful_votes", 0) or 0)

    rows = []
    for category in sorted(stats):
        s = stats[category]
        n = s["n"]
        rows.append(
            {
                "category": category,
                "review_count": n,
                "avg_rating": round(s["rating_sum"] / n, 2) if n else 0.0,
                "total_helpful_votes": s["helpful_sum"],
                "avg_helpful_votes": round(s["helpful_sum"] / n, 2) if n else 0.0,
            }
        )
    return rows


def main():
    try:
        with urllib.request.urlopen(API_REVIEWS_URL) as response:
            body = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(f"Could not reach the API: {e}")
        raise SystemExit(1) from e

    data = json.loads(body)
    reviews = data.get("reviews", [])

    if not reviews:
        print("No reviews returned.")
        return

    total = data.get("total")
    if total is not None:
        print(
            f"API reports {data.get('returned', len(reviews))} review(s) in this page "
            f"of {total} total in the dataset.\n"
        )

    summary = summarize_by_category(reviews)

    print("Summary by research category (this page)")
    print(
        f"{'Category':<28} {'#':>3}  {'Avg rating':>10}  {'Total helpful':>14}  {'Avg helpful':>11}"
    )
    print("-" * 75)
    for row in summary:
        print(
            f"{row['category']!s:<28} {row['review_count']:>3}  "
            f"{row['avg_rating']:>10.2f}  {row['total_helpful_votes']:>14}  "
            f"{row['avg_helpful_votes']:>11.2f}"
        )

    fieldnames = [
        "category",
        "review_count",
        "avg_rating",
        "total_helpful_votes",
        "avg_helpful_votes",
    ]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary)

    print()
    print(f"Wrote {len(summary)} row(s) to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
