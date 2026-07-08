from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User
from app.models.progress import Progress
from app.models.lesson import Lesson
from app.models.knowledge_profile import KnowledgeProfile
from app.services.auth_service import get_current_user
from app.ai.adaptive_engine import get_next_recommendation
from app.ai.progress_predictor import predict_student_completion

router = APIRouter(prefix="/progress", tags=["progress"])

@router.get("")
def get_student_progress_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Calculate overall completion percentage
        total_lessons = db.query(Lesson).count() or 15
        completed_lessons = db.query(Progress).filter(
            Progress.user_id == current_user.id,
            Progress.status == "completed"
        ).count()
        
        overall_pct = (completed_lessons / total_lessons) * 100.0
        
        # Load KnowledgeProfile mastery scores
        profiles = db.query(KnowledgeProfile).filter(
            KnowledgeProfile.user_id == current_user.id
        ).all()
        
        knowledge_profile_dict = {p.topic: float(p.mastery_score) for p in profiles}
        
        # Call Logistic Regression completion predictor ML model
        try:
            prediction = predict_student_completion(db, current_user.id)
        except Exception as pred_e:
            print(f"Prediction fallback due to error: {pred_e}")
            prediction = {"completion_probability": 50.0, "at_risk": False}
        
        # Build Spoken Summary
        # Find strongest topic
        strongest_topic = ""
        strongest_val = -1.0
        weak_topics = []
        for topic, val in knowledge_profile_dict.items():
            if val > strongest_val:
                strongest_val = val
                strongest_topic = topic
            if val < 60.0:
                weak_topics.append(topic)
                
        spoken_summary = f"You have completed {completed_lessons} out of {total_lessons} lessons, which is {int(overall_pct)} percent of the course. "
        if strongest_topic:
            spoken_summary += f"Your strongest topic is {strongest_topic} at {int(strongest_val)} percent mastery. "
        if weak_topics:
            spoken_summary += f"The topics needing review are {', '.join(weak_topics)}. "
        else:
            spoken_summary += "You have solid mastery across all studied topics. "
            
        spoken_summary += f"Your predicted probability of completing this course is {prediction['completion_probability']} percent."
        
        return {
            "user_id": current_user.id,
            "overall_completion": round(overall_pct, 1),
            "lessons_completed": completed_lessons,
            "lessons_total": total_lessons,
            "knowledge_profile": knowledge_profile_dict,
            "completion_prediction": prediction["completion_probability"],
            "at_risk": prediction["at_risk"],
            "spoken_summary": spoken_summary
        }
    except Exception as e:
        print(f"Progress summary endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommend")
def get_recommend(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        recommendation = get_next_recommendation(db, current_user.id)
        
        # Map lesson object to dict
        lesson = recommendation["recommended_lesson"]
        lesson_data = {
            "id": lesson.id,
            "title": lesson.title,
            "topic": lesson.topic,
            "difficulty": lesson.difficulty
        }
        
        return {
            "recommended_lesson": lesson_data,
            "reason": recommendation["reason"],
            "spoken_recommendation": recommendation["spoken_recommendation"]
        }
    except Exception as e:
        print(f"Recommend endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
