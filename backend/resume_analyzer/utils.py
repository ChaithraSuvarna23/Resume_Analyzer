import pdfplumber
import docx
import os
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2.errors import PdfReadError


def extract_text_from_resume(file_path):
    text = ''
    if file_path.endswith('.pdf'):
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ''
        except Exception as e:
            print(f"❌ PDF extract error: {e}")
            raise ValueError("Could not read PDF. Try uploading a .docx instead.")
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + '\n'
    return text



def extract_details(text):
    """
    Extracts skills, CGPA, and email from resume text.
    """
    skills = re.findall(r"\b(Python|Java|SQL|Excel|Pandas|Machine Learning|Deep Learning|Tableau|C\+\+|C|React|Angular|HTML|CSS|Power BI|Cloud|ETL|Docker|Linux|Git|Node\.js|CI/CD|Kubernetes|AWS|Azure|GCP|Unix)\b", text, re.IGNORECASE)
    email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    cgpa_match = re.search(r'(CGPA|GPA)\s*[:\-]?\s*(\d+\.\d+)', text, re.IGNORECASE)
    if not cgpa_match:
        cgpa_match = re.search(r'(\d+\.\d+)\s*(CGPA|GPA)', text, re.IGNORECASE)

    return {
        'email': email[0] if email else 'Not found',
        'skills': list(set(skills)),
        'cgpa': float(cgpa_match.group(2)) if cgpa_match else 0.0
    }

def match_job_description(resume_details, job_title, company):
    """
    Matches resume details with job criteria (skills and CGPA).
    Returns a score and suggestions.
    """
    json_path = os.path.join(os.path.dirname(__file__), '..', 'job_descriptions.json')

    try:
        with open(json_path, 'r') as f:
            jd_data = json.load(f)
    except FileNotFoundError:
        return 0, ['Job description file not found.']

    company_data = jd_data.get(company, {})
    job_data = company_data.get(job_title, {})

    if not job_data:
        return 0, ['Job description not found for the selected company/title.']

    required_skills = set(map(str.lower, job_data.get('skills', [])))
    required_cgpa = job_data.get('cgpa', 0.0)

    resume_skills = set(map(str.lower, resume_details.get('skills', [])))
    matched_skills = required_skills.intersection(resume_skills)

    skill_score = (len(matched_skills) / len(required_skills)) * 100 if required_skills else 0
    cgpa_score = 100 if resume_details.get('cgpa', 0) >= required_cgpa else 0

    total_score = round((skill_score * 0.7) + (cgpa_score * 0.3))

    suggestions = []
    if skill_score < 70:
        suggestions.append("Consider adding more job-relevant skills.")
    if cgpa_score == 0:
        suggestions.append(f"Required CGPA is {required_cgpa}, but resume shows lower.")
    if not suggestions:
        suggestions.append("Great match!")

    return total_score, suggestions
