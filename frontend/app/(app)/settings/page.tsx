"use client";

import { useEffect } from "react";
import { useVoice } from "@/contexts/VoiceContext";

export default function SettingsPage() {
  const { speak, setPageActions, voices, preferredVoice, changeVoice } = useVoice();

  useEffect(() => {
    document.title = "Settings & Help — CodeSight AI";
    setPageActions({});
    if (typeof window !== "undefined") {
       speak("Settings and Help page. Read the screen to learn about voice commands and keyboard shortcuts.", true);
    }
  }, [speak, setPageActions]);

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold">Settings & Help</h1>

      <section className="p-6 bg-card border border-border rounded-lg shadow-sm">
        <h2 className="text-2xl font-bold mb-4">Voice Commands</h2>
        <ul className="list-disc list-inside space-y-2">
          <li><strong>"Hey CodeSight"</strong>: Wake up the ambient voice assistant.</li>
          <li><strong>"Nav to lessons"</strong>: Open the lesson library.</li>
          <li><strong>"Start Quiz"</strong>: Start a quiz for the current lesson.</li>
          <li><strong>"Read Lesson"</strong>: Read the current lesson aloud.</li>
          <li><strong>"Submit Code"</strong>: Run code in the Code Lab.</li>
          <li><strong>"Ask Tutor"</strong>: Go to the AI Tutor page.</li>
        </ul>
      </section>

      <section className="p-6 bg-card border border-border rounded-lg shadow-sm">
        <h2 className="text-2xl font-bold mb-4">Voice Settings</h2>
        <div className="space-y-4">
          <p className="text-muted-foreground">Select your preferred assistant voice. When you change the voice, it will speak a sample phrase.</p>
          <div className="flex flex-col space-y-2 max-w-md">
            <label htmlFor="voice-select" className="font-semibold text-lg">Available Voices</label>
            <select 
              id="voice-select"
              className="p-3 border border-border rounded bg-background text-foreground text-lg focus:ring-2 focus:ring-primary outline-none"
              value={preferredVoice?.voiceURI || ""}
              onChange={(e) => {
                changeVoice(e.target.value);
                // Play sample with the new voice immediately
                speak("Hello, I am your new voice assistant.", true);
              }}
            >
              {voices.length === 0 && <option value="">Loading voices...</option>}
              {voices.map(voice => (
                <option key={voice.voiceURI} value={voice.voiceURI}>
                  {voice.name} ({voice.lang})
                </option>
              ))}
            </select>
          </div>
        </div>
      </section>

      <section className="p-6 bg-card border border-border rounded-lg shadow-sm">
        <h2 className="text-2xl font-bold mb-4">Keyboard Shortcuts (Alt / Option)</h2>
        <ul className="list-disc list-inside space-y-2">
          <li><strong>Alt + V</strong>: Manually trigger voice listening (Push-to-talk).</li>
          <li><strong>Alt + R</strong>: Read current page / lesson aloud.</li>
          <li><strong>Alt + Q</strong>: Start Quiz.</li>
          <li><strong>Alt + H</strong>: Speak help options.</li>
          <li><strong>Tab</strong>: Navigate interactive elements (buttons, inputs, links).</li>
        </ul>
      </section>
    </div>
  );
}
