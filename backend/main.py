from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from services.ai_service import analyze_code
import json
import os
import uvicorn

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    code: str


@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="El código no puede estar vacío.")
    
    response_text = analyze_code(request.code)
    cleaned = response_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(cleaned)
    except Exception:
        # Si la respuesta no es JSON, devolverla en un campo `result`
        return {"result": cleaned}


if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=os.getenv("FASTAPI_HOST", "0.0.0.0"),
        port=int(os.getenv("FASTAPI_PORT", 8000)),
        reload=True,
    )