"""
FastAPI application for TAAS validation service
Provides authenticated API endpoints for text validation
"""
import hmac
import json
import logging
import os
import threading
from html import escape
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, Security, Depends, Form, Body
from fastapi.security import APIKeyHeader
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, field_validator
from src.main import validate_input
from src.services.product_ingestion import evaluate_products, SCORE_FIELDS

# Initialize FastAPI app
app = FastAPI(
    title="TAAS Validation API",
    description="Testing as a Service - Text Validation API with Authentication",
    version="1.0.0"
)

# API Key authentication
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
_OPEN_ACCESS_WARNING_EVENT = threading.Event()
OPEN_ACCESS_WARNING_MESSAGE = (
    "API_KEY is not configured; authentication is disabled for API requests."
)


def is_open_access_enabled() -> bool:
    """Return True when ALLOW_OPEN_ACCESS is set to 1/true/yes/on (case-insensitive)."""
    return os.getenv("ALLOW_OPEN_ACCESS", "").strip().lower() in {"1", "true", "yes", "on"}


def reset_open_access_warning() -> None:
    """Reset the open access warning state (testing utility)."""
    _OPEN_ACCESS_WARNING_EVENT.clear()


class RawProductData(BaseModel):
    """Raw product payload for BBFB processing."""
    make: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    attributes: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("attributes")
    @classmethod
    def validate_attributes(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        for key in SCORE_FIELDS:
            if key not in value:
                continue
            score = value.get(key)
            if not isinstance(score, (int, float)):
                raise ValueError(
                    f'Attribute "{key}" must be a numeric value'
                )
            if not 0.0 <= score <= 1.0:
                raise ValueError(
                    f'Attribute "{key}" value {score} must be between 0.0 and 1.0'
                )
        return value




def validate_api_key_value(api_key: Optional[str]) -> None:
    """Validate the API key value for protected endpoints."""
    expected_key = os.getenv("API_KEY")

    if not expected_key:
        if is_open_access_enabled():
            if not _OPEN_ACCESS_WARNING_EVENT.is_set():
                logging.warning(OPEN_ACCESS_WARNING_MESSAGE)
                _OPEN_ACCESS_WARNING_EVENT.set()
            return
        raise HTTPException(
            status_code=500,
            detail="API key not configured on server"
        )

    if not api_key or not isinstance(api_key, str):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )

    if not hmac.compare_digest(api_key, expected_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )


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
    validate_api_key_value(api_key)
    return api_key


def ensure_string_input(input_text: Any) -> str:
    """Validate that the provided input exists and is a string."""
    if input_text is None:
        # Provide a clear error when the field is missing entirely
        raise ValueError("input_text is required")
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")
    return input_text


def render_gui(
    input_text: str = "",
    context: str = "",
    result: Optional[Dict[str, Any]] = None
) -> str:
    """Render a minimal GUI for text feed testing."""
    escaped_text = escape(input_text or "")
    escaped_context = escape(context or "")
    result_section = ""

    if result is not None:
        actions = []
        if result.get("validation_passed"):
            actions.append("Accepted text feed for testing.")
        else:
            actions.append("Rejected text feed as noise.")
        if result.get("deception_detected"):
            deception_type = result.get("deception_type") or "unknown"
            actions.append(f"Flagged deception pattern: {deception_type}.")
        else:
            actions.append("No deception detected.")

        actions_list = "".join(f"<li>{escape(action)}</li>" for action in actions)
        result_json = escape(json.dumps(result, indent=2))
        result_section = f"""
        <section class="results">
            <h2>Action Results</h2>
            <ul>{actions_list}</ul>
            <h3>Validation Output</h3>
            <pre>{result_json}</pre>
        </section>
        """

    return f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>TAAS Text Feed Testing</title>
        <style>
          body {{ font-family: Arial, sans-serif; margin: 2rem; background: #f6f7fb; }}
          main {{ max-width: 860px; margin: 0 auto; background: white; padding: 2rem;
                 border-radius: 12px; box-shadow: 0 6px 18px rgba(30, 41, 59, 0.08); }}
          h1 {{ margin-top: 0; }}
          label {{ display: block; margin-top: 1rem; font-weight: 600; }}
          textarea, input {{ width: 100%; padding: 0.75rem; margin-top: 0.5rem;
                             border-radius: 6px; border: 1px solid #d5d8e1; }}
          button {{ margin-top: 1.5rem; padding: 0.75rem 1.5rem; border: none;
                   background: #2563eb; color: white; border-radius: 8px;
                   font-weight: 600; cursor: pointer; }}
          .results {{ margin-top: 2rem; padding: 1.5rem; background: #f8fafc;
                     border-radius: 10px; border: 1px solid #e2e8f0; }}
          pre {{ background: #0f172a; color: #e2e8f0; padding: 1rem; border-radius: 8px;
                overflow-x: auto; }}
        </style>
      </head>
      <body>
        <main>
          <h1>Text Feed Testing GUI</h1>
          <p>Submit text to validate coherence and view action results.</p>
          <form method="post">
            <label for="input_text">Input Text</label>
            <textarea id="input_text" name="input_text" rows="6"
              placeholder="Paste a text feed to validate...">{escaped_text}</textarea>
            <label for="context">Context (optional)</label>
            <input id="context" name="context" value="{escaped_context}"
              placeholder="e.g. testing, product, compliance" />
            <label for="api_key">API Key</label>
            <input id="api_key" name="api_key" type="password"
              placeholder="Enter API key for validation" />
            <button type="submit">Run Validation</button>
          </form>
          {result_section}
        </main>
      </body>
    </html>
    """


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


@app.get("/gui", response_class=HTMLResponse)
def gui_form():
    """Serve the text feed testing GUI."""
    return HTMLResponse(render_gui())


@app.post("/gui", response_class=HTMLResponse)
def gui_submit(
    input_text: str = Form(...),
    context: str = Form(""),
    api_key: str = Form("")
):
    """Handle GUI submissions and render validation results."""
    try:
        validated_text = ensure_string_input(input_text)
        validate_api_key_value(api_key)
        result = validate_input(validated_text, context=context or None)
        return HTMLResponse(render_gui(validated_text, context, result))
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


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
        # Empty strings are allowed and handled downstream as noise; missing values are not.
        text = ensure_string_input(request.get("input_text"))
        context = request.get("context")
        result = validate_input(text, context=context)
        return {"validation": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/process-products", dependencies=[Depends(verify_api_key)])
def process_products(
    request: List[RawProductData] = Body(...)
):
    """
    Process RawProductData entries for BBFB evaluation.

    Accepts a JSON array of RawProductData objects. Returns a summary plus
    per-product results with missing field checks and a basic BBFB score.
    """
    products = [product.model_dump() for product in request]
    return evaluate_products(products)
