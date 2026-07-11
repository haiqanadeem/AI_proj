"use client";

import { useEffect, useState } from "react";
import { getProgress } from "@/services/endpoints/progress";
import { ProgressResponse } from "@/types/api";
import { useAuth } from "@/contexts/AuthContext";
import { RecommendationCard } from "@/components/progress/RecommendationCard";
import Link from "next/link";
import { useVoice } from "@/contexts/VoiceContext";

const QUICK_ACTIONS = [
  { href: "/lessons", title: "Lessons", shortcut: "Alt+N for next lesson", command: "Say 'Lessons'" },
  { href: "/tutor", title: "AI Tutor", shortcut: "Alt+H for help", command: "Say 'Ask Tutor'" },
  { href: "/code-lab", title: "Code Lab", shortcut: "Alt+V for voice", command: "Say 'Submit Code'" },
  { href: "/progress", title: "Progress", shortcut: "Check your knowledge", command: "Say 'My Progress'" },
];

export default function DashboardPage() {
  const { user } = useAuth();
  const [progress, setProgress] = useState<ProgressResponse | null>(null);
  const { speak, setPageActions } = useVoice();

  useEffect(() => {
    document.title = "Dashboard — CodeSight AI";
    setPageActions({}); // clear specific actions
    getProgress().then((data) => {
      setProgress(data);
      if (typeof window !== "undefined") {
        speak(`Welcome back, ${user?.name || "Student"}. ${data.spoken_summary}`, true);
      }
    }).catch(console.error);
  }, [user, speak, setPageActions]);

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      
      <RecommendationCard />

      <section>
        <h2 className="text-2xl font-bold mb-4">Quick Navigation</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {QUICK_ACTIONS.map(action => (
            <Link key={action.href} href={action.href} className="block p-6 bg-card border border-border rounded-lg shadow-sm hover:shadow-md focus:outline-none focus:ring-2 focus:ring-primary transition-shadow">
              <h3 className="text-xl font-bold mb-2">{action.title}</h3>
              <p className="text-sm text-muted-foreground mb-1">{action.command}</p>
              <p className="text-sm text-muted-foreground">{action.shortcut}</p>
            </Link>
          ))}
        </div>
      </section>

      {progress && (
        <section>
          <h2 className="text-2xl font-bold mb-4">Your Progress Summary</h2>
          <div className="p-6 bg-card border border-border rounded-lg shadow-sm">
            <p className="text-lg mb-2">Lessons Completed: <strong>{progress.total_lessons_completed}</strong></p>
            <p className="text-lg">Status: <strong>{progress.completion_prediction}</strong></p>
          </div>
        </section>
      )}
    </div>
  );
}
