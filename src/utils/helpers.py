"""
Utility functions for the TAAS monolith
"""
import json
from typing import Any, Dict, List
from datetime import datetime
from pathlib import Path


def serialize_datetime(obj: Any) -> str:
    """Serialize datetime objects to ISO format"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def format_report(data: Dict[str, Any], title: str = "Report") -> str:
    """Format a dictionary as a readable report"""
    lines = [
        "=" * 60,
        f" {title}",
        "=" * 60,
        ""
    ]
    
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{key}:")
            for k, v in value.items():
                lines.append(f"  {k}: {v}")
        else:
            lines.append(f"{key}: {value}")
    
    lines.append("=" * 60)
    return "\n".join(lines)


def validate_fact_data(data: Dict[str, Any]) -> bool:
    """Validate that fact data contains required fields"""
    required_fields = ['id', 'category', 'statement', 'verified', 'timestamp', 'tags']
    return all(field in data for field in required_fields)


def export_to_json(data: Any, filepath: str) -> None:
    """Export data to JSON file with datetime handling"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=serialize_datetime)


def import_from_json(filepath: str) -> Any:
    """Import data from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)


def validate_third_party_framework(framework_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate third-party validation framework configuration.
    
    Args:
        framework_config: Configuration dictionary for the validation framework
        
    Returns:
        Dict containing validation results with 'valid' status and any issues found
    """
    if framework_config is None:
        return {
            'valid': False,
            'error': 'Framework configuration is None',
            'issues': ['Configuration cannot be None']
        }
    
    issues = []
    required_keys = ['name', 'version', 'validation_rules']
    
    # Check required keys
    for key in required_keys:
        if key not in framework_config:
            issues.append(f"Missing required key: {key}")
    
    # Check validation rules if present
    if 'validation_rules' in framework_config:
        rules = framework_config['validation_rules']
        if not isinstance(rules, (list, dict)):
            issues.append("validation_rules must be a list or dict")
        elif isinstance(rules, list) and len(rules) == 0:
            issues.append("validation_rules list is empty")
    
    # Check version format if present
    if 'version' in framework_config:
        version = framework_config['version']
        if not isinstance(version, str) or not version:
            issues.append("version must be a non-empty string")
    
    return {
        'valid': len(issues) == 0,
        'framework_name': framework_config.get('name', 'unknown'),
        'issues': issues,
        'validated_keys': list(framework_config.keys())
    }


def validate_documentation_structure(docs_path: str) -> Dict[str, Any]:
    """
    Validate documentation structure for completeness and consistency.
    
    Args:
        docs_path: Path to the documentation directory
        
    Returns:
        Dict containing validation results with structure information
    """
    if docs_path is None:
        return {
            'valid': False,
            'error': 'Documentation path is None',
            'issues': ['Path cannot be None']
        }
    
    path = Path(docs_path)
    
    if not path.exists():
        return {
            'valid': False,
            'error': f'Documentation path does not exist: {docs_path}',
            'issues': ['Path does not exist']
        }
    
    if not path.is_dir():
        return {
            'valid': False,
            'error': f'Documentation path is not a directory: {docs_path}',
            'issues': ['Path is not a directory']
        }
    
    issues = []
    # Core documentation files (README.md may be in parent directory)
    required_docs = ['ARCHITECTURE.md', 'USER_GUIDE.md']
    found_docs = []
    missing_docs = []
    
    # Check for required documentation files
    for doc in required_docs:
        doc_file = path / doc
        if doc_file.exists():
            found_docs.append(doc)
            # Check if file is not empty
            if doc_file.stat().st_size == 0:
                issues.append(f"{doc} is empty")
        else:
            missing_docs.append(doc)
            issues.append(f"Missing required documentation: {doc}")
    
    # Get all markdown files
    all_md_files = list(path.glob('*.md'))
    
    return {
        'valid': len(missing_docs) == 0 and len(issues) == 0,
        'docs_path': str(path),
        'required_docs': required_docs,
        'found_docs': found_docs,
        'missing_docs': missing_docs,
        'total_md_files': len(all_md_files),
        'issues': issues if issues else []
    }
