import { z } from "zod";

export const UserResponseSchema = z.object({
  id: z.number(),
  name: z.string(),
  email: z.string().email(),
  level: z.string(),
  created_at: z.string().datetime(),
});

export const TokenResponseSchema = z.object({
  access_token: z.string(),
  token_type: z.string(),
  user: z.record(z.any()),
});

export const UserRegisterSchema = z.object({
  name: z.string().min(1, "Name is required"),
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

export const LoginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(1, "Password is required"),
});
