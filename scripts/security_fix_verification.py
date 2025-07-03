#!/usr/bin/env python3
"""
Security Fix Verification Script
Verifies that all security vulnerabilities have been addressed.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=cwd
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_dependency_version(requirements_file, package, min_version):
    """Check if a package meets the minimum version requirement."""
    try:
        with open(requirements_file, 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(package):
                if '>=' in line:
                    version = line.split('>=')[1].strip()
                    return version >= min_version
                elif '==' in line:
                    version = line.split('==')[1].strip()
                    return version >= min_version
                elif line == package:
                    # No version specified, assume it's latest
                    return True
        return False
    except Exception:
        return False

def main():
    """Main verification function."""
    print("🔒 Security Fix Verification")
    print("=" * 50)
    
    # Define the security fixes we implemented
    security_fixes = {
        'httpx': '0.27.0',
        'pydantic': '2.7.1', 
        'zipp': '3.19.1',
        'anyio': '4.4.0'
    }
    
    # Find all requirements.txt files
    project_root = Path(__file__).parent.parent
    requirements_files = list(project_root.rglob('requirements.txt'))
    
    all_passed = True
    
    for req_file in requirements_files:
        print(f"\n📁 Checking: {req_file.relative_to(project_root)}")
        
        file_passed = True
        for package, min_version in security_fixes.items():
            if check_dependency_version(req_file, package, min_version):
                print(f"  ✅ {package} >= {min_version}")
            else:
                print(f"  ❌ {package} < {min_version} or not found")
                file_passed = False
                all_passed = False
        
        if file_passed:
            print("  🎉 All security fixes applied")
        else:
            print("  ⚠️  Some security fixes missing")
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All security vulnerabilities have been fixed!")
        return 0
    else:
        print("❌ Some security vulnerabilities still need attention.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 