"use client";

export function SkipLink() {
  return (
    <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-primary text-primary-foreground p-3 rounded z-50 focus:outline-none focus:ring-4 focus:ring-accent font-bold">
      Skip to main content
    </a>
  );
}
