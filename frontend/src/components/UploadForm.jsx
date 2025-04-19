import React, { useState, useEffect } from 'react';
import { uploadResume, getJobData } from '../api/resumeAPI';
import '../index.css';

const UploadForm = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [company, setCompany] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [jobData, setJobData] = useState({});
  const [result, setResult] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const data = await getJobData();
      setJobData(data);
    };
    fetchData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!resumeFile || !jobTitle || !company) {
      alert('Please fill all fields and upload a resume');
      return;
    }

    const response = await uploadResume(resumeFile, jobTitle, company);
    setResult(response);
  };

  const companyOptions = Object.keys(jobData);
  const jobOptions = company ? Object.keys(jobData[company] || {}) : [];

  return (
    <div className="upload-form">
      <h2>Smart Resume Analyzer</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={(e) => setResumeFile(e.target.files[0])}
        />

        <select value={company} onChange={(e) => {
          setCompany(e.target.value);
          setJobTitle('');
        }}>
          <option value="">Select Company</option>
          {companyOptions.map((comp) => (
            <option key={comp} value={comp}>{comp}</option>
          ))}
        </select>

        <select value={jobTitle} onChange={(e) => setJobTitle(e.target.value)} disabled={!company}>
          <option value="">Select Job Title</option>
          {jobOptions.map((title) => (
            <option key={title} value={title}>{title}</option>
          ))}
        </select>

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
