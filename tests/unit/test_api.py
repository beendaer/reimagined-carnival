"""
Unit tests for API endpoints
"""
import unittest
import sys
import os
from pathlib import Path
from unittest.mock import patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from fastapi.testclient import TestClient
from api import app


class TestAPIEndpoints(unittest.TestCase):
    """Test the FastAPI endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.client = TestClient(app)
        # Set a test API key
        self.test_api_key = "test_api_key_12345"
    
    def test_root_endpoint(self):
        """Test root endpoint returns service information"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("service", data)
        self.assertIn("version", data)
        self.assertIn("status", data)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
    
    @patch.dict(os.environ, {"API_KEY": "test_api_key_12345"})
    def test_validate_endpoint_without_api_key(self):
        """Test that validate endpoint rejects requests without API key"""
        response = self.client.post(
            "/validate",
            json={"input_text": "This is a test", "context": "testing"}
        )
        # APIKeyHeader with auto_error=True returns 401 when header is missing
        self.assertEqual(response.status_code, 401)
    
    @patch.dict(os.environ, {"API_KEY": "test_api_key_12345"})
    def test_validate_endpoint_with_invalid_api_key(self):
        """Test that validate endpoint rejects requests with invalid API key"""
        response = self.client.post(
            "/validate",
            json={"input_text": "This is a test", "context": "testing"},
            headers={"x-api-key": "wrong_key"}
        )
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertIn("detail", data)
        self.assertEqual(data["detail"], "Invalid or missing API key")
    
    @patch.dict(os.environ, {"API_KEY": "test_api_key_12345"})
    def test_validate_endpoint_with_valid_api_key(self):
        """Test that validate endpoint accepts requests with valid API key"""
        response = self.client.post(
            "/validate",
            json={"input_text": "This is a coherent test statement", "context": "testing"},
            headers={"x-api-key": "test_api_key_12345"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check response structure
        self.assertIn("validation", data)
        validation = data["validation"]
        self.assertIn("coherence_score", validation)
        self.assertIn("noise_detected", validation)
        self.assertIn("validation_passed", validation)
        self.assertIn("deception_detected", validation)
        self.assertIn("details", validation)
    
    @patch.dict(os.environ, {"API_KEY": "test_api_key_12345"})
    def test_validate_endpoint_uses_input_text_parameter(self):
        """Test that validate endpoint correctly uses input_text parameter"""
        response = self.client.post(
            "/validate",
            json={"input_text": "Test message", "context": "api_test"},
            headers={"x-api-key": "test_api_key_12345"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # The validation should have processed the text
        validation = data["validation"]
        self.assertIsNotNone(validation["coherence_score"])
    
    @patch.dict(os.environ, {"API_KEY": "test_api_key_12345"})
    def test_validate_endpoint_with_empty_input(self):
        """Test validation with empty input text"""
        response = self.client.post(
            "/validate",
            json={"input_text": "", "context": "testing"},
            headers={"x-api-key": "test_api_key_12345"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        validation = data["validation"]
        
        # Empty text should be detected as noise
        self.assertTrue(validation["noise_detected"])
        self.assertFalse(validation["validation_passed"])
    
    @patch.dict(os.environ, {"API_KEY": "test_api_key_12345"})
    def test_validate_endpoint_without_context(self):
        """Test validation without context parameter"""
        response = self.client.post(
            "/validate",
            json={"input_text": "This is a test without context"},
            headers={"x-api-key": "test_api_key_12345"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("validation", data)
    
    def test_validate_endpoint_without_api_key_env_var(self):
        """Test that endpoint returns 500 when API_KEY env var is not set"""
        # Ensure API_KEY is not set
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.post(
                "/validate",
                json={"input_text": "Test", "context": "testing"},
                headers={"x-api-key": "any_key"}
            )
            self.assertEqual(response.status_code, 500)
            data = response.json()
            self.assertIn("detail", data)
            self.assertEqual(data["detail"], "API key not configured on server")


if __name__ == "__main__":
    unittest.main()
