"""
FastAPI wrapper for TAAS validation service.
Exposes HTTP endpoint for coherence and noise validation.
"""

import os
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

from .main import validate_input

app = FastAPI(title="TAAS Validation Service", version="1.0.0")


class ValidationRequest(BaseModel):
    """Request payload for validation."""
    input_text: str
    context: Optional[str] = None


class ValidationResponse(BaseModel):
    """Response payload for validation."""
    coherence_score: float
    noise_detected: bool
    validation_passed: bool
    details: dict


def verify_api_key(api_key: Optional[str] = Header(default=None, alias="X-API-KEY")):
    """Dependency to verify API key from header."""
    expected_key = os.getenv("API_KEY")
    if not expected_key:
        raise HTTPException(status_code=500, detail="API key not configured")
    if api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "operational", "service": "TAAS Validation"}


@app.post("/validate", dependencies=[Depends(verify_api_key)])
def validate_text(request: dict):
    try:
        text = request.get("text", "")
        context = request.get("context")
        result = validate_input(text, context=context)
        return {"validation": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health():
    """Service health check."""
    return {"status": "healthy"}
