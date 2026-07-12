"use client";

import Link from "next/link";
import { useEffect } from "react";

export default function NotFound() {
  useEffect(() => {
    if (typeof window !== "undefined") {
        window.speechSynthesis.speak(new SpeechSynthesisUtterance("Page not found. Press Alt plus V and say 'Navigate Home'."));
    }
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 text-center">
      <h1 className="text-4xl font-bold mb-4">404 - Page Not Found</h1>
      <p className="text-lg text-muted-foreground mb-8">The page you are looking for doesn't exist.</p>
      <Link href="/dashboard" className="px-6 py-3 bg-primary text-primary-foreground rounded-lg font-bold">
        Return to Dashboard
      </Link>
    </div>
  );
}
