"use client";

import { useVoice } from "@/contexts/VoiceContext";
import { VoiceState } from "@/lib/constants";

export function VoiceButton() {
  const { voiceState, startManualCapture } = useVoice();

  const isDisabled = voiceState === VoiceState.MIC_DENIED || voiceState === VoiceState.VOICE_UNAVAILABLE;

  let label = "Press to speak a command";
  if (voiceState === VoiceState.MIC_DENIED) label = "Microphone denied";
  if (voiceState === VoiceState.VOICE_UNAVAILABLE) label = "Voice unavailable";

  return (
    <button
      onClick={startManualCapture}
      disabled={isDisabled}
      aria-label={label}
      className={`fixed bottom-6 right-6 p-4 rounded-full shadow-lg border-2 border-transparent focus:outline-none focus:border-primary font-bold z-50 flex items-center justify-center ${
        isDisabled ? "bg-muted text-muted-foreground" : "bg-primary text-primary-foreground hover:bg-primary/90"
      }`}
    >
      <span className="text-2xl">🎤</span>
    </button>
  );
}
