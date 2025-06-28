#!/usr/bin/env python3
"""
Fix remaining flake8 issues
"""

import re


def fix_file(file_path, fixes):
    """Apply fixes to a file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    for line_num, fix_func in fixes.items():
        if line_num < len(lines):
            lines[line_num - 1] = fix_func(lines[line_num - 1])
    
    with open(file_path, 'w') as f:
        f.write('\n'.join(lines))


def fix_settings_py():
    """Fix settings.py"""
    fixes = {
        48: lambda line: line.replace(
            'description="Application name")',
            'description="Application name"\n    )'
        ),
        52: lambda line: line.replace(
            'print("WARNING: OPENAI_API_KEY not set. LLM functionality will be limited.")',
            'print(\n        "WARNING: OPENAI_API_KEY not set. "\n        "LLM functionality will be limited."\n    )'
        )
    }
    fix_file('backend/core/config/settings.py', fixes)


def fix_seed_whis_py():
    """Fix seed_whis.py"""
    fixes = {
        13: lambda line: line.replace(
            '"orb_description": (',
            '"orb_description": (\n            '
        ),
        14: lambda line: line.replace(
            '"Use `mlflow.sklearn.autolog()` to track all model metrics and "',
            '"Use `mlflow.sklearn.autolog()` to track all model metrics and "\n            '
        )
    }
    fix_file('backend/core/db/seed_whis.py', fixes)


def main():
    """Main function"""
    fix_settings_py()
    fix_seed_whis_py()
    print("Fixed remaining flake8 issues")


if __name__ == "__main__":
    main() 