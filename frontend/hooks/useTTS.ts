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

  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);
  const [preferredVoice, setPreferredVoice] = useState<SpeechSynthesisVoice | null>(null);
  const preferredVoiceRef = useRef<SpeechSynthesisVoice | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      synthRef.current = window.speechSynthesis;
      
      const loadVoices = () => {
        const availableVoices = window.speechSynthesis.getVoices();
        setVoices(availableVoices);
        
        const savedVoiceURI = localStorage.getItem("codesight_preferred_voice");
        if (savedVoiceURI) {
          const match = availableVoices.find(v => v.voiceURI === savedVoiceURI);
          if (match) {
            setPreferredVoice(match);
            preferredVoiceRef.current = match;
          }
        }
      };

      loadVoices();
      if (window.speechSynthesis.onvoiceschanged !== undefined) {
        window.speechSynthesis.onvoiceschanged = loadVoices;
      }
    }
  }, []);

  const changeVoice = useCallback((voiceURI: string) => {
    const match = voices.find(v => v.voiceURI === voiceURI);
    if (match) {
      setPreferredVoice(match);
      preferredVoiceRef.current = match;
      localStorage.setItem("codesight_preferred_voice", match.voiceURI);
    }
  }, [voices]);

  const speakNext = useCallback(() => {
    if (!synthRef.current || queueRef.current.length === 0) {
      setTimeout(() => {
        setIsSpeaking(false);
        isSpeakingRef.current = false;
      }, 250);
      return;
    }
    const text = queueRef.current.shift()!;
    lastUtteranceRef.current = text;
    
    const utterance = new SpeechSynthesisUtterance(text);
    if (preferredVoiceRef.current) {
      utterance.voice = preferredVoiceRef.current;
    }
    activeUtteranceRef.current = utterance;
    
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
      lastSpokenTimeRef.current = 0; 
      speak(lastUtteranceRef.current);
    }
  }, [speak]);

  return { speak, stopSpeaking, isSpeaking, repeatLast, voices, preferredVoice, changeVoice };
}
