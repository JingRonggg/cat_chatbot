"use client";

import { useState, useEffect, useRef } from "react";
import { ChatMessage } from "./chatMessage";
import chatCompletion from "./chatCompletion";

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [prompt, setPrompt] = useState("");
  const [username, setUsername] = useState("");
  const [user, setUser] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleUsernameSubmit = () => {
    setUser(username);
  };

  const handleSubmit = async () => {
    const currentPrompt = prompt;
    const updatedMessages = [...messages, { role: "user", message: prompt }];
    setMessages(updatedMessages);
    setPrompt("");
    setIsLoading(true);
    const response = await chatCompletion(currentPrompt, user);
    setIsLoading(false);
    setMessages([...updatedMessages, { role: "assistant", message: response.message_history }]);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="h-screen flex items-center justify-center flex-col gap-10 container mx-auto pl-4 pt-6 pr-4">
      {user ? (
        <>
          <div className="flex flex-col gap-3 h-[75%] overflow-scroll w-full">
            {messages.map((message, index) => (
              <div
                key={index}
                className={message.role === "user" ? "chat chat-start" : "chat chat-end"}
              >
                <div className="chat-bubble">
                  {message.message.includes("http") ? (
                    <img src={message.message.match(/https?:\/\/\S+/)[0]} alt="Cat" />
                  ) : (
                    <p>{message.message}</p>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="chat chat-end">
                <div className="chat-bubble">Loading...</div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <input
            type="text"
            className="input input-bordered w-full m-10"
            placeholder="Show me a picture of a cat"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={async (event) => {
              if (event.key === "Enter") {
                await handleSubmit();
              }
            }}
          />
        </>
      ) : (
        <div className="flex flex-col items-center gap-4">
          <input
            type="text"
            className="input input-bordered w-full m-10"
            placeholder="Enter your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                handleUsernameSubmit();
              }
            }}
          />
          <button className="btn btn-primary" onClick={handleUsernameSubmit}>
            Submit
          </button>
        </div>
      )}
    </div>
  );
}