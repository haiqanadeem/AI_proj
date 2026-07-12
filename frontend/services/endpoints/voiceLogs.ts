import { apiFetch } from "../apiClient";
import { VoiceLogResponse } from "../../types/api";

export async function createVoiceLog(
  command: string,
  intent_detected?: string,
  confidence_score?: number,
  execution_time_ms?: number
): Promise<VoiceLogResponse> {
  return apiFetch<VoiceLogResponse>("/voice-logs", {
    method: "POST",
    body: JSON.stringify({
      command,
      intent_detected,
      confidence_score,
      execution_time_ms,
    }),
  });
}

export async function getVoiceLogs(limit: number = 20): Promise<VoiceLogResponse[]> {
  return apiFetch<VoiceLogResponse[]>(`/voice-logs?limit=${limit}`, {
    method: "GET",
  });
}
