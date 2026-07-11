"use client";

import { useEffect, useState } from "react";
import { getLessonById } from "@/services/endpoints/lessons";
import { LessonResponse } from "@/types/api";
import { LessonContent } from "@/components/lessons/LessonContent";
import { useVoice } from "@/contexts/VoiceContext";
import { useParams, useRouter } from "next/navigation";

export default function LessonDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [lesson, setLesson] = useState<LessonResponse | null>(null);
  const { speak, setPageActions } = useVoice();

  useEffect(() => {
    const id = parseInt(params.lessonId as string, 10);
    if (!isNaN(id)) {
      getLessonById(id).then(data => {
        setLesson(data);
        document.title = `${data.title} — CodeSight AI`;
        speak(`Lesson: ${data.title}. ${data.difficulty} level. Say 'read lesson' to hear the content.`, true);
      }).catch(console.error);
    }
  }, [params.lessonId, speak]);

  useEffect(() => {
    if (lesson) {
      setPageActions({
        readLesson: () => {
          speak(lesson.title);
          speak(lesson.content);
          if (lesson.code_example) {
              speak("Code Example:");
              speak(lesson.code_example);
          }
        },
        startQuiz: () => {
          router.push(`/quiz/${lesson.id}`);
        },
        submitCode: () => {
          if (lesson.code_example) {
             localStorage.setItem("pendingCodeExample", lesson.code_example);
          }
          router.push("/code-lab");
        }
      });
    }
  }, [lesson, speak, setPageActions, router]);

  const handleReadLesson = () => {
      speak(lesson?.title || "");
      speak(lesson?.content || "");
      if (lesson?.code_example) {
          speak("Code Example:");
          speak(lesson.code_example);
      }
  };

  if (!lesson) return <div className="text-lg">Loading lesson...</div>;

  return (
    <div>
      <div className="flex flex-wrap gap-4 mb-6">
        <button onClick={handleReadLesson} className="px-4 py-2 bg-secondary text-secondary-foreground rounded focus:outline-none focus:ring-2 focus:ring-primary font-medium">
          🔊 Read Aloud
        </button>
        <button onClick={() => router.push(`/quiz/${lesson.id}`)} className="px-4 py-2 bg-primary text-primary-foreground rounded focus:outline-none focus:ring-2 focus:ring-accent font-medium">
          Start Quiz
        </button>
        <button onClick={() => {
            if (lesson.code_example) localStorage.setItem("pendingCodeExample", lesson.code_example);
            router.push("/code-lab");
        }} className="px-4 py-2 bg-secondary text-secondary-foreground rounded focus:outline-none focus:ring-2 focus:ring-primary font-medium">
          Open in Code Lab
        </button>
      </div>

      <LessonContent lesson={lesson} />
    </div>
  );
}
