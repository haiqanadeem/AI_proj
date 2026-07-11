import { z } from "zod";

export const VoiceLogCreateSchema = z.object({
  command: z.string(),
  intent_detected: z.string().optional().nullable(),
  confidence_score: z.number().optional().nullable(),
  execution_time_ms: z.number().optional().nullable(),
});

export const VoiceLogResponseSchema = z.object({
  id: z.number(),
  user_id: z.number(),
  command: z.string(),
  intent_detected: z.string().nullable(),
  confidence_score: z.number().nullable(),
  execution_time_ms: z.number().nullable(),
  created_at: z.string().datetime(),
});
