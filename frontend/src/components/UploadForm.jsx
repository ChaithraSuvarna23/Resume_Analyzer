import React, { useState } from 'react';
import { uploadResume } from '../api/resumeAPI';
import '../index.css';

const UploadForm = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobTitle, setJobTitle] = useState('');
  const [company, setCompany] = useState('');
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!resumeFile || !jobTitle || !company) {
      alert('Please fill all fields and upload a resume');
      return;
    }

    const response = await uploadResume(resumeFile, jobTitle, company);
    setResult(response);
  };

  return (
    <div className="upload-form">
      <h2>Smart Resume Analyzer</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={(e) => setResumeFile(e.target.files[0])}
        />
        <input
          type="text"
          placeholder="Job Title"
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
        />
        <input
          type="text"
          placeholder="Company"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
        />
        <button type="submit">Analyze</button>
      </form>

      {result && (
        <div className="result-box">
          <h3>Analysis Result</h3>
          <p><strong>Score:</strong> {result.score}</p>
          <p><strong>Suggestions:</strong></p>
          <ul>
            {result.suggestions?.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default UploadForm;
