"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { LoginSchema } from "@/services/schemas/auth";
import { z } from "zod";
import { useAuth } from "@/contexts/AuthContext";
import { useVoiceAuth } from "@/hooks/useVoiceAuth";
import { useEffect, useState } from "react";
import Link from "next/link";

type LoginFormInputs = z.infer<typeof LoginSchema>;

export default function LoginPage() {
  const { login } = useAuth();
  const { state: voiceState, startVoiceLogin } = useVoiceAuth();
  const [errorMsg, setErrorMsg] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormInputs>({
    resolver: zodResolver(LoginSchema),
  });

  useEffect(() => {
    if (typeof window !== "undefined") {
        const msg = new SpeechSynthesisUtterance("Login page. Enter your email and password, then press the voice button to login by voice, or press Enter to submit.");
        window.speechSynthesis.speak(msg);
    }
  }, []);

  const onSubmit = async (data: LoginFormInputs) => {
    setErrorMsg("");
    try {
      await login(data);
    } catch (e: any) {
      setErrorMsg(e.message || "Invalid credentials, try again.");
    }
  };

  return (
    <div className="w-full bg-card p-8 rounded-lg shadow-sm border border-border">
      <h1 className="text-2xl font-bold mb-6 text-center">Login to CodeSight AI</h1>
      
      <div className="mb-6 flex justify-center">
        <button
          type="button"
          onClick={startVoiceLogin}
          disabled={voiceState === "UNAVAILABLE" || voiceState !== "IDLE"}
          className="w-full py-4 bg-secondary text-secondary-foreground rounded-lg border-2 border-transparent focus:outline-none focus:border-primary hover:bg-secondary/80 flex items-center justify-center gap-2 font-medium disabled:opacity-50"
          aria-label={voiceState === "UNAVAILABLE" ? "Voice login unavailable" : "Press to login by voice"}
        >
          {voiceState === "UNAVAILABLE" ? "Voice Unavailable" : voiceState === "IDLE" ? "🎤 Voice Login" : `🎤 ${voiceState.replace("_", " ")}`}
        </button>
      </div>

      <div className="relative flex items-center py-2 mb-6">
          <div className="flex-grow border-t border-border"></div>
          <span className="flex-shrink-0 mx-4 text-muted-foreground text-sm">or use keyboard</span>
          <div className="flex-grow border-t border-border"></div>
      </div>

      <div aria-live="polite" className="text-destructive mb-4 text-sm font-medium">
        {errorMsg}
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label htmlFor="email" className="block text-sm font-medium mb-1">
            Email Address
          </label>
          <input
            id="email"
            type="email"
            {...register("email")}
            className="w-full p-3 rounded-md border border-input bg-background focus:outline-none focus:ring-2 focus:ring-primary"
            aria-invalid={!!errors.email}
            aria-describedby={errors.email ? "email-error" : undefined}
          />
          {errors.email && (
            <p id="email-error" className="text-destructive text-sm mt-1" aria-live="polite">
              {errors.email.message}
            </p>
          )}
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium mb-1">
            Password
          </label>
          <input
            id="password"
            type="password"
            {...register("password")}
            className="w-full p-3 rounded-md border border-input bg-background focus:outline-none focus:ring-2 focus:ring-primary"
            aria-invalid={!!errors.password}
            aria-describedby={errors.password ? "password-error" : undefined}
          />
          {errors.password && (
            <p id="password-error" className="text-destructive text-sm mt-1" aria-live="polite">
              {errors.password.message}
            </p>
          )}
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full py-3 mt-4 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50 font-bold"
        >
          {isSubmitting ? "Logging in..." : "Login"}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-muted-foreground">
        Don't have an account? <Link href="/register" className="text-primary hover:underline focus:outline-none focus:ring-2 focus:ring-primary rounded p-1">Register here</Link>
      </p>
    </div>
  );
}
