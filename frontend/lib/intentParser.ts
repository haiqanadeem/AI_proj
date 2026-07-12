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
  repeatLast: () => void,
  nextLesson: () => void,
  prevLesson: () => void,
  speak: (text: string, force?: boolean) => void
) {
  const { intent, params } = intentData;

  switch (intent) {
    case INTENTS.NAVIGATE_HOME:
    case INTENTS.NAVIGATE_DASHBOARD:
      navigate("/dashboard");
      break;
    case INTENTS.NAVIGATE_CODE_LAB:
      navigate("/code-lab");
      break;
    case INTENTS.NAVIGATE_TUTOR:
      navigate("/tutor");
      break;
    case INTENTS.NAVIGATE_SETTINGS:
      navigate("/settings");
      break;
    case INTENTS.NAVIGATE_REGISTER:
      navigate("/register");
      break;
    case INTENTS.NAVIGATE_LOGIN:
      navigate("/login");
      break;
    case INTENTS.NAVIGATE_LESSONS:
      navigate("/lessons");
      break;
    case INTENTS.NAVIGATE_QUIZ:
      if (params?.lesson_id) navigate(`/quiz/${params.lesson_id}`);
      else startQuiz();
      break;
    case INTENTS.GET_LESSON_NAME:
      import("@/services/endpoints/lessons").then(({ getLessons }) => {
        getLessons().then(data => {
          if (data && data.length > 0) {
            let num = parseInt(params?.lesson_number);
            if (isNaN(num)) {
               speak("I couldn't understand the lesson number.");
               return;
            }
            const lesson = data.find(l => l.order_index === num);
            if (lesson) {
              speak(`The name of lesson ${num} is ${lesson.title}`);
            } else {
              speak(`I couldn't find a lesson number ${num}.`);
            }
          }
        }).catch(err => {
          console.error(err);
          speak("I'm sorry, I couldn't fetch the lesson details.");
        });
      });
      break;
    case INTENTS.LIST_LESSONS:
      import("@/services/endpoints/lessons").then(({ getLessons }) => {
        getLessons().then(data => {
          if (data && data.length > 0) {
            const titles = data.map(l => l.title).join(", ");
            speak(`The available topics are: ${titles}`);
          } else {
            speak("No lessons are currently available.");
          }
        }).catch(err => {
          console.error(err);
          speak("I'm sorry, I couldn't fetch the list of lessons.");
        });
      });
      break;
    case INTENTS.OPEN_LESSON:
      if (params?.lesson_id) navigate(`/lessons/${params.lesson_id}`);
      else navigate("/lessons");
      break;
    case INTENTS.NEXT_LESSON:
      nextLesson();
      break;
    case INTENTS.PREVIOUS_LESSON:
      prevLesson();
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
      if (params?.question) {
        if (typeof window !== "undefined" && window.location.pathname === "/tutor") {
          speak("Asking tutor your question...");
          window.dispatchEvent(new CustomEvent('voice-ask-tutor', { detail: params.question }));
        } else {
          speak("Asking tutor your question...");
          if (typeof window !== "undefined") {
            sessionStorage.setItem("pendingTutorQuery", params.question);
          }
          navigate("/tutor");
        }
      } else {
        speak("Opening tutor");
        navigate("/tutor");
      }
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
    case INTENTS.DICTATE_TEXT:
      if (typeof window !== "undefined") {
        window.dispatchEvent(new CustomEvent('voice-dictate-text', { detail: params }));
      }
      break;
    case INTENTS.FILL_FIELD:
      if (typeof window !== "undefined") {
        window.dispatchEvent(new CustomEvent('voice-fill-field', { detail: params }));
      }
      break;
    case INTENTS.SUBMIT_FORM:
      if (typeof window !== "undefined") {
        window.dispatchEvent(new CustomEvent('voice-submit-form', { detail: params }));
      }
      break;
    default:
      console.warn("Unknown intent:", intent);
      break;
  }
}
