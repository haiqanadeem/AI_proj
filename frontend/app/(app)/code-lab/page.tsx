"use client";

import { useEffect, useState, useRef } from "react";
import { CodeEditor } from "@/components/code/CodeEditor";
import { executeCode, analyzeCode } from "@/services/endpoints/code";
import { useVoice } from "@/contexts/VoiceContext";

export default function CodeLabPage() {
  const [code, setCode] = useState("# Write your Python code here\nprint('Hello World')");
  const [output, setOutput] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [analysis, setAnalysis] = useState("");
  const [running, setRunning] = useState(false);

  const { speak, setPageActions } = useVoice();

  useEffect(() => {
    document.title = "Code Lab — CodeSight AI";

    if (typeof window !== "undefined") {
      const pending = localStorage.getItem("pendingCodeExample");
      if (pending) {
        setCode(pending);
        localStorage.removeItem("pendingCodeExample");
        speak("Code example loaded into Code Lab. Press Run or say Submit Code to execute.", true);
      } else {
        speak("Code Lab. Write your Python code and say Submit Code to run.", true);
      }
    }
  }, [speak]);

  const handleRun = async () => {
    setRunning(true);
    setOutput("");
    setErrorMsg("");
    setAnalysis("");
    speak("Executing code...");

    try {
      const res = await executeCode(code);
      if (res.exit_code === 0) {
        setOutput(res.stdout);
        speak(`Execution successful. Output: ${res.stdout}`);
      } else {
        setOutput(res.stdout);
        setErrorMsg(res.stderr);
        speak("Execution failed. Analyzing error...");

        const analyzeRes = await analyzeCode(code, res.stderr);
        setAnalysis(analyzeRes.spoken_summary);
        speak(analyzeRes.spoken_summary);
      }
    } catch (e) {
      console.error(e);
      speak("An error occurred while executing the code.");
    } finally {
      setRunning(false);
    }
  };

  const codeRef = useRef(code);
  useEffect(() => {
    codeRef.current = code;
  }, [code]);

  useEffect(() => {
    setPageActions({
      submitCode: handleRun,
      readLesson: () => {
        const currentCode = codeRef.current;
        if (currentCode && currentCode.trim()) {
          speak("Here is the code in your editor:");
          speak(currentCode);
        } else {
          speak("Your code editor is empty.");
        }
      }
    });
  }, [handleRun, setPageActions, speak]);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">
      <div className="flex flex-col">
        <h1 className="text-2xl font-bold mb-4">Code Lab</h1>
        <CodeEditor
          initialCode={code}
          onChange={setCode}
          onRun={handleRun}
        />
      </div>
      <div className="flex flex-col gap-6 pt-12">
        <div className="p-4 border border-border rounded-lg shadow-sm bg-card h-64 overflow-y-auto">
          <h2 className="font-bold mb-2">Output</h2>
          {running ? (
            <div className="animate-pulse">Running...</div>
          ) : (
            <>
              {output && <pre className="font-mono text-sm whitespace-pre-wrap mb-2">{output}</pre>}
              {errorMsg && <pre className="font-mono text-sm whitespace-pre-wrap text-destructive">{errorMsg}</pre>}
              {!output && !errorMsg && <p className="text-muted-foreground text-sm italic">No output yet.</p>}
            </>
          )}
        </div>

        {(analysis || errorMsg) && (
          <div className="p-4 border border-destructive rounded-lg shadow-sm bg-destructive/10 text-destructive h-48 overflow-y-auto">
            <h2 className="font-bold mb-2">Analysis & Fixes</h2>
            <p className="text-sm whitespace-pre-wrap">{analysis || "Wait, checking for fixes..."}</p>
          </div>
        )}
      </div>
    </div>
  );
}
