export function announceToScreenReader(text: string) {
  if (typeof document !== "undefined") {
    let announcer = document.getElementById("global-aria-live-announcer");
    if (!announcer) {
      announcer = document.createElement("div");
      announcer.id = "global-aria-live-announcer";
      announcer.setAttribute("aria-live", "polite");
      announcer.className = "sr-only";
      document.body.appendChild(announcer);
    }
    announcer.textContent = "";
    setTimeout(() => {
      if (announcer) announcer.textContent = text;
    }, 50);
  }
}

export function generatePageAnnouncement(pageName: string, actions: string[]): string {
  if (actions.length === 0) return `${pageName}.`;
  return `${pageName}. Available actions: ${actions.join(", ")}.`;
}
