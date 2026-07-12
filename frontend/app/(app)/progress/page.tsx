"use client";

import { useEffect, useState } from "react";
import { getProgress } from "@/services/endpoints/progress";
import { ProgressResponse } from "@/types/api";
import { useVoice } from "@/contexts/VoiceContext";
import { KnowledgeTable } from "@/components/progress/KnowledgeTable";

export default function ProgressPage() {
  const [progress, setProgress] = useState<ProgressResponse | null>(null);
  const { speak, setPageActions } = useVoice();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    document.title = "My Progress — CodeSight AI";
    setPageActions({});
    getProgress().then(data => {
      setProgress(data);
      if (typeof window !== "undefined") {
         speak(`Progress Report. ${data.spoken_summary}`, true);
      }
    }).catch(console.error).finally(() => setLoading(false));
  }, [setPageActions, speak]);

  if (loading) return <div className="text-lg">Loading progress...</div>;
  if (!progress) return <div className="text-lg text-destructive">Failed to load progress.</div>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">My Progress</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
         <div className="p-6 bg-card border border-border rounded-lg shadow-sm">
            <h2 className="text-xl font-bold mb-2">Lessons Completed</h2>
            <p className="text-4xl font-bold text-primary">{progress.total_lessons_completed}</p>
         </div>
         <div className="p-6 bg-card border border-border rounded-lg shadow-sm">
            <h2 className="text-xl font-bold mb-2">Overall Status</h2>
            <p className="text-2xl font-bold text-foreground">{progress.completion_prediction}</p>
         </div>
      </div>

      <h2 className="text-2xl font-bold">Knowledge Profile</h2>
      <KnowledgeTable progress={progress} />
    </div>
  );
}
