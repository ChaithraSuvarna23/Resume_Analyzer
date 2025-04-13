import PyPDF2
import docx
import os
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_resume(file_path):
    """
    Extracts text from PDF or DOCX file.
    """
    text = ''
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ''
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + '\n'
    return text

def extract_details(text):
    """
    Extracts skills, years of experience, and email from resume text.
    """
    skills = re.findall(r"\b(Python|Java|SQL|Excel|Pandas|Machine Learning|Deep Learning|Tableau)\b", text, re.IGNORECASE)
    experience = re.findall(r'(\d+)\+?\s+years?', text, re.IGNORECASE)
    email = re.findall(r'[\w\.-]+@[\w\.-]+', text)

    return {
        'email': email[0] if email else 'Not found',
        'skills': list(set(skills)),
        'experience': experience[0] if experience else 'Not found'
    }

def match_job_description(resume_text, job_title, company):
    """
    Matches the resume text with the job description based on cosine similarity.
    Returns a similarity score and suggestions.
    """
    # Ensure resume_text and job_description are strings
    if not isinstance(resume_text, str):
        raise ValueError("The resume text is not a valid string.")
    
    json_path = os.path.join(os.path.dirname(__file__), '..', 'job_descriptions.json')

    try:
        with open(json_path, 'r') as f:
            jd_data = json.load(f)
    except FileNotFoundError:
        return 0, ['Job description file not found.']

    company_data = jd_data.get(company, {})
    job_data = company_data.get(job_title, {})

    # Ensure the job description data is valid
    if not job_data:
        return 0, ['Job description not found for the selected company/title.']

    skills = job_data.get('skills', [])
    experience_keywords = job_data.get('experience_keywords', [])

    # Combine skills and experience keywords into one text block
    job_description = ' '.join(skills + experience_keywords)

    # Initialize the vectorizer and calculate cosine similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    score = round(similarity * 100)

    # Generate suggestions based on score
    suggestions = []
    if score < 60:
        suggestions.append("Include more keywords relevant to the job.")
        suggestions.append("Improve alignment with the job description.")
    elif score < 80:
        suggestions.append("Looks good, but could be optimized further.")
    else:
        suggestions.append("Great match!")

    return score, suggestions
