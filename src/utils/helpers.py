"""
Utility helper functions
Provides validation and formatting utilities for the monolith
"""
from typing import Dict, Any, List
from datetime import datetime
import os
import re

FILENAME_PATTERN = re.compile(
    r"""
    (?!https?://)                      # avoid matching full URLs
    (?=[A-Za-z0-9_\-./+]*[A-Za-z_])    # require at least one alphabetic character
    [A-Za-z0-9_\-./+]+                 # allow common path characters (including '+')
    \.[A-Za-z][A-Za-z0-9]+             # extension must start with a letter
    """,
    re.VERBOSE,
)
# INLINE_FILE_COMMENT_PATTERN supports:
#   - Python style: # file: path
#   - C/JS style: // file: path
#   - HTML style: <!-- file: path -->
#   - Assembly style: ; file: path
#   - C block style: /* file: path */ or /** file: path */
INLINE_FILE_COMMENT_PATTERN = re.compile(
    r"(?im)^(?:#|//|<!--|;|/\*{1,2})\s*file\s*:\s*([^\s]+)"
)


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


def _collect_text_fragments(value: Any) -> List[str]:
    """Recursively collect string fragments from nested conversation history."""
    fragments: List[str] = []
    if isinstance(value, str):
        fragments.append(value)
    elif isinstance(value, dict):
        for item in value.values():
            fragments.extend(_collect_text_fragments(item))
    elif isinstance(value, list):
        for item in value:
            fragments.extend(_collect_text_fragments(item))
    return fragments


def extract_key_code_segments(history: Any) -> str:
    """
    Extract key code segments from conversation history and format them as Markdown.

    The function looks for fenced code blocks (```), associates them with the
    nearest file name mention, and returns only the Markdown-formatted snippets.

    Args:
        history: Conversation history as a string, list, or dictionary.

    Returns:
        Markdown string containing extracted code snippets grouped by file name.
    """
    if history is None:
        return ""

    # Gather textual content while preserving newlines
    if isinstance(history, str):
        text = history
    else:
        fragments = _collect_text_fragments(history)
        text = "\n".join(fragments)

    code_blocks = list(
        re.finditer(
            r"```(?P<label>[^\n`]*)\n(?P<code>.+?)```", text, re.DOTALL
        )
    )

    if not code_blocks:
        return ""

    segments = []
    snippet_counter = 1
    for match in code_blocks:
        label = match.group("label").strip()
        code = match.group("code").strip()

        file_name = None
        language = None

        # If the fence label looks like a filename, use it. Otherwise treat as language.
        if label:
            label_match = FILENAME_PATTERN.search(label)
            if label_match:
                file_name = label_match.group(0)
            else:
                language = label

        # Try to find explicit file markers inside the code block.
        if not file_name:
            inline_match = INLINE_FILE_COMMENT_PATTERN.search(code)
            if inline_match:
                file_name = inline_match.group(1).strip()

        # Look backwards in the history for the nearest filename mention.
        if not file_name:
            prefix = text[: match.start()]
            filenames = FILENAME_PATTERN.findall(prefix)
            if filenames:
                file_name = filenames[-1]

        if not file_name:
            file_name = f"snippet-{snippet_counter}"
            snippet_counter += 1

        segments.append(
            {"file": file_name, "language": language, "code": code}
        )

    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for segment in segments:
        grouped.setdefault(segment["file"], []).append(segment)

    parts: List[str] = []
    for file_name, snippets in grouped.items():
        for idx, snippet in enumerate(snippets, start=1):
            heading = f"### {file_name}"
            if len(snippets) > 1:
                heading = f"{heading} (part {idx})"
            parts.append(heading)
            fence = f"```{snippet['language']}" if snippet["language"] else "```"
            parts.append(fence)
            parts.append(snippet["code"])
            parts.append("```")
            parts.append("")  # spacer

    return "\n".join(parts).rstrip()
