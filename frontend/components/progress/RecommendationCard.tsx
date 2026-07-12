"use client";

import { useEffect, useState } from "react";
import { getRecommendation } from "@/services/endpoints/progress";
import { RecommendationResponse } from "@/types/api";
import Link from "next/link";
import { useVoice } from "@/contexts/VoiceContext";

export function RecommendationCard() {
  const [rec, setRec] = useState<RecommendationResponse | null>(null);

  useEffect(() => {
    getRecommendation().then(setRec).catch(console.error);
  }, []);

  if (!rec) return <div className="p-4 border rounded shadow-sm animate-pulse h-32 bg-card"></div>;

  return (
    <div className="p-6 border border-border rounded-lg shadow-sm bg-card mb-6">
      <h2 className="text-xl font-bold mb-2">Recommended for You</h2>
      <p className="text-lg mb-4">{rec.title}</p>
      <p className="text-muted-foreground mb-4">{rec.reason}</p>
      <Link href={`/lessons/${rec.lesson_id}`} className="inline-block bg-primary text-primary-foreground px-4 py-2 rounded font-medium focus:outline-none focus:ring-2 focus:ring-accent">
        Start Lesson
      </Link>
    </div>
  );
}
