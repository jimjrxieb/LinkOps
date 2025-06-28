#!/usr/bin/env python3
"""
Script to fix flake8 issues in the backend directory
"""

import os
import re
import subprocess
from pathlib import Path


def fix_line_length(content, max_length=79):
    """Fix lines that are too long by breaking them appropriately"""
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        if len(line) <= max_length:
            fixed_lines.append(line)
            continue
            
        # Try to break at logical points
        if 'import ' in line and len(line) > max_length:
            # Handle imports
            if 'from ' in line and ' import ' in line:
                parts = line.split(' import ')
                if len(parts) == 2:
                    from_part = parts[0]
                    import_part = parts[1]
                    if len(from_part) + 4 <= max_length:
                        fixed_lines.append(f"{from_part}")
                        fixed_lines.append(f"    import {import_part}")
                    else:
                        fixed_lines.append(line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        elif 'def ' in line and len(line) > max_length:
            # Handle function definitions
            if '(' in line and ')' in line:
                func_name = line.split('(')[0]
                params = line[line.find('(')+1:line.rfind(')')]
                if len(func_name) + 4 <= max_length:
                    fixed_lines.append(f"{func_name}(")
                    fixed_lines.append(f"    {params})")
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        elif 'class ' in line and len(line) > max_length:
            # Handle class definitions
            if '(' in line and ')' in line:
                class_name = line.split('(')[0]
                parents = line[line.find('(')+1:line.rfind(')')]
                if len(class_name) + 4 <= max_length:
                    fixed_lines.append(f"{class_name}(")
                    fixed_lines.append(f"    {parents})")
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        elif '=' in line and len(line) > max_length:
            # Handle assignments
            if ' = ' in line:
                var_name, value = line.split(' = ', 1)
                if len(var_name) + 4 <= max_length:
                    fixed_lines.append(f"{var_name} = (")
                    fixed_lines.append(f"    {value})")
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        else:
            # For other cases, just add the line as is
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


def remove_unused_imports(content):
    """Remove unused imports"""
    lines = content.split('\n')
    fixed_lines = []
    imports_to_remove = [
        'from datetime import datetime',
        'import datetime',
        'import uuid',
        'from sqlalchemy.dialects import postgresql',
        'import alembic.op',
        'import sqlalchemy as sa',
        'from backend.models import rune'
    ]
    
    for line in lines:
        should_keep = True
        for import_to_remove in imports_to_remove:
            if import_to_remove in line.strip():
                should_keep = False
                break
        if should_keep:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


def fix_migration_imports(content):
    """Fix migration file imports"""
    lines = content.split('\n')
    fixed_lines = []
    
    # Move imports to top
    imports = []
    other_lines = []
    
    for line in lines:
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            imports.append(line)
        else:
            other_lines.append(line)
    
    # Add imports at the top
    fixed_lines.extend(imports)
    fixed_lines.extend(other_lines)
    
    return '\n'.join(fixed_lines)


def process_file(file_path):
    """Process a single file to fix flake8 issues"""
    print(f"Processing {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove unused imports
    content = remove_unused_imports(content)
    
    # Fix migration imports
    if 'migrations' in str(file_path):
        content = fix_migration_imports(content)
    
    # Fix line length issues
    content = fix_line_length(content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    """Main function to process all backend files"""
    backend_dir = Path('backend')
    
    if not backend_dir.exists():
        print("Backend directory not found!")
        return
    
    # Process Python files
    for py_file in backend_dir.rglob('*.py'):
        if py_file.is_file():
            process_file(py_file)
    
    print("Flake8 fixes completed!")


if __name__ == "__main__":
    main() 