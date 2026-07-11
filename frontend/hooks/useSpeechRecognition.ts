import { useEffect, useRef, useState, useCallback } from "react";
import { GREETINGS } from "../lib/constants";

export function useSpeechRecognition(onGreetingDetected: () => void, onMicDenied: () => void) {
  const [isSupported, setIsSupported] = useState(true);
  const recognitionRef = useRef<any>(null);
  const shouldBeRunningRef = useRef(false);
  const restartTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const restartAttemptsRef = useRef(0);
  const resolveStopRef = useRef<((value: void | PromiseLike<void>) => void) | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRec = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRec) {
        recognitionRef.current = new SpeechRec();
        recognitionRef.current.continuous = true;
        recognitionRef.current.interimResults = true;
        recognitionRef.current.lang = "en-US";
        
        recognitionRef.current.onresult = (event: any) => {
          for (let i = event.resultIndex; i < event.results.length; ++i) {
             const transcript = event.results[i][0].transcript.trim().toLowerCase();
             
             if (event.results[i].isFinal) {
                if (GREETINGS.PRIMARY.some(g => transcript.includes(g))) {
                    onGreetingDetected();
                    return;
                }
             }
             
             const words = transcript.split(/\s+/).length;
             if (words >= 2 && GREETINGS.SECONDARY.some(g => transcript.includes(g))) {
                 onGreetingDetected();
                 return;
             }
          }
        };

        recognitionRef.current.onend = () => {
          if (resolveStopRef.current) {
            resolveStopRef.current();
            resolveStopRef.current = null;
          } else if (shouldBeRunningRef.current) {
            const backoff = Math.min(1000 * Math.pow(2, restartAttemptsRef.current), 30000);
            console.log(`Ambient listening stopped unexpectedly. Restarting in ${backoff}ms...`);
            restartTimeoutRef.current = setTimeout(() => {
                restartAttemptsRef.current++;
                try {
                    recognitionRef.current?.start();
                } catch(e) {}
            }, backoff);
          }
        };

        recognitionRef.current.onerror = (event: any) => {
           if (event.error === 'not-allowed') {
              setIsSupported(false);
              shouldBeRunningRef.current = false;
              onMicDenied();
           }
        };
      } else {
        setIsSupported(false);
      }
    }
    return () => {
        shouldBeRunningRef.current = false;
        if (restartTimeoutRef.current) clearTimeout(restartTimeoutRef.current);
        if (recognitionRef.current) {
           try { recognitionRef.current.stop(); } catch(e){}
        }
    };
  }, [onGreetingDetected, onMicDenied]);

  const startAmbient = useCallback(() => {
    if (!recognitionRef.current) return;
    shouldBeRunningRef.current = true;
    restartAttemptsRef.current = 0;
    try {
        recognitionRef.current.start();
    } catch(e) {}
  }, []);

  const stopAmbientAndWait = useCallback((): Promise<void> => {
    return new Promise((resolve) => {
      if (!recognitionRef.current) {
          resolve();
          return;
      }
      shouldBeRunningRef.current = false;
      if (restartTimeoutRef.current) clearTimeout(restartTimeoutRef.current);
      
      resolveStopRef.current = resolve;
      
      try {
          recognitionRef.current.stop();
      } catch (e) {
          resolve(); 
      }
    });
  }, []);

  return { isSupported, startAmbient, stopAmbientAndWait };
}
