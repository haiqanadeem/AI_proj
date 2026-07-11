import { IntentResponse } from "../types/api";
import { INTENTS } from "./constants";

export function routeIntent(
  intentData: IntentResponse,
  navigate: (path: string) => void,
  readLesson: () => void,
  stopReading: () => void,
  startQuiz: () => void,
  submitCode: () => void,
  logout: () => void,
  speakHelp: () => void,
  repeatLast: () => void
) {
  const { intent, params } = intentData;

  switch (intent) {
    case INTENTS.NAVIGATE_HOME:
    case INTENTS.NAVIGATE_DASHBOARD:
      navigate("/dashboard");
      break;
    case INTENTS.NAVIGATE_LESSONS:
      navigate("/lessons");
      break;
    case INTENTS.NAVIGATE_QUIZ:
      if (params?.lesson_id) navigate(`/quiz/${params.lesson_id}`);
      else startQuiz();
      break;
    case INTENTS.OPEN_LESSON:
      if (params?.lesson_id) navigate(`/lessons/${params.lesson_id}`);
      else navigate("/lessons");
      break;
    case INTENTS.NEXT_LESSON:
      navigate("/lessons");
      break;
    case INTENTS.PREVIOUS_LESSON:
      navigate("/lessons");
      break;
    case INTENTS.START_QUIZ:
      startQuiz();
      break;
    case INTENTS.READ_LESSON:
      readLesson();
      break;
    case INTENTS.STOP_READING:
      stopReading();
      break;
    case INTENTS.ASK_TUTOR:
      navigate("/tutor");
      break;
    case INTENTS.SUBMIT_CODE:
      submitCode();
      break;
    case INTENTS.EVALUATE_PROGRESS:
      navigate("/progress");
      break;
    case INTENTS.LOGOUT:
      logout();
      break;
    case INTENTS.HELP:
      speakHelp();
      break;
    case INTENTS.REPEAT_LAST:
      repeatLast();
      break;
    default:
      console.warn("Unknown intent:", intent);
      break;
  }
}
