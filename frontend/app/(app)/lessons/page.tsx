"use client";

import { useEffect, useState } from "react";
import { getLessons } from "@/services/endpoints/lessons";
import { LessonResponse } from "@/types/api";
import { LessonCard } from "@/components/lessons/LessonCard";
import { LessonFilters } from "@/components/lessons/LessonFilters";
import { useVoice } from "@/contexts/VoiceContext";

export default function LessonsPage() {
  const [lessons, setLessons] = useState<LessonResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const { speak, setPageActions } = useVoice();

  useEffect(() => {
    document.title = "Lessons — CodeSight AI";
    setPageActions({});
    loadLessons("", "");
  }, [setPageActions]);

  const loadLessons = (diff: string, topic: string) => {
    setLoading(true);
    getLessons(diff, topic)
      .then(data => {
        setLessons(data);
        if (typeof window !== "undefined") {
           speak(`Lesson library. ${data.length} lessons available. Use filters or say 'Open lesson name'.`, true);
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Lesson Library</h1>
      <LessonFilters onFilter={loadLessons} />
      
      {loading ? (
        <div className="text-lg">Loading lessons...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {lessons.map(lesson => (
            <LessonCard key={lesson.id} lesson={lesson} />
          ))}
          {lessons.length === 0 && (
            <div className="col-span-full text-lg text-muted-foreground">No lessons found matching those filters.</div>
          )}
        </div>
      )}
    </div>
  );
}
