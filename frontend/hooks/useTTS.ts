import { useCallback, useRef, useState, useEffect } from "react";

export function useTTS() {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const synthRef = useRef<SpeechSynthesis | null>(null);
  const queueRef = useRef<string[]>([]);
  const lastUtteranceRef = useRef<string>("");
  const isSpeakingRef = useRef(false);
  const activeUtteranceRef = useRef<SpeechSynthesisUtterance | null>(null);
  
  const lastSpokenTextRef = useRef<string>("");
  const lastSpokenTimeRef = useRef<number>(0);

  useEffect(() => {
    if (typeof window !== "undefined") {
      synthRef.current = window.speechSynthesis;
    }
  }, []);

  const speakNext = useCallback(() => {
    if (!synthRef.current || queueRef.current.length === 0) {
      setTimeout(() => {
        setIsSpeaking(false);
        isSpeakingRef.current = false;
      }, 250); // debounce
      return;
    }
    const text = queueRef.current.shift()!;
    lastUtteranceRef.current = text;
    
    const utterance = new SpeechSynthesisUtterance(text);
    activeUtteranceRef.current = utterance; // Prevent garbage collection
    
    utterance.onend = () => {
      activeUtteranceRef.current = null;
      speakNext();
    };
    
    utterance.onerror = () => {
      activeUtteranceRef.current = null;
      speakNext();
    };

    setIsSpeaking(true);
    isSpeakingRef.current = true;
    synthRef.current.speak(utterance);
  }, []);

  const speak = useCallback((text: string, clearFirst: boolean = false) => {
    if (clearFirst && synthRef.current) {
      synthRef.current.cancel();
      queueRef.current = [];
      setIsSpeaking(false);
      isSpeakingRef.current = false;
      activeUtteranceRef.current = null;
      lastSpokenTextRef.current = "";
      lastSpokenTimeRef.current = 0;
    }

    const now = Date.now();
    // Deduplicate exact same text if triggered within 1000ms (fixes React StrictMode double-fire)
    if (lastSpokenTextRef.current === text && (now - lastSpokenTimeRef.current) < 1000) {
      return;
    }
    lastSpokenTextRef.current = text;
    lastSpokenTimeRef.current = now;

    queueRef.current.push(text);
    if (!isSpeakingRef.current) {
      speakNext();
    }
  }, [speakNext]);

  const stopSpeaking = useCallback(() => {
    if (synthRef.current) {
      synthRef.current.cancel();
      queueRef.current = [];
      setIsSpeaking(false);
      isSpeakingRef.current = false;
      activeUtteranceRef.current = null;
    }
  }, []);

  const repeatLast = useCallback(() => {
    if (lastUtteranceRef.current) {
      // Bypass deduplication timestamp for manual repeat
      lastSpokenTimeRef.current = 0; 
      speak(lastUtteranceRef.current);
    }
  }, [speak]);

  return { speak, stopSpeaking, isSpeaking, repeatLast };
}
