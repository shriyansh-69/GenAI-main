# We Can Use This File For Checking If There Any InValid File Are Stored

import json

with open("data/arxiv_cs.json","r",encoding="utf-8") as f:
    papers = json.load(f)

invalid = []

for paper in papers:
    categories = paper.get("categories", "")

    if not any(cat.startswith("cs.") for cat in categories.split()):
        invalid.append(categories)


print("Total papers:", len(papers))
print("Invalid File", len(invalid))
