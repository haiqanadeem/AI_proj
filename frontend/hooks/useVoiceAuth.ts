"use client";

import { useState, useCallback, useEffect, useRef } from "react";
import { useAuth } from "../contexts/AuthContext";

type VoiceAuthState = "IDLE" | "AWAITING_EMAIL" | "CONFIRMING_EMAIL" | "AWAITING_PASSWORD" | "CONFIRMING_PASSWORD" | "SUBMITTING" | "DONE" | "ERROR" | "UNAVAILABLE";

export function useVoiceAuth() {
  const [state, setState] = useState<VoiceAuthState>("IDLE");
  const [email, setEmail] = useState("");
  const { login } = useAuth();

  const recognitionRef = useRef<any>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      synthRef.current = window.speechSynthesis;
      const SpeechRec = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRec) {
        recognitionRef.current = new SpeechRec();
        recognitionRef.current.continuous = false;
        recognitionRef.current.interimResults = false;
        recognitionRef.current.lang = "en-US";
      } else {
        setState("UNAVAILABLE");
      }
    }
  }, []);

  const speak = useCallback((text: string, onEnd?: () => void) => {
    if (!synthRef.current) {
      if (onEnd) onEnd();
      return;
    }
    synthRef.current.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    if (onEnd) utterance.onend = onEnd;
    synthRef.current.speak(utterance);
  }, []);

  const captureSpeech = useCallback((): Promise<string> => {
    return new Promise((resolve, reject) => {
      if (!recognitionRef.current) {
        reject(new Error("SpeechRecognition not available"));
        return;
      }

      const recognition = recognitionRef.current;

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript.trim().toLowerCase();
        resolve(transcript);
      };

      recognition.onerror = (event: any) => {
        if (event.error === "not-allowed") {
          setState("UNAVAILABLE");
        }
        reject(new Error(event.error));
      };

      try {
        recognition.start();
      } catch (e) {
        reject(e);
      }
    });
  }, []);

  const submitLogin = useCallback(async (e: string, p: string) => {
    setState("SUBMITTING");
    speak("Logging in...");
    try {
      await login({ email: e, password: p });
      setState("DONE");
      speak("Login successful.");
    } catch (error) {
      setState("ERROR");
      speak("Invalid credentials, try again.", () => {
        setState("IDLE");
      });
    }
  }, [login, speak]);

  const requestPassword = useCallback((currentEmail: string) => {
    setState("AWAITING_PASSWORD");
    speak("Please say your password. Note: your password will be spoken aloud to confirm unless you add 'skip confirmation' at the end.", async () => {
      try {
        const transcript = await captureSpeech();
        const skipRequested = transcript.includes("skip confirmation");
        const parsedPassword = transcript.replace(/skip confirmation/g, "").replace(/\s+/g, "");

        if (skipRequested) {
          submitLogin(currentEmail, parsedPassword);
        } else {
          setState("CONFIRMING_PASSWORD");
          speak(`I heard ${parsedPassword}. Say yes or try again.`, async () => {
            const confirmation = await captureSpeech();
            if (confirmation.includes("yes") || confirmation.includes("correct") || confirmation.includes("yeah")) {
              submitLogin(currentEmail, parsedPassword);
            } else {
              requestPassword(currentEmail);
            }
          });
        }
      } catch (e) {
        speak("I didn't catch that. Please say your password again.", () => requestPassword(currentEmail));
      }
    });
  }, [captureSpeech, speak, submitLogin]);

  const requestEmail = useCallback(() => {
    setState("AWAITING_EMAIL");
    speak("Please say your email address", async () => {
      try {
        const transcript = await captureSpeech();
        const parsedEmail = transcript.replace(/\s+/g, "").replace(/at/g, "@").replace(/dot/g, ".");
        setEmail(parsedEmail);
        setState("CONFIRMING_EMAIL");

        speak(`I heard ${parsedEmail}. Is that correct? Say yes or try again.`, async () => {
          const confirmation = await captureSpeech();
          if (confirmation.includes("yes") || confirmation.includes("correct") || confirmation.includes("yeah")) {
            requestPassword(parsedEmail);
          } else {
            requestEmail();
          }
        });
      } catch (e) {
        speak("I didn't catch that. Please say your email address again.", requestEmail);
      }
    });
  }, [captureSpeech, speak, requestPassword]);

  const startVoiceLogin = useCallback(async () => {
    if (state === "UNAVAILABLE" || !recognitionRef.current) return;
    requestEmail();
  }, [state, requestEmail]);

  return { state, startVoiceLogin };
}
