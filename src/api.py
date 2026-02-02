"""
FastAPI wrapper for TAAS validation service.
Exposes HTTP endpoint for coherence and noise validation.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

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


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "operational", "service": "TAAS Validation"}


@app.post("/validate", response_model=ValidationResponse)
async def validate(request: ValidationRequest):
    """
    Validate input text for coherence and noise.
    
    Returns coherence score, noise detection, and validation status.
    """
    try:
        result = validate_input(
            input_text=request.input_text,
            context=request.context
        )
        
        return ValidationResponse(
            coherence_score=result["coherence_score"],
            noise_detected=result["noise_detected"],
            validation_passed=result["validation_passed"],
            details=result.get("details", {})
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Service health check."""
    return {"status": "healthy"}
