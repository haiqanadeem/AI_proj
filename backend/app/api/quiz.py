import uuid
from datetime import datetime
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User
from app.models.quiz import QuizAttempt
from app.models.progress import Progress
from app.models.lesson import Lesson
from app.services.auth_service import get_current_user
from app.ai.quiz_generator import generate_quiz_for_topic
from app.ai.adaptive_engine import update_student_mastery, get_next_recommendation

router = APIRouter(prefix="/quiz", tags=["quiz"])

class QuizGenerateRequest(BaseModel):
    topic: str
    difficulty: str
    lesson_id: int

class QuizSubmitRequest(BaseModel):
    lesson_id: int
    quiz_json: dict
    answers: Dict[str, str] # e.g. {"1": "B", "2": "A"}
    time_taken_sec: int

@router.post("/generate")
def generate_quiz(
    req: QuizGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        lesson = db.query(Lesson).filter(Lesson.id == req.lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        
        if not lesson.quiz_json:
            raise HTTPException(status_code=404, detail="Quiz not available for this lesson")
            
        quiz = dict(lesson.quiz_json)
        quiz["quiz_id"] = str(uuid.uuid4())
        return quiz
    except HTTPException:
        raise
    except Exception as e:
        print(f"Quiz generate endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit")
def submit_quiz(
    req: QuizSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        questions = req.quiz_json.get("questions", [])
        if not questions:
            raise HTTPException(status_code=400, detail="Invalid quiz format")
            
        correct_count = 0
        total_questions = len(questions)
        feedback_list = []
        
        for q in questions:
            q_id = str(q.get("id"))
            student_ans = req.answers.get(q_id, "").strip().upper()
            correct_ans = q.get("correct_answer", "").strip().upper()
            
            is_correct = student_ans == correct_ans
            if is_correct:
                correct_count += 1
                
            feedback_list.append({
                "question_id": int(q_id),
                "correct": is_correct,
                "your_answer": student_ans,
                "correct_answer": correct_ans,
                "explanation": q.get("explanation", "")
            })
            
        score = (correct_count / total_questions) * 100.0 if total_questions else 0.0
        passed = score >= 70.0
        
        # 1. Save Quiz Attempt to database
        attempt = QuizAttempt(
            user_id=current_user.id,
            lesson_id=req.lesson_id,
            quiz_json=req.quiz_json,
            answers_json=req.answers,
            score=score,
            passed=passed,
            time_taken_sec=req.time_taken_sec,
            completed_at=datetime.utcnow()
        )
        db.add(attempt)
        db.commit()
        
        # 2. Update Lesson Progress
        progress = db.query(Progress).filter(
            Progress.user_id == current_user.id,
            Progress.lesson_id == req.lesson_id
        ).first()
        
        if not progress:
            progress = Progress(
                user_id=current_user.id,
                lesson_id=req.lesson_id,
                status="completed" if passed else "in_progress",
                completion_pct=100 if passed else 50,
                time_spent_sec=req.time_taken_sec,
                mastery_score=score,
                started_at=datetime.utcnow(),
                completed_at=datetime.utcnow() if passed else None
            )
            db.add(progress)
        else:
            progress.time_spent_sec += req.time_taken_sec
            if passed:
                progress.status = "completed"
                progress.completion_pct = 100
                progress.completed_at = progress.completed_at or progress.started_at
            else:
                progress.status = "in_progress"
                progress.completion_pct = max(progress.completion_pct, 50)
            progress.mastery_score = max(progress.mastery_score, score)
            
        db.commit()
        
        # 3. Update Adaptive Mastery for this topic
        lesson = db.query(Lesson).filter(Lesson.id == req.lesson_id).first()
        topic_name = lesson.topic if lesson else "General"
        update_student_mastery(db, current_user.id, topic_name)
        
        # 4. Get next recommendation
        recommend_data = get_next_recommendation(db, current_user.id)
        
        # 5. Build Spoken feedback summary
        pass_fail_text = "passed" if passed else "did not pass"
        spoken_summary = f"You scored {int(score)} percent and {pass_fail_text}! You got {correct_count} out of {total_questions} questions correct. {recommend_data.get('spoken_recommendation')}"
        
        return {
            "score": score,
            "passed": passed,
            "correct_count": correct_count,
            "total_questions": total_questions,
            "feedback": feedback_list,
            "spoken_summary": spoken_summary
        }
    except Exception as e:
        print(f"Quiz submit endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
