"""
Unit tests for main module functions
"""
import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from main import validate_input


class TestValidateInput(unittest.TestCase):
    """Test the validate_input function used by the API"""
    
    def test_validate_coherent_input(self):
        """Test validation of coherent input text"""
        result = validate_input(
            "This is a well-formed and coherent statement about software testing"
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn("coherence_score", result)
        self.assertIn("noise_detected", result)
        self.assertIn("validation_passed", result)
        self.assertIn("details", result)
        
        # Coherent text should have high score and pass validation
        self.assertGreater(result["coherence_score"], 0.7)
        self.assertFalse(result["noise_detected"])
        self.assertTrue(result["validation_passed"])
    
    def test_validate_noisy_input(self):
        """Test validation of noisy/low-quality input"""
        result = validate_input("Bad")
        
        self.assertIsInstance(result, dict)
        self.assertIn("coherence_score", result)
        self.assertIn("noise_detected", result)
        self.assertIn("validation_passed", result)
        
        # Noisy text should have low score
        self.assertLess(result["coherence_score"], 0.5)
        self.assertTrue(result["noise_detected"])
        self.assertFalse(result["validation_passed"])

    def test_validate_repetition_noise(self):
        """Test validation of chaotic repetition in input"""
        text = "Oops tissuetissue stop it im not a dickheaddickhead selfself"
        result = validate_input(text)

        self.assertTrue(result["noise_detected"])
        self.assertIn("Repetitive token sequences detected", result["details"]["findings"])
    
    def test_validate_with_context(self):
        """Test validation with context parameter"""
        result = validate_input(
            "Authentication requires valid credentials",
            context="security"
        )
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result["validation_passed"])
        
        # Check that details are provided
        self.assertIn("status", result["details"])
        self.assertIn("findings", result["details"])
        self.assertIn("metadata", result["details"])
    
    def test_validate_empty_input(self):
        """Test validation of empty or very short input"""
        result = validate_input("")
        
        # Empty input should be detected as noise
        self.assertTrue(result["noise_detected"])
        self.assertFalse(result["validation_passed"])
    
    def test_validate_input_non_string_raises(self):
        """Non-string input should raise a clear error"""
        with self.assertRaises(ValueError):
            validate_input(123)
    
    def test_coherence_score_range(self):
        """Test that coherence score is always between 0 and 1"""
        test_inputs = [
            "Bad",
            "This is a test",
            "This is a well-formed statement with good content and coherent structure",
            ""
        ]
        
        for text in test_inputs:
            result = validate_input(text)
            self.assertGreaterEqual(result["coherence_score"], 0.0)
            self.assertLessEqual(result["coherence_score"], 1.0)


if __name__ == "__main__":
    unittest.main()
