"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ThemeToggle } from "./ThemeToggle";
import { useAuth } from "@/contexts/AuthContext";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/lessons", label: "Lessons" },
  { href: "/tutor", label: "AI Tutor" },
  { href: "/code-lab", label: "Code Lab" },
  { href: "/progress", label: "Progress" },
  { href: "/settings", label: "Settings" },
];

export function AppNav() {
  const pathname = usePathname();
  const { logout, isAuthenticated } = useAuth();

  return (
    <nav aria-label="Main navigation" className="w-full bg-card border-b border-border p-4 flex flex-col md:flex-row justify-between items-center shadow-sm gap-4">
      <ul className="flex flex-wrap gap-2 md:gap-4 items-center">
        {links.map((link) => (
          <li key={link.href}>
            <Link
              href={link.href}
              className={`px-3 py-2 rounded-md font-medium text-lg focus:outline-none focus:ring-2 focus:ring-primary ${
                pathname.startsWith(link.href)
                  ? "bg-primary text-primary-foreground"
                  : "hover:bg-muted text-foreground"
              }`}
              aria-current={pathname.startsWith(link.href) ? "page" : undefined}
            >
              {link.label}
            </Link>
          </li>
        ))}
        {isAuthenticated && (
          <li>
            <button
              onClick={logout}
              className="px-3 py-2 rounded-md font-medium text-lg text-destructive hover:bg-destructive/10 focus:outline-none focus:ring-2 focus:ring-destructive"
            >
              Logout
            </button>
          </li>
        )}
      </ul>
      <ThemeToggle />
    </nav>
  );
}
