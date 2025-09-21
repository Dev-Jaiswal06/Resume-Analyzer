import React, { useState } from "react";
import axios from "axios";

function ResumeUploader() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await axios.post("http://localhost:8000/upload_resume/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    setResult(res.data);
  };

  return (
    <div>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Analyze Resume</button>
      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>Resume Score: {result.resume_score}/10</h3>
          <p><b>Summary:</b> {result.summary}</p>
          <p><b>Keywords:</b> {result.keywords.join(", ")}</p>
          <pre>{result.extracted_text}</pre>
        </div>
      )}
    </div>
  );
}

export default ResumeUploader;
