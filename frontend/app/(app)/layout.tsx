"use client";

import { VoiceProvider } from "@/contexts/VoiceContext";
import { AppNav } from "@/components/layout/AppNav";
import { SkipLink } from "@/components/layout/SkipLink";
import { VoiceStatusBar } from "@/components/voice/VoiceStatusBar";
import { VoiceButton } from "@/components/voice/VoiceButton";
import { useKeyboardShortcuts } from "@/hooks/useKeyboardShortcuts";
import { ReactNode } from "react";
import { useRouter } from "next/navigation";
import { useVoice } from "@/contexts/VoiceContext";

function KeyboardShortcutsHandler() {
  const router = useRouter();
  const { startManualCapture, speak } = useVoice();
  
  useKeyboardShortcuts(
    startManualCapture,
    () => speak("Read page not explicitly set on this route."),
    () => router.push("/lessons"),
    () => router.push("/lessons"),
    () => router.push("/lessons"),
    () => router.push("/settings")
  );
  return null;
}

export default function AppLayout({ children }: { children: ReactNode }) {
  return (
    <VoiceProvider>
      <div className="min-h-screen bg-background text-foreground flex flex-col">
        <SkipLink />
        <VoiceStatusBar />
        <AppNav />
        <KeyboardShortcutsHandler />
        <main id="main-content" className="flex-grow w-full max-w-7xl mx-auto p-4 md:p-8">
          {children}
        </main>
        <VoiceButton />
      </div>
    </VoiceProvider>
  );
}
