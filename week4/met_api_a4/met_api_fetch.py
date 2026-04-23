import csv
import requests
import time

# This script uses The Metropolitan Museum of Art Collection API.
# The search endpoint returns object IDs that match a keyword query.
SEARCH_URL = "https://collectionapi.metmuseum.org/public/collection/v1/search"
OBJECT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects/{}"

# We search for artworks related to cats.
# hasImages=true helps us return artworks that include image links.
search_params = {
    "q": "cat",
    "hasImages": "true"
}

# Send a GET request to the search endpoint and parse the JSON response.
search_response = requests.get(SEARCH_URL, params=search_params)
search_response.raise_for_status()
search_data = search_response.json()

# The search response includes a list of matching object IDs.
object_ids = search_data.get("objectIDs", [])

if not object_ids:
    print("No objects found.")
    exit()

rows = []

# We only need at least 50 records for the assignment.
for object_id in object_ids[:50]:
    object_response = requests.get(OBJECT_URL.format(object_id))
    object_response.raise_for_status()
    obj = object_response.json()

    # We extract fields that are useful for understanding each artwork.
    # These fields could support search, browsing, or educational interfaces.
    row = {
        "objectID": obj.get("objectID"),
        "title": obj.get("title"),
        "artistDisplayName": obj.get("artistDisplayName"),
        "objectDate": obj.get("objectDate"),
        "department": obj.get("department"),
        "medium": obj.get("medium"),
        "primaryImageSmall": obj.get("primaryImageSmall"),
        "objectURL": obj.get("objectURL")
    }
    rows.append(row)

    # Small pause to avoid sending requests too quickly.
    time.sleep(0.05)

# Save the structured output to a CSV file so it can be reviewed and reused.
with open("artworks.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = [
        "objectID",
        "title",
        "artistDisplayName",
        "objectDate",
        "department",
        "medium",
        "primaryImageSmall",
        "objectURL"
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# Print a readable preview so the output is visible in the terminal too.
print(f"Saved {len(rows)} records to artworks.csv")
for row in rows[:5]:
    print(row["title"], "-", row["artistDisplayName"], "-", row["objectDate"])
