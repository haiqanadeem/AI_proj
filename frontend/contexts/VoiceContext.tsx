"use client";

import React, { createContext, useContext, useState, useCallback, useEffect, useRef } from "react";
import { VoiceState } from "../lib/constants";
// import { useSpeechRecognition } from "../hooks/useSpeechRecognition";
import { useTTS } from "../hooks/useTTS";
import { useVoiceRecognition } from "../hooks/useVoiceRecognition";
import { useVoiceCommands } from "../hooks/useVoiceCommands";
import { createVoiceLog } from "../services/endpoints/voiceLogs";
import { announceToScreenReader } from "../lib/accessibility";
import { useAuth } from "./AuthContext";
import { IntentResponse } from "../types/api";

interface VoiceContextType {
  voiceState: VoiceState;
  isSpeaking: boolean;
  interimTranscript: string;
  startManualCapture: () => void;
  speak: (text: string, clearFirst?: boolean) => void;
  stopSpeaking: () => void;
  voices: SpeechSynthesisVoice[];
  preferredVoice: SpeechSynthesisVoice | null;
  changeVoice: (voiceURI: string) => void;
  setPageActions: (actions: {
    readLesson?: () => void;
    startQuiz?: () => void;
    submitCode?: () => void;
    nextLesson?: () => void;
    prevLesson?: () => void;
  }) => void;
}

const VoiceContext = createContext<VoiceContextType | undefined>(undefined);

const playBeep = () => {
  try {
    const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    oscillator.type = 'sine';
    oscillator.frequency.value = 800;
    gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
    oscillator.start(audioCtx.currentTime);
    oscillator.stop(audioCtx.currentTime + 0.15);
  } catch (e) { }
};

export function VoiceProvider({ children }: { children: React.ReactNode }) {
  const [voiceState, setVoiceState] = useState<VoiceState>(VoiceState.AMBIENT_UNAVAILABLE);
  const [interimTranscript, setInterimTranscript] = useState<string>("");
  const voiceStateRef = useRef<VoiceState>(VoiceState.AMBIENT_UNAVAILABLE);
  const hasInitializedRef = useRef(false);
  const { logout } = useAuth();

  const pageActionsRef = useRef<{
    readLesson?: () => void;
    startQuiz?: () => void;
    submitCode?: () => void;
    nextLesson?: () => void;
    prevLesson?: () => void;
  }>({});

  const updateVoiceState = useCallback((newState: VoiceState) => {
    voiceStateRef.current = newState;
    setVoiceState(newState);
  }, []);

  const { speak, stopSpeaking, isSpeaking, repeatLast, voices, preferredVoice, changeVoice } = useTTS();
  const { handleIntent } = useVoiceCommands();
  const { isMediaRecorderSupported, captureCommand, stopCaptureAndWait, processCommand } = useVoiceRecognition();

  const setPageActions = useCallback((actions: any) => {
    pageActionsRef.current = actions;
  }, []);

  const returnToAmbient = useCallback(() => {
    const current = voiceStateRef.current;
    if (current === VoiceState.VOICE_UNAVAILABLE || current === VoiceState.MIC_DENIED) return;
    updateVoiceState(VoiceState.AMBIENT_UNAVAILABLE);
  }, [updateVoiceState]);

  useEffect(() => {
    if (typeof window === "undefined" || hasInitializedRef.current) return;
    hasInitializedRef.current = true;

    if (!isMediaRecorderSupported) {
      updateVoiceState(VoiceState.VOICE_UNAVAILABLE);
    } else {
      updateVoiceState(VoiceState.AMBIENT_UNAVAILABLE);
    }
  }, [isMediaRecorderSupported, updateVoiceState]);

  const startManualCapture = useCallback(async () => {
    const current = voiceStateRef.current;
    if (current === VoiceState.VOICE_UNAVAILABLE) return;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      stream.getTracks().forEach(t => t.stop());
    } catch (e) {
      console.error("Microphone permission denied", e);
      updateVoiceState(VoiceState.MIC_DENIED);
      return;
    }

    stopSpeaking();
    playBeep();
    updateVoiceState(VoiceState.ACTIVE_LISTENING);
    setInterimTranscript("");
    announceToScreenReader("Listening for your command...");

    try {
      const startTime = Date.now();
      const captureResult = await captureCommand((text) => {
        setInterimTranscript(text);
      });

      updateVoiceState(VoiceState.PROCESSING);
      announceToScreenReader("Processing your command...");

      try {
        const intentRes = await processCommand(captureResult);
        const executionTime = Date.now() - startTime;

        createVoiceLog(intentRes.raw_command, intentRes.intent, intentRes.confidence, executionTime).catch(console.error);

        updateVoiceState(VoiceState.RESPONDING);
        setInterimTranscript("");

        if (intentRes.confidence < 0.6) {
          speak("I didn't quite catch that. Please say it again.");
          setTimeout(returnToAmbient, 3000);
          return;
        }

        handleIntent(
          intentRes,
          pageActionsRef.current.readLesson || (() => speak("Reading lesson is not available here.")),
          () => { stopSpeaking(); returnToAmbient(); },
          pageActionsRef.current.startQuiz || (() => speak("Quiz is not available here.")),
          pageActionsRef.current.submitCode || (() => speak("Code lab is not available here.")),
          () => speak("Use Alt plus V to toggle voice, or press Alt plus H for shortcuts."),
          repeatLast,
          logout,
          pageActionsRef.current.nextLesson || (() => speak("You must be inside a lesson to go to the next lesson.")),
          pageActionsRef.current.prevLesson || (() => speak("You must be inside a lesson to go to the previous lesson.")),
          speak
        );

        setTimeout(returnToAmbient, 4000);

      } catch (e) {
        speak("I couldn't process that command.");
        setTimeout(returnToAmbient, 2000);
      }
    } catch (e) {
      console.error(e);
      speak("Microphone access failed.");
      updateVoiceState(VoiceState.MIC_DENIED);
    }
  }, [stopSpeaking, captureCommand, processCommand, handleIntent, speak, returnToAmbient, repeatLast, logout, updateVoiceState]);

  const startManualCaptureRef = useRef(startManualCapture);
  startManualCaptureRef.current = startManualCapture;

  return (
    <VoiceContext.Provider
      value={{
        voiceState,
        isSpeaking,
        interimTranscript,
        startManualCapture,
        speak,
        stopSpeaking,
        voices,
        preferredVoice,
        changeVoice,
        setPageActions
      }}
    >
      {children}
    </VoiceContext.Provider>
  );
}

export function useVoice() {
  const context = useContext(VoiceContext);
  if (context === undefined) {
    throw new Error("useVoice must be used within a VoiceProvider");
  }
  return context;
}

