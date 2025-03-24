import React, { useState } from 'react';
import axios from 'axios';
import './UploadTranscript.css';

function UploadTranscript() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await axios.post("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setStatus(res.data.message);
    } catch (err) {
      setStatus("Upload failed: " + err.message);
    }
    setLoading(false);
  };

  return (
    <div className="upload-container">
      <h2>Upload Transcript</h2>
      <input type="file" onChange={handleFileChange} className="file-input" />
      <button onClick={handleUpload} className="upload-button">
        Upload
      </button>
      {loading && (
        <div className="loading-container">
          <div className="spinner"></div>
          <div className="loading-text">Uploading...</div>
        </div>
      )}
      <p className="status-message">{status}</p>
    </div>
  );
}

export default UploadTranscript;
