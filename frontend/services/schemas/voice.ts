import { z } from "zod";

export const TranscribeResponseSchema = z.object({
  transcript: z.string().catch(""),
  confidence: z.number().catch(0),
});

export const IntentResponseSchema = z.object({
  intent: z.string(),
  params: z.record(z.any()).optional().nullable(),
  confidence: z.number(),
  raw_command: z.string(),
});
