import { ReactNode } from "react";

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col justify-center items-center p-4">
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-primary text-primary-foreground p-2 z-50">
        Skip to main content
      </a>
      <main id="main-content" className="w-full max-w-md">
        {children}
      </main>
    </div>
  );
}
