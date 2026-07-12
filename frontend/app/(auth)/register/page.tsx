"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { UserRegisterSchema } from "@/services/schemas/auth";
import { z } from "zod";
import { useAuth } from "@/contexts/AuthContext";
import { useEffect, useState } from "react";
import Link from "next/link";

type RegisterFormInputs = z.infer<typeof UserRegisterSchema>;

export default function RegisterPage() {
  const { register: registerUser } = useAuth();
  const [errorMsg, setErrorMsg] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormInputs>({
    resolver: zodResolver(UserRegisterSchema),
  });

  useEffect(() => {
    if (typeof window !== "undefined") {
        window.speechSynthesis.cancel();
        const msg = new SpeechSynthesisUtterance("Registration page. Enter your name, email, and password, then press Enter to submit.");
        window.speechSynthesis.speak(msg);
    }
  }, []);

  const onSubmit = async (data: RegisterFormInputs) => {
    setErrorMsg("");
    try {
      await registerUser(data);
    } catch (e: any) {
      setErrorMsg(e.message || "Registration failed. Try again.");
    }
  };

  return (
    <div className="w-full bg-card p-8 rounded-lg shadow-sm border border-border">
      <h1 className="text-2xl font-bold mb-6 text-center">Register for CodeSight</h1>

      <div aria-live="polite" className="text-destructive mb-4 text-sm font-medium">
        {errorMsg}
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium mb-1">
            Full Name
          </label>
          <input
            id="name"
            type="text"
            {...register("name")}
            className="w-full p-3 rounded-md border border-input bg-background focus:outline-none focus:ring-2 focus:ring-primary"
            aria-invalid={!!errors.name}
            aria-describedby={errors.name ? "name-error" : undefined}
          />
          {errors.name && (
            <p id="name-error" className="text-destructive text-sm mt-1" aria-live="polite">
              {errors.name.message}
            </p>
          )}
        </div>

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
          {isSubmitting ? "Registering..." : "Register"}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-muted-foreground">
        Already have an account? <Link href="/login" className="text-primary hover:underline focus:outline-none focus:ring-2 focus:ring-primary rounded p-1">Login here</Link>
      </p>
    </div>
  );
}
