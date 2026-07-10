from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User
from app.models.lesson import Lesson
from app.models.code_submission import CodeSubmission
from app.services.auth_service import get_current_user
from app.services.code_sandbox import execute_code_safely
from app.ai.code_analyzer import analyze_student_code

router = APIRouter(prefix="/code", tags=["code"])

class CodeExecuteRequest(BaseModel):
    code: str
    language: str = "python"
    lesson_id: Optional[int] = None

class CodeAnalyzeRequest(BaseModel):
    code: str
    execution_error: Optional[str] = None
    lesson_id: Optional[int] = None

@router.post("/execute")
def execute_code(
    req: CodeExecuteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Run code in sandbox
        result = execute_code_safely(req.code, req.language)
        
        # Save submission record (preliminary execution result)
        sub = CodeSubmission(
            user_id=current_user.id,
            lesson_id=req.lesson_id,
            code=req.code,
            language=req.language,
            execution_output=result["stdout"],
            execution_errors=result["stderr"],
            exit_code=result["exit_code"],
            execution_time_ms=result["execution_time_ms"]
        )
        db.add(sub)
        db.commit()
        
        return result
    except Exception as e:
        print(f"Code execute endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
def analyze_code(
    req: CodeAnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Get lesson context if available
        rag_context = "No specific lesson context."
        if req.lesson_id:
            lesson = db.query(Lesson).filter(Lesson.id == req.lesson_id).first()
            if lesson:
                rag_context = lesson.content

        # Call Gemini to get plain-text analysis of error
        analysis = analyze_student_code(req.code, req.execution_error, rag_context)
        
        # Find the last submission and attach the AI explanation
        last_sub = db.query(CodeSubmission).filter(
            CodeSubmission.user_id == current_user.id,
            CodeSubmission.code == req.code
        ).order_by(CodeSubmission.submitted_at.desc()).first()
        
        if last_sub:
            last_sub.ai_analysis = analysis.get("spoken_summary")
            db.commit()
            
        return analysis
    except Exception as e:
        print(f"Code analyze endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
