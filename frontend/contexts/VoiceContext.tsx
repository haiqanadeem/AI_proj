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
  // page-specific action setters
  setPageActions: (actions: {
    readLesson?: () => void;
    startQuiz?: () => void;
    submitCode?: () => void;
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
        oscillator.frequency.value = 800; // 800 Hz beep
        gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime); // Low volume
        oscillator.start(audioCtx.currentTime);
        oscillator.stop(audioCtx.currentTime + 0.15); // 150ms beep
    } catch(e) {}
};

export function VoiceProvider({ children }: { children: React.ReactNode }) {
  const [voiceState, setVoiceState] = useState<VoiceState>(VoiceState.VOICE_UNAVAILABLE);
  const [interimTranscript, setInterimTranscript] = useState<string>("");
  const voiceStateRef = useRef<VoiceState>(VoiceState.VOICE_UNAVAILABLE);
  const hasInitializedRef = useRef(false);
  const { logout } = useAuth();

  const pageActionsRef = useRef<{
    readLesson?: () => void;
    startQuiz?: () => void;
    submitCode?: () => void;
  }>({});

  // Helper to update both state and ref in sync
  const updateVoiceState = useCallback((newState: VoiceState) => {
    voiceStateRef.current = newState;
    setVoiceState(newState);
  }, []);

  const { speak, stopSpeaking, isSpeaking, repeatLast } = useTTS();
  const { handleIntent } = useVoiceCommands();
  const { isMediaRecorderSupported, captureCommand, stopCaptureAndWait, processCommand } = useVoiceRecognition();

  const setPageActions = useCallback((actions: any) => {
    pageActionsRef.current = actions;
  }, []);

  const returnToAmbient = useCallback(() => {
    const current = voiceStateRef.current;
    if (current === VoiceState.VOICE_UNAVAILABLE || current === VoiceState.MIC_DENIED) return;
    updateVoiceState(VoiceState.VOICE_UNAVAILABLE); // Instead of ambient listening, just return to unavailable
    // if (current === VoiceState.AMBIENT_UNAVAILABLE) {
    //   updateVoiceState(VoiceState.AMBIENT_UNAVAILABLE);
    //   return;
    // }
    // updateVoiceState(VoiceState.AMBIENT_LISTENING);
    // startAmbientRef.current();
  }, [updateVoiceState]);

  /* Commenting out Ambient Listening for now
  const onGreetingDetected = useCallback(async () => {
    await stopAmbientRef.current();
    updateVoiceState(VoiceState.ACKNOWLEDGING);
    speak("Yes, I'm here. What's your call?");

    // Wait a moment for TTS to finish before capturing
    setTimeout(() => {
      startManualCaptureRef.current();
    }, 2000);
  }, [speak, updateVoiceState]);

  const onMicDenied = useCallback(() => {
    updateVoiceState(VoiceState.MIC_DENIED);
  }, [updateVoiceState]);

  const { isSupported: isAmbientSupported, startAmbient, stopAmbientAndWait } = useSpeechRecognition(onGreetingDetected, onMicDenied);

  // Stable refs for functions that need to be called from callbacks
  const startAmbientRef = useRef(startAmbient);
  startAmbientRef.current = startAmbient;
  const stopAmbientRef = useRef(stopAmbientAndWait);
  stopAmbientRef.current = stopAmbientAndWait;
  */

  // ONE-TIME initialization — no voiceState in deps
  useEffect(() => {
    if (typeof window === "undefined" || hasInitializedRef.current) return;
    hasInitializedRef.current = true;

    if (!isMediaRecorderSupported) {
      updateVoiceState(VoiceState.VOICE_UNAVAILABLE);
    } else {
      // With ambient off, just stay in unavailable/idle state
      updateVoiceState(VoiceState.VOICE_UNAVAILABLE); 
    }
  }, [isMediaRecorderSupported, updateVoiceState]);

  /* Commenting out Ambient Pause logic
  // Pause ambient ONLY when TTS is speaking AND we're actually in ambient mode
  useEffect(() => {
    const current = voiceStateRef.current;
    // Don't touch the mic if we're in an active capture or processing state
    if (current === VoiceState.ACTIVE_LISTENING || current === VoiceState.PROCESSING || current === VoiceState.RESPONDING || current === VoiceState.ACKNOWLEDGING) {
      return;
    }
    if (isSpeaking && current === VoiceState.AMBIENT_LISTENING) {
      stopAmbientAndWait();
    } else if (!isSpeaking && current === VoiceState.AMBIENT_LISTENING) {
      startAmbient();
    }
  }, [isSpeaking, stopAmbientAndWait, startAmbient]);
  */

  const startManualCapture = useCallback(async () => {
    // Force stop any ongoing speech (like the lesson being read)
    stopSpeaking();
    
    // Play a small beep so user knows it's active
    playBeep();

    updateVoiceState(VoiceState.ACTIVE_LISTENING);
    setInterimTranscript("");
    announceToScreenReader("Listening for your command...");

    try {
      const startTime = Date.now();
      const captureResult = await captureCommand((text) => setInterimTranscript(text));
      
      updateVoiceState(VoiceState.PROCESSING);
      announceToScreenReader("Processing your command...");

      try {
        const intentRes = await processCommand(captureResult);
        const executionTime = Date.now() - startTime;

        // Log it
        createVoiceLog(intentRes.raw_command, intentRes.intent, intentRes.confidence, executionTime).catch(console.error);

        updateVoiceState(VoiceState.RESPONDING);
        setInterimTranscript("");

        if (intentRes.confidence < 0.6) {
          speak("I didn't quite catch that. Please say it again.");
          setTimeout(returnToAmbient, 3000);
          return;
        }

        // Route intent
        handleIntent(
          intentRes,
          pageActionsRef.current.readLesson || (() => speak("Reading lesson is not available here.")),
          () => { stopSpeaking(); returnToAmbient(); },
          pageActionsRef.current.startQuiz || (() => speak("Quiz is not available here.")),
          pageActionsRef.current.submitCode || (() => speak("Code lab is not available here.")),
          () => speak("Use Alt plus V to toggle voice, or press Alt plus H for shortcuts."),
          repeatLast,
          logout
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

  // Keep a ref so callbacks (like onGreetingDetected) can call the latest version
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

