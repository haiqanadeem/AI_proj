"use client";

import React, { useEffect } from "react";
import { useVoice } from "@/contexts/VoiceContext";
import { VoiceState } from "@/lib/constants";

export function VoiceStatusBar() {
  const { voiceState, isSpeaking, interimTranscript } = useVoice();

  let message = "Loading voice engine...";
  let isPulsing = false;

  switch (voiceState) {
    case VoiceState.AMBIENT_LISTENING:
      message = "Ambient — say 'Hey CodeSight' to begin";
      break;
    case VoiceState.AMBIENT_UNAVAILABLE:
      message = "Ambient listening unavailable — press voice button or Alt+V";
      break;
    case VoiceState.MIC_DENIED:
      message = "Microphone access denied — use keyboard shortcuts (Alt+H for help)";
      break;
    case VoiceState.VOICE_UNAVAILABLE:
      message = "Voice not supported — use keyboard shortcuts";
      break;
    case VoiceState.GREETING_DETECTED:
    case VoiceState.ACKNOWLEDGING:
    case VoiceState.RESPONDING:
      message = "Speaking...";
      break;
    case VoiceState.ACTIVE_LISTENING:
      message = interimTranscript ? `"${interimTranscript}..."` : "Listening for your command...";
      isPulsing = true;
      break;
    case VoiceState.PROCESSING:
      message = "Processing your request...";
      isPulsing = true;
      break;
  }

  if (isSpeaking && voiceState !== VoiceState.ACTIVE_LISTENING) {
    message = "Speaking... (Mic paused)";
  }
  useEffect(() => {
    console.group("🖥 Navbar");

    console.log("voiceState:", voiceState);

    console.log("interimTranscript:", interimTranscript);

    console.log("message:", message);

    console.groupEnd();

  }, [voiceState, interimTranscript]);

  return (
    <div
      role="status"
      aria-live="polite"
      className="w-full bg-accent text-accent-foreground p-3 flex items-center justify-center gap-3 border-b border-border shadow-sm"
    >
      <div className={`w-3 h-3 rounded-full bg-primary ${isPulsing ? "animate-pulse" : ""}`} aria-hidden="true" />
      <span className="font-medium text-lg">{message}</span>
    </div>
  );
}
