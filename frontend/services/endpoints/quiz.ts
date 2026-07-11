import { apiFetch } from "../apiClient";
import { QuizGenerateResponse, QuizResultResponse } from "../../types/api";

export async function generateQuiz(
  topic: string,
  difficulty: string,
  lesson_id: number
): Promise<QuizGenerateResponse> {
  return apiFetch<QuizGenerateResponse>("/quiz/generate", {
    method: "POST",
    body: JSON.stringify({ topic, difficulty, lesson_id }),
  });
}

export async function submitQuiz(
  lesson_id: number,
  quiz_data: any,
  answers: Record<string, string>,
  time_taken_sec: number
): Promise<QuizResultResponse> {
  return apiFetch<QuizResultResponse>("/quiz/submit", {
    method: "POST",
    body: JSON.stringify({ lesson_id, quiz_data, answers, time_taken_sec }),
  });
}
