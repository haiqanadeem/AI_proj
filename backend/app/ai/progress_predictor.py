import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sqlalchemy.orm import Session
from app.models.progress import Progress
from app.models.quiz import QuizAttempt
from app.models.code_submission import CodeSubmission
from app.models.knowledge_profile import KnowledgeProfile
from app.models.lesson import Lesson

# Pre-train a simple logistic regression model on synthetic data on import
# Features: [quiz_avg, completion_rate, code_runs, weak_topics_count]
# Target: 1 = likely to complete course, 0 = at risk

# Synthetic training data
# high quiz score, high completion, high submissions, 0 weak topics -> likely (1)
# low quiz score, low completion, low submissions, 3 weak topics -> at risk (0)
X_train = np.array([
    [90.0, 0.8, 15, 0],
    [85.0, 0.7, 12, 0],
    [40.0, 0.2, 2, 3],
    [50.0, 0.3, 4, 2],
    [95.0, 1.0, 30, 0],
    [30.0, 0.1, 1, 4],
    [75.0, 0.6, 10, 1],
    [60.0, 0.5, 8, 2],
    [20.0, 0.0, 0, 5],
    [80.0, 0.8, 20, 0]
])
y_train = np.array([1, 1, 0, 0, 1, 0, 1, 0, 0, 1])

# Scale and train
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
predictor_model = LogisticRegression()
predictor_model.fit(X_train_scaled, y_train)

def predict_student_completion(db: Session, user_id: int) -> dict:
    # 1. Fetch student features
    # A. Quiz average
    attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).all()
    scores = [float(att.score) for att in attempts if att.score is not None]
    quiz_avg = sum(scores) / len(scores) if scores else 0.0
    
    # B. Lesson completion rate
    total_lessons = db.query(Lesson).count() or 15
    completed_lessons = db.query(Progress).filter(
        Progress.user_id == user_id,
        Progress.status == "completed"
    ).count()
    completion_rate = completed_lessons / total_lessons
    
    # C. Code submission count
    code_runs = db.query(CodeSubmission).filter(CodeSubmission.user_id == user_id).count()
    
    # D. Weak topics count (mastery < 60%)
    profiles = db.query(KnowledgeProfile).filter(
        KnowledgeProfile.user_id == user_id
    ).all()
    weak_topics_count = sum(1 for p in profiles if p.mastery_score < 60.0)
    
    # Pack features
    features = np.array([[
        float(quiz_avg),
        float(completion_rate),
        float(code_runs),
        float(weak_topics_count)
    ]])
    
    # Predict probability
    features_scaled = scaler.transform(features)
    # predict_proba returns [prob_0, prob_1]
    prob_completion = predictor_model.predict_proba(features_scaled)[0][1]
    prob_pct = float(round(prob_completion * 100, 1))
    
    # Recommendations based on risk status
    at_risk = bool(prob_completion < 0.55)
    if at_risk:
        recommendation = "Our predictive model flags you as at risk of struggling. We recommend reviewing weak topics and asking the AI tutor for detailed explanations."
    else:
        recommendation = "You have a high predicted completion rate! Keep up the excellent work."
        
    return {
        "completion_probability": prob_pct,
        "at_risk": at_risk,
        "recommendation": recommendation,
        "features": {
            "quiz_avg": round(quiz_avg, 2),
            "completion_rate": round(completion_rate, 2),
            "code_runs": code_runs,
            "weak_topics_count": weak_topics_count
        }
    }
