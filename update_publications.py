from serpapi import GoogleSearch
import json
from collections import defaultdict

# Your SerpApi key and Google Scholar ID
API_KEY = "08420396472a78c1d9274803e3568cae469cd4c3fbab1385bb4043aa74bcd472"
SCHOLAR_ID = "j6ekzokAAAAJ"  # Replace with your Google Scholar ID

all_publications = []
page = 0

while True:
    params = {
        "engine": "google_scholar_author",
        "author_id": SCHOLAR_ID,
        "api_key": API_KEY,
        "start": page * 100
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    if "articles" not in results or not results["articles"]:
        break
    
    all_publications.extend(results["articles"])
    page += 1

# Group publications by year
publications_by_year = defaultdict(list)
for pub in all_publications:
    year = pub.get("year", "No Year")
    title = pub.get("title", "Untitled")
    authors = pub.get("authors", "Unknown Authors")
    journal = pub.get("publication", "Unknown Publication")
    link = pub.get("link", "#")
    
    citation = f"{authors} ({year}). {title}. <em>{journal}</em>. <a href='{link}' target='_blank'>Link</a>"
    publications_by_year[year].append(citation)

# Sort years
sorted_years = sorted(publications_by_year.keys(), reverse=True)

# Save JSON
with open("publications.json", "w", encoding="utf-8") as f:
    json.dump({year: publications_by_year[year] for year in sorted_years}, f, ensure_ascii=False, indent=4)

print("✅ publications.json updated successfully!")
