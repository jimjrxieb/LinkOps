# shadows/audit_logic/lint_fixer/lint_runner.py

import subprocess
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional


def run_python_lint(path: str, max_line_length: int = 88) -> Dict[str, Any]:
    """Run Python linting and formatting tools."""
    results = {"flake8": False, "black": False}

    print(f"🔎 Running flake8 on {path}...")
    try:
        result = subprocess.run(
            ["flake8", "--max-line-length", str(max_line_length), path],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            print("✅ flake8 passed")
            results["flake8"] = True
        else:
            print(f"⚠️ flake8 found issues:\n{result.stdout}")
    except FileNotFoundError:
        print("❌ flake8 not found. Install with: pip install flake8")

    print(f"🧼 Auto-formatting with black on {path}...")
    try:
        result = subprocess.run(
            ["black", "--line-length", str(max_line_length), path],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            print("✅ black formatting complete")
            results["black"] = True
        else:
            print(f"⚠️ black formatting issues:\n{result.stderr}")
    except FileNotFoundError:
        print("❌ black not found. Install with: pip install black")

    return results


def run_yaml_lint(path: str) -> Dict[str, Any]:
    """Run YAML linting and formatting tools."""
    results = {"yamllint": False, "prettier": False}

    print(f"🔎 Running yamllint on {path}...")
    try:
        result = subprocess.run(
            ["yamllint", path], capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            print("✅ yamllint passed")
            results["yamllint"] = True
        else:
            print(f"⚠️ yamllint found issues:\n{result.stdout}")
    except FileNotFoundError:
        print("❌ yamllint not found. Install with: pip install yamllint")

    print(f"🧼 Auto-formatting YAML using Prettier on {path}...")
    try:
        result = subprocess.run(
            ["prettier", "--write", path], capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            print("✅ prettier formatting complete")
            results["prettier"] = True
        else:
            print(f"⚠️ prettier formatting issues:\n{result.stderr}")
    except FileNotFoundError:
        print("❌ prettier not found. Install with: npm install -g prettier")

    return results


def should_skip_directory(dir_name: str) -> bool:
    """Check if directory should be skipped during linting."""
    skip_dirs = {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        "build",
        "dist",
        ".pytest_cache",
        ".mypy_cache",
    }
    return dir_name in skip_dirs


def lint_and_fix_repo(
    path_to_repo: str,
    max_line_length: int = 88,
    skip_patterns: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Run comprehensive linting and formatting on a repository.

    Args:
        path_to_repo: Path to the repository root
        max_line_length: Maximum line length for Python files
        skip_patterns: List of file patterns to skip

    Returns:
        Dictionary with linting results summary
    """
    if skip_patterns is None:
        skip_patterns = []

    print(f"\n🚨 Starting full lint/fix pass on: {path_to_repo}")
    print(f"📏 Max line length: {max_line_length}")
    print(f"⏭️ Skip patterns: {skip_patterns}\n")

    stats = {
        "python_files": 0,
        "yaml_files": 0,
        "python_success": 0,
        "yaml_success": 0,
        "errors": [],
    }

    repo_path = Path(path_to_repo)
    if not repo_path.exists():
        print(f"❌ Repository path does not exist: {path_to_repo}")
        return stats

    for root, dirs, files in os.walk(path_to_repo):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if not should_skip_directory(d)]

        for file in files:
            full_path = os.path.join(root, file)

            # Check skip patterns
            if any(pattern in full_path for pattern in skip_patterns):
                continue

            if file.endswith(".py"):
                stats["python_files"] += 1
                print(f"\n📄 Processing Python file: {full_path}")
                results = run_python_lint(full_path, max_line_length)
                if results["flake8"] and results["black"]:
                    stats["python_success"] += 1
                else:
                    stats["errors"].append(f"Python linting failed: {full_path}")

            elif file.endswith((".yaml", ".yml")):
                stats["yaml_files"] += 1
                print(f"\n📄 Processing YAML file: {full_path}")
                results = run_yaml_lint(full_path)
                if results["yamllint"] and results["prettier"]:
                    stats["yaml_success"] += 1
                else:
                    stats["errors"].append(f"YAML linting failed: {full_path}")

    # Print summary
    print(f"\n📊 Linting Summary:")
    print(
        f"   Python files: {stats['python_files']} processed, {stats['python_success']} successful"
    )
    print(
        f"   YAML files: {stats['yaml_files']} processed, {stats['yaml_success']} successful"
    )

    if stats["errors"]:
        print(f"\n❌ Errors encountered:")
        for error in stats["errors"]:
            print(f"   - {error}")
    else:
        print(f"\n✅ All files processed successfully!")

    return stats


def main():
    """Main entry point for command line usage."""
    if len(sys.argv) < 2:
        print("Usage: python lint_runner.py <repository_path> [max_line_length]")
        print("Example: python lint_runner.py . 88")
        sys.exit(1)

    repo_path = sys.argv[1]
    max_line_length = int(sys.argv[2]) if len(sys.argv) > 2 else 88

    results = lint_and_fix_repo(repo_path, max_line_length)

    if results["errors"]:
        sys.exit(1)
    else:
        print("\n🎉 Linting and formatting complete!")
        sys.exit(0)


if __name__ == "__main__":
    main()
