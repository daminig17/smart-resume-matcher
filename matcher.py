from PyPDF2 import PdfReader

IT_SECTIONS = {
    "Data Science": ["python", "pandas", "machine learning", "tensorflow", "sql"],
    "Web Development": ["html", "css", "javascript", "react", "flask", "django"],
    "Cloud Computing": ["aws", "azure", "gcp", "docker", "kubernetes"],
    "Cybersecurity": ["security", "network", "encryption", "firewall", "hacking"],
    "AI/ML": ["deep learning", "transformers", "pytorch", "nlp", "computer vision"]
}

def parse_resume(path):
    text = ""
    if path.endswith(".txt"):
        with open(path, "r", errors="ignore") as f:
            text = f.read().lower()
    elif path.endswith(".pdf"):
        try:
            reader = PdfReader(path)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text().lower()
        except:
            pass
    return text

def match_resume(path):
    text = parse_resume(path)
    if not text:
        return None, 0, [], ["Could not parse resume. Try PDF/Text only."]

    best_section, best_score, matched_skills, missing_skills = None, 0, [], []

    for section, keywords in IT_SECTIONS.items():
        found = [k for k in keywords if k in text]
        not_found = [k for k in keywords if k not in text]
        score = len(found)

        if score > best_score:
            best_score = score
            best_section = section
            matched_skills = found
            missing_skills = not_found

    if best_section and best_score > 0:
        confidence = round(best_score / len(IT_SECTIONS[best_section]), 2)
        return best_section, confidence, matched_skills, missing_skills
    else:
        return None, 0, [], ["No relevant IT skills found. Add programming & tools."]
