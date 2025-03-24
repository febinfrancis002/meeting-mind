import React, { useState } from "react";
import axios from "axios";
import "./ChatTranscripts.css";

function ChatTranscripts() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {
    if (!message) return;
    // Add user's message to the chat log.
    const newChat = [...chat, { sender: "User", text: message }];
    setChat(newChat);
    try {
      // Note: we send the question using the key "question".
      const res = await axios.post("http://localhost:8000/chat", {
        question: message,
      });
      setChat([...newChat, { sender: "Bot", text: res.data.answer }]);
    } catch (err) {
      setChat([...newChat, { sender: "Bot", text: "Error: " + err.message }]);
    }
    setMessage("");
  };

  return (
    <div className="chat-container">
      <h2>Chat with Transcripts</h2>
      <div className="chat-window">
        {chat.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-message ${
              msg.sender === "User" ? "user-message" : "bot-message"
            }`}
          >
            <strong>{msg.sender}:</strong> {msg.text}
          </div>
        ))}
      </div>
      <div className="chat-input-container">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your question..."
          className="chat-input"
        />
        <button onClick={sendMessage} className="send-button">
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatTranscripts;
