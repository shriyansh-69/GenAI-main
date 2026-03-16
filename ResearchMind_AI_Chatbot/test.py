# This File Is For Checking That The Paper's Are Loaded Are CS Pages

import json

with open("data/arxiv_cs.json","r",encoding="utf-8") as f:
    papers = json.load(f)

invalid = []

for paper in papers:
    categories = paper.get("categories", "")

    if not any(cat.startswith("cs.") for cat in categories.split()):
        invalid.append(categories)

print("Total Papers",len(papers))
print("Invalid Papers",len(invalid))

