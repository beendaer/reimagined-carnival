"""
Unit tests for utility helper functions
"""
import unittest
import sys
from pathlib import Path
import tempfile
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))
from utils.helpers import (
    validate_third_party_framework,
    validate_documentation_structure,
    validate_fact_data,
    serialize_datetime,
    format_report,
    extract_key_code_segments
)
from datetime import datetime


class TestValidateThirdPartyFramework(unittest.TestCase):
    """Test third-party framework validation"""
    
    def test_validate_framework_with_none(self):
        """Test that None input returns proper error dict, not None"""
        result = validate_third_party_framework(None)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
        self.assertIn('Configuration cannot be None', result['issues'])
    
    def test_validate_framework_with_valid_config(self):
        """Test validation with valid framework configuration"""
        config = {
            'name': 'TestFramework',
            'version': '1.0.0',
            'validation_rules': ['rule1', 'rule2']
        }
        result = validate_third_party_framework(config)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertTrue(result['valid'])
        self.assertEqual(result['framework_name'], 'TestFramework')
        self.assertEqual(len(result['issues']), 0)
    
    def test_validate_framework_with_missing_keys(self):
        """Test validation with missing required keys"""
        config = {'name': 'TestFramework'}
        result = validate_third_party_framework(config)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertFalse(result['valid'])
        self.assertEqual(result['framework_name'], 'TestFramework')
        self.assertGreater(len(result['issues']), 0)
        self.assertIn('Missing required key: version', result['issues'])
        self.assertIn('Missing required key: validation_rules', result['issues'])
    
    def test_validate_framework_with_invalid_version(self):
        """Test validation with invalid version format"""
        config = {
            'name': 'TestFramework',
            'version': 123,  # Should be string
            'validation_rules': ['rule1']
        }
        result = validate_third_party_framework(config)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertFalse(result['valid'])
        self.assertIn('version must be a non-empty string', result['issues'])
    
    def test_validate_framework_with_empty_rules(self):
        """Test validation with empty validation rules"""
        config = {
            'name': 'TestFramework',
            'version': '1.0.0',
            'validation_rules': []
        }
        result = validate_third_party_framework(config)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertFalse(result['valid'])
        self.assertIn('validation_rules list is empty', result['issues'])
    
    def test_validate_framework_with_dict_rules(self):
        """Test validation with dict-based validation rules"""
        config = {
            'name': 'TestFramework',
            'version': '1.0.0',
            'validation_rules': {'rule1': True, 'rule2': False}
        }
        result = validate_third_party_framework(config)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertTrue(result['valid'])


class TestValidateDocumentationStructure(unittest.TestCase):
    """Test documentation structure validation"""
    
    def test_validate_docs_with_none(self):
        """Test that None input returns proper error dict, not None"""
        result = validate_documentation_structure(None)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
        self.assertIn('Path cannot be None', result['issues'])
    
    def test_validate_docs_with_nonexistent_path(self):
        """Test validation with non-existent path"""
        result = validate_documentation_structure('/nonexistent/path')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
        self.assertIn('Path does not exist', result['issues'])
    
    def test_validate_docs_with_file_instead_of_directory(self):
        """Test validation when path points to a file instead of directory"""
        with tempfile.NamedTemporaryFile() as tmp:
            result = validate_documentation_structure(tmp.name)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, dict)
            self.assertFalse(result['valid'])
            self.assertIn('Path is not a directory', result['issues'])
    
    def test_validate_docs_with_valid_structure(self):
        """Test validation with proper documentation structure"""
        # Use the actual docs directory in the project
        docs_path = Path(__file__).parent.parent.parent / 'docs'
        result = validate_documentation_structure(str(docs_path))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertTrue(result['valid'])
        self.assertIn('ARCHITECTURE.md', result['found_docs'])
        self.assertIn('USER_GUIDE.md', result['found_docs'])
        self.assertEqual(len(result['missing_docs']), 0)
        self.assertGreaterEqual(result['total_md_files'], 2)
    
    def test_validate_docs_with_missing_files(self):
        """Test validation with missing required documentation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create only one of the required files
            arch_file = Path(tmpdir) / 'ARCHITECTURE.md'
            arch_file.write_text('# Architecture')
            
            result = validate_documentation_structure(tmpdir)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, dict)
            self.assertFalse(result['valid'])
            self.assertIn('ARCHITECTURE.md', result['found_docs'])
            self.assertIn('USER_GUIDE.md', result['missing_docs'])
            self.assertGreater(len(result['issues']), 0)
    
    def test_validate_docs_with_empty_file(self):
        """Test validation detects empty documentation files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create required files, one empty
            arch_file = Path(tmpdir) / 'ARCHITECTURE.md'
            arch_file.write_text('')  # Empty file
            
            user_file = Path(tmpdir) / 'USER_GUIDE.md'
            user_file.write_text('# User Guide')
            
            result = validate_documentation_structure(tmpdir)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, dict)
            self.assertFalse(result['valid'])
            self.assertIn('ARCHITECTURE.md is empty', result['issues'])


class TestOtherHelpers(unittest.TestCase):
    """Test other helper functions"""
    
    def test_serialize_datetime(self):
        """Test datetime serialization"""
        dt = datetime(2024, 1, 1, 12, 0, 0)
        result = serialize_datetime(dt)
        self.assertIsInstance(result, str)
        self.assertIn('2024-01-01', result)
    
    def test_format_report(self):
        """Test report formatting"""
        data = {'key1': 'value1', 'key2': {'nested': 'value'}}
        result = format_report(data, 'Test Report')
        self.assertIsInstance(result, str)
        self.assertIn('Test Report', result)
        self.assertIn('key1: value1', result)
        self.assertIn('nested: value', result)
    
    def test_validate_fact_data(self):
        """Test fact data validation"""
        valid_data = {
            'id': 'test',
            'category': 'test',
            'statement': 'test',
            'verified': True,
            'timestamp': 'now',
            'tags': []
        }
        self.assertTrue(validate_fact_data(valid_data))
        
        invalid_data = {'id': 'test'}
        self.assertFalse(validate_fact_data(invalid_data))

    def test_extract_key_code_segments_with_filename_context(self):
        """Extracts code using nearby filename mention."""
        history = [
            {
                "tagged_text": {
                    "header": "Extracting from history",
                    "summary": "and extract key code segments from conversation history"
                }
            },
            {"tagged_text": {"summary": "Focus on bbfb_engine.py for extraction."}},
            {"tagged_text": {"summary": "```python\nprint('hello')\n```"}}
        ]

        result = extract_key_code_segments(history)
        self.assertIn("### bbfb_engine.py", result)
        self.assertIn("```python", result)
        self.assertIn("print('hello')", result)

    def test_extract_key_code_segments_with_labeled_block(self):
        """Handles code fences labeled with filename."""
        history = "```utils/helpers.py\n# file: utils/helpers.py\nvalue = 1\n```"
        result = extract_key_code_segments(history)
        self.assertTrue(result.startswith("### utils/helpers.py"))
        self.assertIn("value = 1", result)


if __name__ == '__main__':
    unittest.main()
