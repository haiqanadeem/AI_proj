import { apiFetch } from "../apiClient";
import { ChatResponse } from "../../types/api";

export async function chatWithTutor(
  message: string,
  session_id: string,
  lesson_context?: string
): Promise<ChatResponse> {
  return apiFetch<ChatResponse>("/tutor/chat", {
    method: "POST",
    body: JSON.stringify({ message, session_id, lesson_context }),
  });
}
