import { LessonResponse } from "@/types/api";

export function LessonContent({ lesson }: { lesson: LessonResponse }) {
  return (
    <article className="prose dark:prose-invert max-w-none">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-4">{lesson.title}</h1>
        <div className="flex gap-4 text-sm text-muted-foreground">
          <span className="bg-secondary text-secondary-foreground px-2 py-1 rounded">{lesson.difficulty}</span>
          <span>Topic: {lesson.topic}</span>
          <span>{lesson.estimated_minutes} minutes estimated</span>
        </div>
      </div>
      
      <div className="text-lg leading-relaxed mb-8 whitespace-pre-wrap">
        {lesson.content}
      </div>

      {lesson.code_example && (
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Code Example</h2>
          <pre className="p-4 bg-muted text-foreground rounded-lg overflow-x-auto border border-border" aria-label="Code example">
            <code>{lesson.code_example}</code>
          </pre>
        </div>
      )}
    </article>
  );
}
