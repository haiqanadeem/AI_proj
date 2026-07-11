"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { generateQuiz, submitQuiz } from "@/services/endpoints/quiz";
import { getLessonById } from "@/services/endpoints/lessons";
import { QuizGenerateResponse, QuizResultResponse } from "@/types/api";
import { QuizQuestionCard } from "@/components/quiz/QuizQuestionCard";
import { useVoice } from "@/contexts/VoiceContext";

export default function QuizPage() {
  const params = useParams();
  const router = useRouter();
  const { speak, setPageActions } = useVoice();
  
  const [lessonId, setLessonId] = useState<number>(0);
  const [quiz, setQuiz] = useState<QuizGenerateResponse | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<QuizResultResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [startTime, setStartTime] = useState<number>(0);

  useEffect(() => {
    const id = parseInt(params.lessonId as string, 10);
    if (!isNaN(id)) {
      setLessonId(id);
      getLessonById(id).then(lesson => {
        document.title = `Quiz: ${lesson.title} — CodeSight AI`;
        return generateQuiz(lesson.topic, lesson.difficulty, id);
      }).then(data => {
        setQuiz(data);
        setStartTime(Date.now());
        setLoading(false);
        speak(`Quiz generated with ${data.questions.length} questions. You can use Tab to navigate and space to select options.`, true);
      }).catch(console.error);
    }
  }, [params.lessonId, speak]);

  useEffect(() => {
    setPageActions({});
  }, [setPageActions]);

  const handleSelect = (qId: number, val: string) => {
    setAnswers(prev => ({ ...prev, [qId.toString()]: val }));
  };

  const handleSubmit = async () => {
    if (!quiz) return;
    setSubmitting(true);
    const timeTaken = Math.floor((Date.now() - startTime) / 1000);
    try {
      const res = await submitQuiz(lessonId, quiz, answers, timeTaken);
      setResult(res);
      speak(`Quiz submitted. You scored ${res.score} out of ${res.total}. ${res.spoken_summary}`);
    } catch (e) {
      console.error(e);
      speak("Failed to submit quiz.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="text-lg">Generating personalized quiz...</div>;
  if (!quiz) return <div className="text-lg text-destructive">Failed to load quiz.</div>;

  if (result) {
    return (
      <div className="max-w-2xl mx-auto p-8 bg-card border border-border rounded-lg shadow-sm text-center">
        <h1 className="text-3xl font-bold mb-4">Quiz Results</h1>
        <p className="text-xl mb-4">Score: <strong>{result.score} / {result.total}</strong></p>
        <p className="text-lg mb-8">{result.feedback}</p>
        <button onClick={() => router.push(`/lessons/${lessonId}`)} className="px-6 py-3 bg-primary text-primary-foreground font-bold rounded-lg focus:outline-none focus:ring-2 focus:ring-accent">
          Return to Lesson
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Quiz: {quiz.topic}</h1>
      
      {quiz.questions.map((q, i) => (
        <QuizQuestionCard 
          key={q.id} 
          index={i}
          question={q} 
          selectedValue={answers[q.id.toString()] || ""} 
          onSelect={(val) => handleSelect(q.id, val)}
        />
      ))}
      
      <div className="flex justify-end mt-8">
        <button 
          onClick={handleSubmit} 
          disabled={submitting || Object.keys(answers).length < quiz.questions.length}
          className="px-8 py-4 bg-primary text-primary-foreground font-bold rounded-lg focus:outline-none focus:ring-2 focus:ring-accent disabled:opacity-50"
        >
          {submitting ? "Submitting..." : "Submit Quiz"}
        </button>
      </div>
    </div>
  );
}
