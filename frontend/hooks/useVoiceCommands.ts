import { useRouter } from "next/navigation";
import { routeIntent } from "../lib/intentParser";
import { IntentResponse } from "../types/api";

export function useVoiceCommands() {
  const router = useRouter();

  const handleIntent = (
    intentData: IntentResponse,
    readLesson: () => void,
    stopReading: () => void,
    startQuiz: () => void,
    submitCode: () => void,
    speakHelp: () => void,
    repeatLast: () => void,
    logout: () => void
  ) => {
    routeIntent(
      intentData,
      (path) => router.push(path),
      readLesson,
      stopReading,
      startQuiz,
      submitCode,
      logout,
      speakHelp,
      repeatLast
    );
  };

  return { handleIntent };
}
