#!/usr/bin/env python3
"""
Validator for Agent 2a NetLogo Interface Widget JSON output
Validates against the schema and provides detailed error reporting
"""

import json
import jsonschema
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

# Schema path
SCHEMA_PATH = Path(__file__).parent / "agent_2a_widget_schema.json"

# Allowed widget types
ALLOWED_WIDGET_TYPES = {
    "Button", "Slider", "Switch", "Chooser", "Input", 
    "Monitor", "Plot", "Output", "Note"
}

def load_schema() -> Dict[str, Any]:
    """Load the JSON schema for validation."""
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_widget_json(data: Any, schema: Optional[Dict[str, Any]] = None) -> Tuple[bool, List[str]]:
    """
    Validate widget JSON data against schema.
    
    Args:
        data: JSON data to validate (can be string, dict, or list)
        schema: Optional schema dict; if None, loads from file
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Load schema if not provided
    if schema is None:
        try:
            schema = load_schema()
        except Exception as e:
            errors.append(f"Failed to load schema: {e}")
            return False, errors
    
    # Parse JSON if string
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON: {e}")
            return False, errors
    
    # Validate against schema
    try:
        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as e:
        errors.append(f"Schema validation error: {e.message}")
        if e.path:
            errors.append(f"  Path: {' -> '.join(str(p) for p in e.path)}")
    except Exception as e:
        errors.append(f"Validation error: {e}")
        return False, errors
    
    # Additional business logic validation
    if isinstance(data, list):
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                errors.append(f"Item {i} is not an object")
                continue
                
            # Check widget type is in allowed set
            widget_type = item.get('type')
            if widget_type and widget_type not in ALLOWED_WIDGET_TYPES:
                errors.append(f"Item {i}: Invalid widget type '{widget_type}'. Allowed: {sorted(ALLOWED_WIDGET_TYPES)}")
            
            # Check required fields are non-empty
            for field in ['type', 'name', 'description']:
                value = item.get(field)
                if not value or (isinstance(value, str) and not value.strip()):
                    errors.append(f"Item {i}: Field '{field}' is empty or missing")
    
    return len(errors) == 0, errors

def validate_file(file_path: Path) -> Tuple[bool, List[str]]:
    """Validate a JSON file containing widget data."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return validate_widget_json(data)
    except Exception as e:
        return False, [f"File read error: {e}"]

def main():
    """CLI for validating widget JSON files."""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python validate_agent_2a_widgets.py <json_file>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist")
        sys.exit(1)
    
    is_valid, errors = validate_file(file_path)
    
    if is_valid:
        print("✓ JSON is valid")
        sys.exit(0)
    else:
        print("✗ JSON validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()
