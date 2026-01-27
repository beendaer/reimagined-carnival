"""
Utility functions for the TAAS monolith
"""
import json
from typing import Any, Dict
from datetime import datetime


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
