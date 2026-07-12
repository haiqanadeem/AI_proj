import Link from "next/link";
import { LessonResponse } from "@/types/api";

export function LessonCard({ lesson }: { lesson: LessonResponse }) {
  return (
    <Link href={`/lessons/${lesson.id}`} className="block p-6 bg-card border border-border rounded-lg shadow-sm hover:shadow-md focus:outline-none focus:ring-2 focus:ring-primary transition-shadow">
      <h3 className="text-xl font-bold mb-2">{lesson.title}</h3>
      <p className="text-sm text-muted-foreground mb-4">Topic: {lesson.topic}</p>
      <div className="flex justify-between text-sm">
        <span className="bg-secondary text-secondary-foreground px-2 py-1 rounded">{lesson.difficulty}</span>
        <span className="text-muted-foreground">{lesson.estimated_minutes} min</span>
      </div>
    </Link>
  );
}
