import { z } from "zod";

export const ChatRequestSchema = z.object({
  message: z.string(),
  session_id: z.string(),
  lesson_context: z.string().optional().nullable(),
});

export const RagSourceSchema = z.object({
  content: z.string(),
  metadata: z.record(z.any()),
});

export const ChatResponseSchema = z.object({
  response: z.string(),
  rag_sources: z.array(RagSourceSchema).optional().nullable(),
});
