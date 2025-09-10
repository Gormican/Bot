from fastapi import APIRouter, HTTPException
from app.models import StudyQuestion
from app.services.study import ask_openai

router = APIRouter(prefix="/study", tags=["study"])

@router.post("/ask")
def ask(q: StudyQuestion):
    try:
        answer = ask_openai(q.question)
        return {"answer": answer}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Study error: {e}")
