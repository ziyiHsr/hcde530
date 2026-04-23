# HCDE 530 A4 - The Met API

This project uses The Metropolitan Museum of Art Collection API to retrieve structured artwork data.

The script:
- calls the Met search endpoint with the query "cat"
- retrieves detailed records for 50 artworks
- parses the JSON responses
- extracts selected fields such as title, artist, date, and medium
- saves the results to a CSV file

Files:
- `met_api_fetch.py` - main Python script
- `artworks.csv` - structured output file
- `week4.md` - competency claim and HCD reflection
