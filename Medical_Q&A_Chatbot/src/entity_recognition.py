# This Rule Based  File Is Created For Replying In Proper Seqeunce 
# It Is Basically Rule-Based  Medical Entity Recongition For Our Dataset

DISEASES = [
    "leukemia",
    "cancer",
    "diabetes",
    "asthma",
    "arthritis",
    "tuberculosis",
    "guillain-barré syndrome",
    "gaucher disease",
    "krabbe disease"
]

SYMPTOMS = [
    "fever",
    "fatigue",
    "bleeding",
    "pain",
    "cough",
    "weight loss",
    "night sweats",
    "headache",
    "nausea"
]

TREATMENTS = [
    "chemotherapy",
    "radiation",
    "radiation therapy",
    "surgery",
    "stem cell transplant",
    "medication",
    "antibiotics",
    "therapy"
]


def extract_entities(text: str) -> dict:
    """
    Extract Basic medical entities from input text using keyword matching.
    Returns a dictionary with diseases, symptoms, Treatments.
    """

    text = text.lower()

    entities = {
        "Diseases" : [],
        "Symptoms" : [],
        "Treatments" : []
    }

    for disease in DISEASES:
        if disease in text:
            entities["Diseases"].append(disease)

    for symptom in SYMPTOMS:
        if symptom in text:
            entities["Symptoms"].append(symptom)

    for treatment in TREATMENTS:
        if treatment in text:
            entities["Treatments"].append(treatment)


    return entities



