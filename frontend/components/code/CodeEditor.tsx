import { useState, useRef, useEffect } from "react";

export function CodeEditor({ 
  initialCode, 
  onChange, 
  onRun 
}: { 
  initialCode: string; 
  onChange: (code: string) => void;
  onRun: () => void;
}) {
  const [code, setCode] = useState(initialCode);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    setCode(initialCode);
  }, [initialCode]);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setCode(e.target.value);
    onChange(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const start = e.currentTarget.selectionStart;
      const end = e.currentTarget.selectionEnd;
      const newCode = code.substring(0, start) + "    " + code.substring(end);
      setCode(newCode);
      onChange(newCode);
      setTimeout(() => {
        if (textareaRef.current) {
          textareaRef.current.selectionStart = textareaRef.current.selectionEnd = start + 4;
        }
      }, 0);
    }
  };

  return (
    <div className="flex flex-col border border-border rounded-lg overflow-hidden focus-within:ring-2 focus-within:ring-primary shadow-sm h-[400px]">
      <div className="bg-muted p-2 flex justify-between items-center border-b border-border">
        <span className="font-bold font-mono text-sm text-muted-foreground">main.py</span>
        <button 
          onClick={onRun}
          className="px-4 py-1 bg-primary text-primary-foreground font-bold rounded focus:outline-none focus:ring-2 focus:ring-accent text-sm"
          aria-label="Run code"
        >
          Run
        </button>
      </div>
      <textarea
        ref={textareaRef}
        value={code}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        className="flex-grow p-4 bg-background font-mono text-foreground focus:outline-none resize-none"
        aria-label="Code editor"
        spellCheck="false"
      />
    </div>
  );
}
