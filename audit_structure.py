#!/usr/bin/env python3
"""
LinkOps Structure Audit Script
Verifies that the project structure is clean and properly organized.
"""

import os
import sys
from pathlib import Path

def check_file_exists(path, description):
    """Check if a file exists and report status."""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_directory_structure(path, description):
    """Check if a directory exists and report status."""
    exists = os.path.isdir(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_backend_structure():
    """Audit backend structure."""
    print("\n🔧 BACKEND STRUCTURE AUDIT")
    print("=" * 50)
    
    checks = [
        # FastAPI entrypoint
        ("backend/main.py", "FastAPI entrypoint"),
        
        # Core directories
        ("backend/core", "Core logic directory"),
        ("backend/core/api", "API routes directory"),
        ("backend/core/db", "Database layer directory"),
        ("backend/core/logic", "Business logic directory"),
        
        # Configuration
        ("backend/config", "Configuration directory"),
        ("backend/config/settings.py", "Settings file"),
        ("backend/config/database.py", "Database config"),
        ("backend/config/kafka.py", "Kafka config"),
        
        # Models and schemas
        ("backend/models", "Data models directory"),
        ("backend/routes", "Additional routes directory"),
        ("backend/utils", "Utility functions directory"),
        
        # Database migrations
        ("backend/migrations", "Database migrations directory"),
        ("backend/alembic.ini", "Alembic configuration"),
        
        # Tests and scripts
        ("backend/tests", "Test files directory"),
        ("backend/scripts", "Utility scripts directory"),
        
        # Dependencies
        ("backend/requirements.txt", "Python dependencies"),
        ("backend/Dockerfile", "Backend Dockerfile"),
    ]
    
    passed = 0
    total = len(checks)
    
    for path, description in checks:
        if check_file_exists(path, description) or check_directory_structure(path, description):
            passed += 1
    
    return passed, total

def check_frontend_structure():
    """Audit frontend structure."""
    print("\n🎨 FRONTEND STRUCTURE AUDIT")
    print("=" * 50)
    
    checks = [
        # Vue entrypoint
        ("frontend/src/main.js", "Vue entrypoint"),
        ("frontend/src/App.vue", "Main Vue component"),
        
        # Vue directories
        ("frontend/src/views", "Vue page components"),
        ("frontend/src/components", "Vue reusable components"),
        ("frontend/src/router", "Vue Router configuration"),
        ("frontend/src/stores", "Pinia state management"),
        ("frontend/src/assets", "Static assets"),
        
        # Configuration
        ("frontend/package.json", "Node.js dependencies"),
        ("frontend/vite.config.js", "Vite configuration"),
        ("frontend/tailwind.config.js", "Tailwind CSS config"),
        ("frontend/Dockerfile", "Frontend Dockerfile"),
        
        # Static files
        ("frontend/index.html", "HTML entry point"),
        ("frontend/public", "Public assets directory"),
    ]
    
    passed = 0
    total = len(checks)
    
    for path, description in checks:
        if check_file_exists(path, description) or check_directory_structure(path, description):
            passed += 1
    
    return passed, total

def check_docker_configuration():
    """Audit Docker configuration."""
    print("\n🐳 DOCKER CONFIGURATION AUDIT")
    print("=" * 50)
    
    checks = [
        ("docker-compose.yml", "Docker Compose file"),
    ]
    
    passed = 0
    total = len(checks)
    
    for path, description in checks:
        if check_file_exists(path, description):
            passed += 1
    
    # Check docker-compose.yml content
    if os.path.exists("docker-compose.yml"):
        with open("docker-compose.yml", "r") as f:
            content = f.read()
            if "context: ./backend" in content:
                print("✅ Backend context correctly set to ./backend")
                passed += 1
            else:
                print("❌ Backend context not set to ./backend")
            
            if "context: ./frontend" in content:
                print("✅ Frontend context correctly set to ./frontend")
                passed += 1
            else:
                print("❌ Frontend context not set to ./frontend")
            
            total += 2
    
    return passed, total

def check_cleanup():
    """Check that unwanted files are removed."""
    print("\n🧹 CLEANUP VERIFICATION")
    print("=" * 50)
    
    unwanted_files = [
        "main.py",  # Should only be in backend/
        "requirements.txt",  # Should only be in backend/
        "alembic.ini",  # Should only be in backend/
        "Dockerfile",  # Should only be in backend/ and frontend/
        "App.js",  # React file, should be removed
        "index.js",  # React file, should be removed
        "router.js",  # Duplicate router, should be removed
    ]
    
    passed = 0
    total = len(unwanted_files)
    
    for file in unwanted_files:
        if not os.path.exists(file):
            print(f"✅ {file} - Not found in root (good)")
            passed += 1
        else:
            print(f"❌ {file} - Still exists in root (should be removed)")
    
    return passed, total

def check_duplicate_directories():
    """Check for duplicate or nested directories."""
    print("\n🔍 DUPLICATE DIRECTORY CHECK")
    print("=" * 50)
    
    suspicious_paths = [
        "backend/backend",
        "backend/core/core",
        "frontend/frontend",
        "frontend/src/src",
    ]
    
    passed = 0
    total = len(suspicious_paths)
    
    for path in suspicious_paths:
        if not os.path.exists(path):
            print(f"✅ {path} - Not found (good)")
            passed += 1
        else:
            print(f"❌ {path} - Found (potential duplicate)")
    
    return passed, total

def main():
    """Run the complete audit."""
    print("🔍 LINKOPS STRUCTURE AUDIT")
    print("=" * 60)
    
    total_passed = 0
    total_checks = 0
    
    # Run all audits
    backend_passed, backend_total = check_backend_structure()
    frontend_passed, frontend_total = check_frontend_structure()
    docker_passed, docker_total = check_docker_configuration()
    cleanup_passed, cleanup_total = check_cleanup()
    duplicate_passed, duplicate_total = check_duplicate_directories()
    
    # Calculate totals
    total_passed = backend_passed + frontend_passed + docker_passed + cleanup_passed + duplicate_passed
    total_checks = backend_total + frontend_total + docker_total + cleanup_total + duplicate_total
    
    # Summary
    print("\n📊 AUDIT SUMMARY")
    print("=" * 60)
    print(f"Backend Structure: {backend_passed}/{backend_total} ✅")
    print(f"Frontend Structure: {frontend_passed}/{frontend_total} ✅")
    print(f"Docker Configuration: {docker_passed}/{docker_total} ✅")
    print(f"Cleanup Verification: {cleanup_passed}/{cleanup_total} ✅")
    print(f"Duplicate Check: {duplicate_passed}/{duplicate_total} ✅")
    print(f"\nOverall: {total_passed}/{total_checks} checks passed")
    
    if total_passed == total_checks:
        print("\n🎉 All checks passed! Structure is clean and properly organized.")
        return 0
    else:
        print(f"\n⚠️  {total_checks - total_passed} issues found. Please review and fix.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 