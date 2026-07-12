import { useState } from "react";

export function ChatInput({ onSend, disabled }: { onSend: (msg: string) => void, disabled: boolean }) {
  const [msg, setMsg] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (msg.trim() && !disabled) {
      onSend(msg.trim());
      setMsg("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={msg}
        onChange={e => setMsg(e.target.value)}
        disabled={disabled}
        className="flex-grow p-3 rounded-lg border border-input bg-background focus:outline-none focus:ring-2 focus:ring-primary disabled:opacity-50"
        placeholder="Ask a question or say it via Voice..."
      />
      <button 
        type="submit" 
        disabled={disabled || !msg.trim()}
        className="px-6 py-3 bg-primary text-primary-foreground font-bold rounded-lg focus:outline-none focus:ring-2 focus:ring-accent disabled:opacity-50"
      >
        Send
      </button>
    </form>
  );
}
