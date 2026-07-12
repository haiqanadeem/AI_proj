import { z } from "zod";

export const CodeExecuteRequestSchema = z.object({
  code: z.string(),
  language: z.string().default("python"),
  lesson_id: z.number().optional(),
});

export const CodeExecuteResponseSchema = z.object({
  stdout: z.string().catch(""),
  stderr: z.string().catch(""),
  exit_code: z.number().catch(-1),
  execution_time_ms: z.number().catch(0),
});

export const CodeAnalyzeRequestSchema = z.object({
  code: z.string(),
  execution_error: z.string().optional().nullable(),
  lesson_id: z.number().optional(),
});

export const CodeErrorSchema = z.object({
  type: z.enum(["SyntaxError", "LogicError", "RuntimeError", "Error"]).catch("Error"),
  description: z.string(),
  line: z.number().catch(1),
  fix: z.string().catch(""),
});

export const CodeAnalyzeResponseSchema = z.object({
  has_errors: z.boolean().catch(true),
  errors: z.array(CodeErrorSchema).catch([]),
  positive_feedback: z.string().catch(""),
  spoken_summary: z.string().catch("Analysis unavailable."),
});
