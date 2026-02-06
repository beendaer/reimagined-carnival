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

import api
from fastapi.testclient import TestClient
from api import app


class TestAPIEndpoints(unittest.TestCase):
    """Test the FastAPI endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.client = TestClient(app)
        # Set a test API key
        self.test_api_key = "test_api_key_12345"
        api.reset_open_access_warning()
    
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

    def test_gui_get_endpoint(self):
        """Test GUI endpoint renders HTML"""
        response = self.client.get("/gui")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers.get("content-type", ""))
        self.assertIn("Text Feed Testing GUI", response.text)
        self.assertIn("Run Validation", response.text)

    @patch.dict(os.environ, {"ALLOW_OPEN_ACCESS": "true"}, clear=True)
    def test_gui_post_endpoint_with_open_access(self):
        """Test GUI form submission shows results"""
        with self.assertLogs(level="WARNING") as log:
            response = self.client.post(
                "/gui",
                data={
                    "input_text": "This is a coherent test statement",
                    "context": "testing",
                    "api_key": "test_api_key_12345"
                }
            )
            response_followup = self.client.post(
                "/gui",
                data={
                    "input_text": "This is a coherent test statement",
                    "context": "testing",
                    "api_key": "test_api_key_12345"
                }
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_followup.status_code, 200)
        self.assertIn("Action Results", response.text)
        self.assertIn("Validation Output", response.text)
        log_entries = [
            entry for entry in log.output
            if api.OPEN_ACCESS_WARNING_MESSAGE in entry
        ]
        self.assertEqual(len(log.output), 1)
        self.assertEqual(len(log_entries), 1)

    @patch.dict(os.environ, {"API_KEY": "test_api_key_12345"})
    def test_gui_post_endpoint_with_api_key(self):
        """Test GUI form submission with API key shows results"""
        response = self.client.post(
            "/gui",
            data={
                "input_text": "This is a coherent test statement",
                "context": "testing",
                "api_key": "test_api_key_12345"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Action Results", response.text)
        self.assertIn("Validation Output", response.text)

    @patch.dict(os.environ, {"API_KEY": "test_api_key_12345"})
    def test_gui_post_endpoint_without_api_key(self):
        """Test GUI form submission without API key is rejected"""
        response = self.client.post(
            "/gui",
            data={"input_text": "This is a coherent test statement", "context": "testing"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid or missing API key", response.text)
    
    @patch.dict(os.environ, {"API_KEY": "test_api_key_12345"})
    def test_validate_endpoint_without_api_key(self):
        """Test that validate endpoint rejects requests without API key"""
        response = self.client.post(
            "/validate",
            json={"input_text": "This is a test", "context": "testing"}
        )
        self.assertEqual(response.status_code, 401)  # Unauthorized due to missing or invalid header
    
    @patch.dict(os.environ, {"API_KEY": "test_api_key_12345"}, clear=True)
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

    def test_validate_endpoint_with_open_access(self):
        """Test that endpoint accepts requests when open access is enabled"""
        # Ensure API_KEY is not set
        with patch.dict(os.environ, {"ALLOW_OPEN_ACCESS": "true"}, clear=True):
            with self.assertLogs(level="WARNING") as log:
                response = self.client.post(
                    "/validate",
                    json={"input_text": "Test", "context": "testing"},
                    headers={"x-api-key": "invalid_key"}
                )
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertIn("validation", data)
                response = self.client.post(
                    "/validate",
                    json={"input_text": "Test", "context": "testing"}
                )
                self.assertEqual(response.status_code, 200)
            log_entries = [
                entry for entry in log.output
                if api.OPEN_ACCESS_WARNING_MESSAGE in entry
            ]
            self.assertEqual(len(log.output), 1)
            self.assertEqual(len(log_entries), 1)

    @patch.dict(os.environ, {"API_KEY": "test_api_key_12345"})
    def test_process_products_endpoint(self):
        """Test processing RawProductData payloads."""
        response = self.client.post(
            "/api/process-products",
            json=[
                {
                    "make": "Haier",
                    "model": "HWF75AW3",
                    "category": "washing_machine",
                    "price": 454.0,
                    "attributes": {
                        "reliability": 0.94,
                        "performance": 0.90,
                        "efficiency": 0.90
                    }
                }
            ],
            headers={"x-api-key": "test_api_key_12345"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["summary"]["processed"], 1)
        self.assertEqual(data["summary"]["valid"], 1)
        self.assertAlmostEqual(data["results"][0]["bbfb_score"], 0.913, places=3)

    @patch.dict(os.environ, {"API_KEY": "test_api_key_12345"})
    def test_validate_endpoint_rejects_non_string_input(self):
        """Test validation endpoint rejects non-string input_text payloads."""
        payload = {
            "input_text": {"file_system": {"manifest": None}},
            "context": "testing"
        }
        response = self.client.post(
            "/validate",
            json=payload,
            headers={"x-api-key": "test_api_key_12345"}
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("detail", data)
        self.assertEqual(data["detail"], "Input text must be a string")


if __name__ == "__main__":
    unittest.main()
