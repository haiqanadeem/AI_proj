"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { UserResponse, LoginInput, UserRegister } from "../types/api";
import { loginUser, registerUser, getMe } from "../services/endpoints/auth";
import { useRouter } from "next/navigation";

interface AuthContextType {
  user: UserResponse | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (input: LoginInput) => Promise<void>;
  register: (input: UserRegister) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      setToken(storedToken);
      getMe()
        .then((userData) => {
          setUser(userData);
        })
        .catch(() => {
          localStorage.removeItem("token");
          setToken(null);
        })
        .finally(() => {
          setIsLoading(false);
        });
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (input: LoginInput) => {
    setIsLoading(true);
    try {
      const response = await loginUser(input);
      localStorage.setItem("token", response.access_token);
      setToken(response.access_token);
      
      const userData = await getMe();
      setUser(userData);
      
      const params = new URLSearchParams(window.location.search);
      const returnTo = params.get("returnTo") || "/dashboard";
      router.push(returnTo);
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (input: UserRegister) => {
    setIsLoading(true);
    try {
      await registerUser(input);
      await login({ email: input.email, password: input.password });
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
    router.push("/login");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!token,
        isLoading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
