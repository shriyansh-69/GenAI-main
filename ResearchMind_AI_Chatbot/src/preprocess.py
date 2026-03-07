import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_word = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)

    words = text.split()

    words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_word
    ]

    return " ".join(words)

# Loading The Filtered Dataset 
with open("data/arxiv_cs.json","r",encoding="utf-8") as f:
    papers = json.load(f)

print(f"Loaded {len(papers)} Paper's ")


# Preprocess Abstracts

for paper in papers:
    abstract = paper.get("abstract", "")
    paper["clean_abstract"] = clean_text(abstract)


# Saving processed Dataset

with open("data/arxiv_cs_clean.json","w",encoding="utf-8") as s:
    json.dump(papers,s,indent=2)

print("Preprocessing Completed")
print("Saved as: data/arxiv_cs_clean.json")




