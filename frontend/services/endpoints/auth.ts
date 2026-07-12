import { apiFetch } from "../apiClient";
import { z } from "zod";
import { UserResponseSchema, TokenResponseSchema, UserRegisterSchema, LoginSchema } from "../schemas/auth";

export type UserResponse = z.infer<typeof UserResponseSchema>;
export type TokenResponse = z.infer<typeof TokenResponseSchema>;
export type UserRegister = z.infer<typeof UserRegisterSchema>;
export type LoginInput = z.infer<typeof LoginSchema>;

export async function loginUser(input: LoginInput): Promise<TokenResponse> {
  const params = new URLSearchParams();
  params.append("username", input.email);
  params.append("password", input.password);
  params.append("grant_type", "password");

  return apiFetch<TokenResponse>("/auth/login", {
    method: "POST",
    body: params.toString(),
  });
}

export async function registerUser(input: UserRegister): Promise<UserResponse> {
  return apiFetch<UserResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function getMe(): Promise<UserResponse> {
  return apiFetch<UserResponse>("/auth/me", {
    method: "GET",
  });
}
