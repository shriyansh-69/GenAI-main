## This File Is Used For Converting XML Into json 

import xml.etree.ElementTree as et
import json 
import os


xml_root = "data/xml/MedQuAD"
output_json = "data/medquad.json"

all_qa = []

for root_dir, _, files in os.walk(xml_root):
    for file  in files:
        if not file.endswith(".xml"):
            continue

        file_path = os.path.join(root_dir, file)

        try :
            tree = et.parse(file_path)
            root = tree.getroot()

            qapairs = root.find("QAPairs")
            if qapairs is None:
                continue

            for qa in qapairs.findall("QAPair"):
                q = qa.find("Question")
                a = qa.find("Answer")

                if q is None or a is None:
                    continue


            question = "".join(q.itertext()).strip()
            answer = "".join(a.itertext()).strip()



            if question and answer:
                all_qa.append({
                    "question" : question,
                    "answer" : answer
                })

        except Exception as e:
            print(f"Skipped {file_path}  error: {e}")

with open(output_json,"w", encoding="utf-8") as f:
    json.dump(all_qa, f, indent=2, ensure_ascii=False)

print("====================================")
print(f"Total Q&A pair's Extracted: {len(all_qa)}")
print(f"✅ Saved to: {output_json}")
print("====================================")

# Description This Code  Is For Converting The XML Content  Into Json 
# For Our RAG

    





        