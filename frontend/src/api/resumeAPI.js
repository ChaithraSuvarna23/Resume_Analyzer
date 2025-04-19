export const uploadResume = async (file, jobTitle, company) => {
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_title', jobTitle);
    formData.append('company', company);
  
    try {
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        body: formData,
      });
  
      if (!response.ok) throw new Error('Server error');
  
      return await response.json();
    } catch (error) {
      console.error('Error uploading resume:', error);
      return { score: 0, suggestions: ['Something went wrong.'] };
    }
  };
  
  export const getJobData = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/job_data');
      if (!response.ok) throw new Error('Failed to fetch job data');
      return await response.json();
    } catch (error) {
      console.error('Error fetching job data:', error);
      return {};
    }
  };