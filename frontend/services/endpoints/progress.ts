import { apiFetch } from "../apiClient";
import { ProgressResponse, RecommendationResponse } from "../../types/api";

export async function getProgress(): Promise<ProgressResponse> {
  const res: any = await apiFetch("/progress", {
    method: "GET",
  });
  
  // Map backend format to frontend type
  const knowledge_profile = Object.keys(res.knowledge_profile || {}).map((key) => ({
      topic: key,
      mastery_percentage: res.knowledge_profile[key],
      status: res.knowledge_profile[key] >= 80 ? "Mastered" : res.knowledge_profile[key] >= 50 ? "In Progress" : "Needs Review"
  }));
  
  return {
      user_id: res.user_id || 0,
      total_lessons_completed: res.lessons_completed || 0,
      knowledge_profile,
      completion_prediction: `${res.completion_prediction}%`,
      at_risk: res.at_risk || false,
      spoken_summary: res.spoken_summary || ""
  };
}

export async function getRecommendation(): Promise<RecommendationResponse> {
  const res: any = await apiFetch("/progress/recommend", {
    method: "GET",
  });
  
  return {
      lesson_id: res.recommended_lesson?.id || 0,
      title: res.recommended_lesson?.title || "Unknown Lesson",
      reason: res.reason || "",
      spoken_recommendation: res.spoken_recommendation || ""
  };
}
