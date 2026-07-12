import { useCallback, useRef, useState, useEffect } from "react";
import { transcribeAudio, classifyIntent } from "../services/endpoints/voice";
import { IntentResponse } from "../types/api";

export function useVoiceRecognition() {
  const [isMediaRecorderSupported, setIsMediaRecorderSupported] = useState(true);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const speechRecRef = useRef<any>(null);
  const resolveCaptureRef = useRef<((value: { blob: Blob | null, text: string | null }) => void) | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined" && !navigator.mediaDevices?.getUserMedia) {
      setIsMediaRecorderSupported(false);
    }
  }, []);

  const captureCommand = useCallback((onInterim?: (text: string) => void): Promise<{ blob: Blob | null, text: string | null }> => {
    return new Promise(async (resolve, reject) => {
      resolveCaptureRef.current = resolve;

      const startMediaRecorderFallback = async () => {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          const recorder = new MediaRecorder(stream);
          mediaRecorderRef.current = recorder;
          let chunks: Blob[] = [];

          recorder.ondataavailable = (e) => {
            if (e.data.size > 0) chunks.push(e.data);
          };

          recorder.onstop = () => {
            const audioBlob = new Blob(chunks, { type: 'audio/webm' });
            stream.getTracks().forEach(track => track.stop());
            if (resolveCaptureRef.current) {
              resolveCaptureRef.current({ blob: audioBlob, text: null });
              resolveCaptureRef.current = null;
            }
          };

          recorder.start();

          setTimeout(() => {
            if (recorder.state === "recording") recorder.stop();
          }, 5000); // reduced from 7 to 5 seconds for better UX if fallback is hit
        } catch (err) {
          reject(err);
        }
      };

      // Try to use native SpeechRecognition first for real-time text and fast response
      const SpeechRec = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRec) {
        try {
          const recognizer = new SpeechRec();
          speechRecRef.current = recognizer;
          recognizer.continuous = false;
          recognizer.interimResults = true;
          recognizer.lang = "en-US";

          let finalStr = "";
          let fallbackTriggered = false;

          recognizer.onresult = (e: any) => {
            let interimStr = "";
            for (let i = e.resultIndex; i < e.results.length; ++i) {
              if (e.results[i].isFinal) finalStr += e.results[i][0].transcript;
              else interimStr += e.results[i][0].transcript;
            }
            if (onInterim) onInterim((finalStr + " " + interimStr).trim());
          };

          recognizer.onend = () => {
            if (fallbackTriggered) return;

            if (resolveCaptureRef.current) {
              resolveCaptureRef.current({ blob: null, text: finalStr.trim() });
              resolveCaptureRef.current = null;
            }
          };

          recognizer.onerror = (e: any) => {
            if (e.error === 'no-speech') {
              if (resolveCaptureRef.current) {
                resolveCaptureRef.current({ blob: null, text: "" });
                resolveCaptureRef.current = null;
              }
            } else if (e.error === 'not-allowed') {
              console.warn("SpeechRec not-allowed, falling back to MediaRecorder");
              fallbackTriggered = true;
              startMediaRecorderFallback();
            } else {
              console.warn("SpeechRec error, falling back to MediaRecorder:", e.error);
              fallbackTriggered = true;
              startMediaRecorderFallback();
            }
          };

          recognizer.start();
          return;
        } catch (e) {
          console.error("SpeechRec failed to initialize, falling back to MediaRecorder", e);
          startMediaRecorderFallback();
          return;
        }
      }

      startMediaRecorderFallback();
    });
  }, []);

  const stopCaptureAndWait = useCallback((): Promise<void> => {
    return new Promise((resolve) => {
      if (speechRecRef.current) {
        try { speechRecRef.current.stop(); } catch (e) { }
      }
      if (!mediaRecorderRef.current || mediaRecorderRef.current.state === "inactive") {
        resolve();
        return;
      }

      const oldResolve = resolveCaptureRef.current;
      resolveCaptureRef.current = (res) => {
        if (oldResolve) oldResolve(res);
        resolve();
      };

      mediaRecorderRef.current.stop();
    });
  }, []);

  const processCommand = useCallback(async (input: { blob: Blob | null, text: string | null }): Promise<IntentResponse> => {
    let transcriptToClassify = input.text;

    // If we don't have text (fallback was used), transcribe the blob via backend
    if (!transcriptToClassify && input.blob) {
      const transcribeRes = await transcribeAudio(input.blob);
      if (!transcribeRes.transcript) {
        throw new Error("No transcript detected");
      }
      transcriptToClassify = transcribeRes.transcript;
    }

    if (!transcriptToClassify) {
      throw new Error("Empty transcript");
    }

    const intentRes = await classifyIntent(transcriptToClassify);
    return intentRes;
  }, []);

  return { isMediaRecorderSupported, captureCommand, stopCaptureAndWait, processCommand };
}
