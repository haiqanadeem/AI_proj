import { useEffect } from "react";

export function useKeyboardShortcuts(
  toggleVoice: () => void,
  readPage: () => void,
  nextLesson: () => void,
  prevLesson: () => void,
  startQuiz: () => void,
  speakHelp: () => void
) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.altKey) {
        switch (e.key.toLowerCase()) {
          case "v":
            e.preventDefault();
            toggleVoice();
            break;
          case "r":
            e.preventDefault();
            readPage();
            break;
          case "n":
            e.preventDefault();
            nextLesson();
            break;
          case "p":
            e.preventDefault();
            prevLesson();
            break;
          case "q":
            e.preventDefault();
            startQuiz();
            break;
          case "h":
            e.preventDefault();
            speakHelp();
            break;
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [toggleVoice, readPage, nextLesson, prevLesson, startQuiz, speakHelp]);
}
