"use client";

import { useEffect } from "react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
    if (typeof window !== "undefined") {
        window.speechSynthesis.speak(new SpeechSynthesisUtterance("An unexpected error occurred."));
    }
  }, [error]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 text-center">
      <h1 className="text-4xl font-bold mb-4 text-destructive">Something went wrong</h1>
      <p className="text-lg text-muted-foreground mb-8">{error.message || "An unexpected error occurred."}</p>
      <button
        onClick={() => reset()}
        className="px-6 py-3 bg-primary text-primary-foreground rounded-lg font-bold"
      >
        Try again
      </button>
    </div>
  );
}
