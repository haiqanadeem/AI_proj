import { apiFetch } from "../apiClient";
import { LessonResponse } from "../../types/api";

export async function getLessons(difficulty?: string, topic?: string): Promise<LessonResponse[]> {
  const params = new URLSearchParams();
  if (difficulty) params.append("difficulty", difficulty);
  if (topic) params.append("topic", topic);

  const query = params.toString();
  const res = await apiFetch<{ lessons: LessonResponse[], total: number }>(`/lessons${query ? `?${query}` : ""}`, {
    method: "GET",
  });
  return res.lessons;
}

export async function getLessonById(id: number): Promise<LessonResponse> {
  return apiFetch<LessonResponse>(`/lessons/${id}`, {
    method: "GET",
  });
}
