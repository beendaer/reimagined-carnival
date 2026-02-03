"""
FastAPI application for TAAS validation service
Provides authenticated API endpoints for text validation
"""
import hmac
import os
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from src.main import validate_input

# Initialize FastAPI app
app = FastAPI(
    title="TAAS Validation API",
    description="Testing as a Service - Text Validation API with Authentication",
    version="1.0.0"
)

# API Key authentication
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Verify API key from request header
    
    Args:
        api_key: API key from x-api-key header
        
    Returns:
        The validated API key
        
    Raises:
        HTTPException: If API key is invalid or missing
    """
    expected_key = os.getenv("API_KEY")
    
    if not expected_key:
        raise HTTPException(
            status_code=500,
            detail="API key not configured on server"
        )

    if not api_key or not hmac.compare_digest(api_key, expected_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
    
    return api_key


@app.get("/")
def root():
    """Root endpoint - API information"""
    return {
        "service": "TAAS Validation API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": ["/validate", "/docs"]
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/validate", dependencies=[Depends(verify_api_key)])
def validate_text(request: dict):
    """
    Validate text for coherence and quality
    
    Requires API key authentication via x-api-key header
    
    Args:
        request: Dictionary containing:
            - input_text: The text to validate
            - context: Optional context for validation
            
    Returns:
        Dictionary with validation results including coherence score,
        noise detection, and deception analysis
        
    Raises:
        HTTPException: If validation fails or request is malformed
    """
    try:
        text = request.get("input_text", "")
        context = request.get("context")
        result = validate_input(text, context=context)
        return {"validation": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
