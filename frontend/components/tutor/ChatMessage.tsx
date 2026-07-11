export function ChatMessage({ role, content }: { role: "user" | "tutor", content: string }) {
  const isUser = role === "user";
  return (
    <div className={`flex w-full ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div className={`max-w-[80%] rounded-lg p-4 ${isUser ? "bg-primary text-primary-foreground" : "bg-muted text-foreground border border-border"}`}>
        <p className="whitespace-pre-wrap">{content}</p>
      </div>
    </div>
  );
}
