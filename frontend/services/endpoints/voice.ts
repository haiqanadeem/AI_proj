import { apiFetch } from "../apiClient";
import { TranscribeResponse, IntentResponse } from "../../types/api";

export async function transcribeAudio(audioBlob: Blob): Promise<TranscribeResponse> {
  const formData = new FormData();
  formData.append("audio", audioBlob, "audio.webm");

  return apiFetch<TranscribeResponse>("/voice/transcribe", {
    method: "POST",
    body: formData,
  });
}

export async function classifyIntent(transcript: string): Promise<IntentResponse> {
  return apiFetch<IntentResponse>("/ai/classify-intent", {
    method: "POST",
    body: JSON.stringify({ transcript }),
  });
}
