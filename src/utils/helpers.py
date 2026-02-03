"""
Utility helper functions
Provides validation and formatting utilities for the monolith
"""
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
import os


def validate_third_party_framework(config: Any) -> Dict[str, Any]:
    """
    Validate third-party framework configuration
    
    Args:
        config: Framework configuration dictionary
        
    Returns:
        Dictionary with validation results
    """
    if config is None:
        return {
            'valid': False,
            'error': 'Configuration is None',
            'issues': ['Configuration cannot be None']
        }
    
    if not isinstance(config, dict):
        return {
            'valid': False,
            'error': 'Configuration must be a dictionary',
            'issues': ['Configuration must be a dictionary']
        }
    
    issues = []
    required_keys = ['name', 'version', 'validation_rules']
    
    # Check for required keys
    for key in required_keys:
        if key not in config:
            issues.append(f'Missing required key: {key}')
    
    # Get framework name
    framework_name = config.get('name', 'Unknown')
    
    # Validate version format
    if 'version' in config:
        if not isinstance(config['version'], str) or not config['version'].strip():
            issues.append('version must be a non-empty string')
    
    # Validate validation_rules
    if 'validation_rules' in config:
        rules = config['validation_rules']
        if isinstance(rules, list) and len(rules) == 0:
            issues.append('validation_rules list is empty')
        # Dict-based rules are also acceptable
    
    return {
        'valid': len(issues) == 0,
        'framework_name': framework_name,
        'issues': issues
    }


def validate_documentation_structure(path: Any) -> Dict[str, Any]:
    """
    Validate documentation structure
    
    Args:
        path: Path to documentation directory
        
    Returns:
        Dictionary with validation results
    """
    if path is None:
        return {
            'valid': False,
            'error': 'Path is None',
            'issues': ['Path cannot be None']
        }
    
    if not os.path.exists(path):
        return {
            'valid': False,
            'error': 'Path does not exist',
            'issues': ['Path does not exist']
        }
    
    if not os.path.isdir(path):
        return {
            'valid': False,
            'error': 'Path is not a directory',
            'issues': ['Path is not a directory']
        }
    
    issues = []
    required_docs = ['ARCHITECTURE.md', 'USER_GUIDE.md']
    found_docs = []
    missing_docs = []
    
    # List all markdown files
    md_files = [f for f in os.listdir(path) if f.endswith('.md')]
    
    # Check for required documentation
    for doc in required_docs:
        doc_path = os.path.join(path, doc)
        if os.path.exists(doc_path):
            found_docs.append(doc)
            # Check if file is empty
            if os.path.getsize(doc_path) == 0:
                issues.append(f'{doc} is empty')
        else:
            missing_docs.append(doc)
            issues.append(f'Missing required documentation: {doc}')
    
    return {
        'valid': len(issues) == 0,
        'found_docs': found_docs,
        'missing_docs': missing_docs,
        'total_md_files': len(md_files),
        'issues': issues
    }


def validate_fact_data(data: Dict[str, Any]) -> bool:
    """
    Validate fact data structure
    
    Args:
        data: Fact data dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_keys = ['id', 'category', 'statement', 'verified', 'timestamp', 'tags']
    return all(key in data for key in required_keys)


def serialize_datetime(dt: datetime) -> str:
    """
    Serialize datetime to ISO format string
    
    Args:
        dt: Datetime object to serialize
        
    Returns:
        ISO formatted datetime string
    """
    return dt.isoformat()


def format_report(data: Dict[str, Any], title: str = "Report") -> str:
    """
    Format data as a readable report
    
    Args:
        data: Data dictionary to format
        title: Report title
        
    Returns:
        Formatted report string
    """
    lines = [
        "=" * 50,
        title,
        "=" * 50,
        ""
    ]
    
    def format_value(value: Any, indent: int = 0) -> List[str]:
        """Recursively format values"""
        prefix = "  " * indent
        result = []
        
        if isinstance(value, dict):
            for k, v in value.items():
                if isinstance(v, dict):
                    result.append(f"{prefix}{k}:")
                    result.extend(format_value(v, indent + 1))
                else:
                    result.append(f"{prefix}{k}: {v}")
        else:
            result.append(f"{prefix}{value}")
        
        return result
    
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{key}:")
            lines.extend(format_value(value, 1))
        else:
            lines.append(f"{key}: {value}")
    
    lines.append("")
    lines.append("=" * 50)
    
    return "\n".join(lines)
