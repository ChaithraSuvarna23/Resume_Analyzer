import json
from flask import Blueprint, request, jsonify
from .utils import extract_text_from_resume, extract_details, match_job_description
import os
import traceback

analyzer_blueprint = Blueprint('analyzer', __name__)

@analyzer_blueprint.route('/api/analyze', methods=['POST'])
def analyze_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400

        resume_file = request.files['resume']
        job_title = request.form.get('job_title')
        company = request.form.get('company')

        print(f"Received job_title={job_title}, company={company}, filename={resume_file.filename}")

        if not job_title or not company:
            return jsonify({'error': 'Missing job title or company'}), 400

        # Save uploaded file
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        file_path = os.path.join('uploads', resume_file.filename)
        resume_file.save(file_path)

        # Process resume
        resume_text = extract_text_from_resume(file_path)
        if isinstance(resume_text, dict):
            resume_text = str(resume_text)
        details = extract_details(resume_text)
        score, suggestions = match_job_description(details, job_title, company)

        return jsonify({
            'text': resume_text,
            'details': details,
            'score': score,
            'suggestions': suggestions
        })

    except Exception as e:
        print("🔥 Error during /api/analyze")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@analyzer_blueprint.route('/api/job_data', methods=['GET'])
def get_job_data():
    try:
        json_path = os.path.join(os.path.dirname(__file__), '..', 'job_descriptions.json')
        with open(json_path, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': 'Could not load job data', 'details': str(e)}), 500
