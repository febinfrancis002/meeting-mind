import React, { useState } from 'react';
import './App.css';
import UploadTranscript from './components/UploadTranscript';
import ChatTranscripts from './components/ChatTranscripts';

function App() {
  const [activeTab, setActiveTab] = useState("upload");

  return (
    <div className="app-container">
      <div className="content-container">
        <nav className="sidebar">
          <div className="brand">
            <h2>Meeting Mind</h2>
          </div>
          <ul>
            <li
              className={activeTab === "upload" ? "active" : ""}
              onClick={() => setActiveTab("upload")}
            >
              Upload Transcript
            </li>
            <li
              className={activeTab === "chat" ? "active" : ""}
              onClick={() => setActiveTab("chat")}
            >
              Chat with Transcripts
            </li>
          </ul>
        </nav>
        <main className="main-content">
          {activeTab === "upload" && <UploadTranscript />}
          {activeTab === "chat" && <ChatTranscripts />}
        </main>
      </div>
    </div>
  );
}

export default App;
