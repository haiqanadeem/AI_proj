"use client";

import { useEffect, useState, useRef } from "react";
import { chatWithTutor } from "@/services/endpoints/tutor";
import { ChatMessage } from "@/components/tutor/ChatMessage";
import { ChatInput } from "@/components/tutor/ChatInput";
import { useVoice } from "@/contexts/VoiceContext";
import { v4 as uuidv4 } from "uuid";

interface Message {
  role: "user" | "tutor";
  content: string;
}

export default function TutorPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState("");
  const [loading, setLoading] = useState(false);
  const { speak, setPageActions } = useVoice();
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    document.title = "AI Tutor — CodeSight AI";
    setSessionId(uuidv4());
    setPageActions({});
    
    const initialMsg = "Hello! I am your CodeSight AI Tutor. What programming question can I help you with?";
    setMessages([{ role: "tutor", content: initialMsg }]);
    if (typeof window !== "undefined") {
        speak(initialMsg, true);
    }
  }, [setPageActions, speak]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (msg: string) => {
    setMessages(prev => [...prev, { role: "user", content: msg }]);
    setLoading(true);
    try {
      const response = await chatWithTutor(msg, sessionId);
      setMessages(prev => [...prev, { role: "tutor", content: response.response }]);
      speak(response.response);
    } catch (e) {
      console.error(e);
      speak("Sorry, I had trouble answering that.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] max-h-[800px] border border-border rounded-lg shadow-sm bg-card overflow-hidden">
      <div className="bg-muted p-4 border-b border-border">
        <h1 className="text-xl font-bold">AI Tutor</h1>
        <p className="text-sm text-muted-foreground">Ask questions via keyboard or voice.</p>
      </div>

      <div className="flex-grow overflow-y-auto p-4 flex flex-col">
        {messages.map((m, i) => (
          <ChatMessage key={i} role={m.role} content={m.content} />
        ))}
        {loading && (
          <div className="flex w-full justify-start mb-4">
            <div className="max-w-[80%] rounded-lg p-4 bg-muted text-foreground border border-border flex gap-2 items-center">
              <span className="w-2 h-2 rounded-full bg-primary animate-bounce"></span>
              <span className="w-2 h-2 rounded-full bg-primary animate-bounce delay-100"></span>
              <span className="w-2 h-2 rounded-full bg-primary animate-bounce delay-200"></span>
            </div>
          </div>
        )}
        <div ref={endRef} />
      </div>

      <div className="p-4 bg-background border-t border-border">
        <ChatInput onSend={handleSend} disabled={loading} />
      </div>
    </div>
  );
}
