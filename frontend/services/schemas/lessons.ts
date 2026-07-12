import { z } from "zod";

export const LessonResponseSchema = z.object({
  id: z.number(),
  title: z.string(),
  topic: z.string(),
  difficulty: z.string(),
  content: z.string(),
  code_example: z.string().nullable().optional(),
  estimated_minutes: z.number(),
  order_index: z.number(),
  next_lesson_id: z.number().nullable().optional(),
  prev_lesson_id: z.number().nullable().optional(),
});
