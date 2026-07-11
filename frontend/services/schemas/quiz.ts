import { z } from "zod";

export const QuizQuestionSchema = z.object({
  id: z.number(),
  type: z.enum(["mcq", "code_completion", "debug"]).catch("mcq"),
  question: z.string(),
  options: z.array(z.string()),
  correct_answer: z.enum(["A", "B", "C", "D"]),
  explanation: z.string(),
});

export const QuizGenerateResponseSchema = z.object({
  topic: z.string(),
  difficulty: z.string(),
  questions: z.array(QuizQuestionSchema),
}).catch({
  topic: "Unknown",
  difficulty: "beginner",
  questions: []
});

export const QuizSubmitSchema = z.object({
  lesson_id: z.number(),
  quiz_data: z.any(),
  answers: z.record(z.string()),
  time_taken_sec: z.number(),
});

export const QuizResultResponseSchema = z.object({
  score: z.number(),
  total: z.number(),
  feedback: z.string(),
  spoken_summary: z.string(),
}).catch({
  score: 0,
  total: 0,
  feedback: "Feedback could not be processed.",
  spoken_summary: "Your quiz could not be processed."
});
