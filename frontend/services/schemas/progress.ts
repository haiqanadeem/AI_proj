import { z } from "zod";

export const ProgressTopicSchema = z.object({
  topic: z.string(),
  mastery_percentage: z.number(),
  status: z.string(),
});

export const ProgressResponseSchema = z.object({
  user_id: z.number(),
  total_lessons_completed: z.number(),
  knowledge_profile: z.array(ProgressTopicSchema),
  completion_prediction: z.string(),
  at_risk: z.boolean(),
  spoken_summary: z.string(),
}).catch({
  user_id: 0,
  total_lessons_completed: 0,
  knowledge_profile: [],
  completion_prediction: "Unknown",
  at_risk: false,
  spoken_summary: "Progress data could not be retrieved."
});

export const RecommendationResponseSchema = z.object({
  lesson_id: z.number(),
  title: z.string(),
  reason: z.string(),
  spoken_recommendation: z.string(),
}).catch({
  lesson_id: 0,
  title: "Keep exploring lessons",
  reason: "No specific recommendation available.",
  spoken_recommendation: "You should keep exploring the lesson library."
});
