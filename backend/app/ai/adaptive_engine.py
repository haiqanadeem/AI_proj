from sqlalchemy.orm import Session
from app.models.lesson import Lesson
from app.models.progress import Progress
from app.models.quiz import QuizAttempt
from app.models.knowledge_profile import KnowledgeProfile
from app.models.code_submission import CodeSubmission

def update_student_mastery(db: Session, user_id: int, topic: str):
    # Get all lessons for this topic
    lessons = db.query(Lesson).filter(Lesson.topic == topic).all()
    if not lessons:
        return
        
    lesson_ids = [l.id for l in lessons]
    
    # 1. Quiz performance (60% weight)
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == user_id,
        QuizAttempt.lesson_id.in_(lesson_ids)
    ).all()
    
    quiz_scores = [float(att.score) for att in attempts if att.score is not None]
    quiz_avg = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0.0
    
    # 2. Lesson completion rate (30% weight)
    progress_records = db.query(Progress).filter(
        Progress.user_id == user_id,
        Progress.lesson_id.in_(lesson_ids)
    ).all()
    
    completions = [1.0 if prg.status == "completed" else 0.0 for prg in progress_records]
    # pad with zeros for unstarted lessons in the topic
    unstarted_count = max(0, len(lessons) - len(progress_records))
    completions.extend([0.0] * unstarted_count)
    completion_rate = sum(completions) / len(lessons) if lessons else 0.0
    
    # 3. Error-free code rate (10% weight)
    submissions = db.query(CodeSubmission).filter(
        CodeSubmission.user_id == user_id,
        CodeSubmission.lesson_id.in_(lesson_ids)
    ).all()
    
    errors = [1.0 if (sub.exit_code != 0 or sub.execution_errors) else 0.0 for sub in submissions]
    error_free_rate = 1.0 - (sum(errors) / len(errors)) if errors else 1.0
    
    # Formula: mastery = (quiz_avg * 0.6) + (completion_rate * 30) + (error_free_rate * 10)
    # quiz_avg is 0-100, completion_rate is 0-1, error_free_rate is 0-1
    # Let's align all to 0-100
    mastery_score = (quiz_avg * 0.6) + (completion_rate * 100 * 0.3) + (error_free_rate * 100 * 0.1)
    mastery_score = round(min(max(mastery_score, 0.0), 100.0), 2)
    
    # Update or insert KnowledgeProfile
    profile = db.query(KnowledgeProfile).filter(
        KnowledgeProfile.user_id == user_id,
        KnowledgeProfile.topic == topic
    ).first()
    
    if not profile:
        profile = KnowledgeProfile(
            user_id=user_id,
            topic=topic,
            mastery_score=mastery_score,
            quiz_avg=round(quiz_avg, 2),
            attempts_count=len(attempts)
        )
        db.add(profile)
    else:
        profile.mastery_score = mastery_score
        profile.quiz_avg = round(quiz_avg, 2)
        profile.attempts_count = len(attempts)
        
    db.commit()
    return mastery_score

def get_next_recommendation(db: Session, user_id: int) -> dict:
    # 1. Find weak topics (mastery < 60%)
    profiles = db.query(KnowledgeProfile).filter(
        KnowledgeProfile.user_id == user_id
    ).all()
    
    weak_profiles = [p for p in profiles if p.mastery_score < 60.0]
    
    if weak_profiles:
        # Recommend lowest-mastery topic first
        weakest = min(weak_profiles, key=lambda x: x.mastery_score)
        # Find first uncompleted or lowest order lesson in this topic
        lessons = db.query(Lesson).filter(Lesson.topic == weakest.topic).order_by(Lesson.order_index).all()
        for lesson in lessons:
            prog = db.query(Progress).filter(
                Progress.user_id == user_id,
                Progress.lesson_id == lesson.id
            ).first()
            if not prog or prog.status != "completed":
                return {
                    "recommended_lesson": lesson,
                    "reason": f"Your mastery of {weakest.topic} is {weakest.mastery_score}% — below the 60% target. Reviewing this will strengthen your foundation.",
                    "spoken_recommendation": f"Based on your progress, I recommend reviewing {weakest.topic}. You scored {int(weakest.mastery_score)} percent mastery there. Say, Open {lesson.title} Lesson, to continue."
                }
                
    # 2. Otherwise, recommend next unstarted/in_progress lesson in sequence
    # Get all completed lessons
    completed_progress = db.query(Progress).filter(
        Progress.user_id == user_id,
        Progress.status == "completed"
    ).all()
    completed_ids = [p.lesson_id for p in completed_progress]
    
    # Get next lesson by order_index that is not completed
    next_lesson = db.query(Lesson).filter(
        ~Lesson.id.in_(completed_ids) if completed_ids else True
    ).order_by(Lesson.order_index).first()
    
    if next_lesson:
        return {
            "recommended_lesson": next_lesson,
            "reason": f"Ready for the next step! Recommended: {next_lesson.title}.",
            "spoken_recommendation": f"Great work! Based on your progress, I recommend studying {next_lesson.title} next. Say, Open {next_lesson.title} Lesson, to continue."
        }
    else:
        # All lessons completed!
        # Recommend reviewing first lesson or return completion
        first_lesson = db.query(Lesson).order_by(Lesson.order_index).first()
        return {
            "recommended_lesson": first_lesson,
            "reason": "You have completed all 15 lessons! Review any topic to keep your skills sharp.",
            "spoken_recommendation": "Congratulations! You have completed all fifteen lessons in the course. You can review any topic to keep your skills sharp."
        }
