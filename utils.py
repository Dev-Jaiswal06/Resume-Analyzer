import spacy

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return list(set(keywords))

def rate_resume(text):
    score = 0
    if "Experience" in text: score += 2
    if "Education" in text: score += 2
    if "Skills" in text: score += 2
    if len(text) > 300: score += 2
    if "Project" in text: score += 2
    return score
