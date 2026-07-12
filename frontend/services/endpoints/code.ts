import { apiFetch } from "../apiClient";
import { CodeExecuteResponse, CodeAnalyzeResponse } from "../../types/api";

export async function executeCode(
  code: string,
  language: string = "python",
  lesson_id?: number
): Promise<CodeExecuteResponse> {
  return apiFetch<CodeExecuteResponse>("/code/execute", {
    method: "POST",
    body: JSON.stringify({ code, language, lesson_id }),
  });
}

export async function analyzeCode(
  code: string,
  execution_error?: string,
  lesson_id?: number
): Promise<CodeAnalyzeResponse> {
  return apiFetch<CodeAnalyzeResponse>("/code/analyze", {
    method: "POST",
    body: JSON.stringify({ code, execution_error, lesson_id }),
  });
}
