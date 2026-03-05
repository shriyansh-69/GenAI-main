import json 
import os

# Input And Output files
input_file = "arxiv-metadata-oai-snapshot.json"
output_file = "data/arxiv_cs.json"

# Valid So It Doesn't Crash
os.makedirs("data", exist_ok=True)


# Extracting Related From The Dataset And  Setting Limit For Number of Document's
cs_papers = []
limit = 60000

print("Filtering Computer Science papers...\n")

with open(input_file,"r",encoding="utf-8") as f:
    for line in f:
        try:
            paper = json.loads(line)

            categories  = paper.get("categories","")

            if "cs." in categories:
                cs_papers.append({
                    "id" : paper.get("id"),
                    "title" : paper.get("title"),
                    "abstract" : paper.get("abstract"),
                    "categories" : categories,
                    "update_date" : paper.get("update_date"),
                })


            # It IS For Stopping When The Data Hit's the Limit 
            if len(cs_papers) >= limit:
                break

        except Exception:
            continue  # SKIP Bad Lines Safely 

print(f"Total CS papers extracted: {len(cs_papers)}")



        


