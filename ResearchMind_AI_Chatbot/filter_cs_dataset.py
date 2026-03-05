import json 
import os

# Input And Output files
input_file = "arxiv-metadata-oai-snapshot.json"
output_file = "data/arxiv_cs.json"

# Valid So It Doesn't Crash
os.makedirs("data", exist_ok=True)


# Extracting Related From The Dataset And  Setting Limit For Number of Document's
cs_paper = []
limit = 60000


