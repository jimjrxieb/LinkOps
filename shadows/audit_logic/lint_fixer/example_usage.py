#!/usr/bin/env python3
"""
Example usage of the lint_runner.py script.

This demonstrates how to use the linting and formatting tools
programmatically or from the command line.
"""

from lint_runner import lint_and_fix_repo


def example_programmatic_usage():
    """Example of using the lint runner programmatically."""
    print("🔧 Example: Programmatic Usage")
    print("=" * 50)

    # Example 1: Basic usage
    results = lint_and_fix_repo(path_to_repo=".", max_line_length=88)

    print(f"\nResults: {results}")

    # Example 2: With custom skip patterns
    results = lint_and_fix_repo(
        path_to_repo=".", max_line_length=88, skip_patterns=["test_", "temp_", "draft_"]
    )

    print(f"\nResults with skip patterns: {results}")


def example_command_line_usage():
    """Example of command line usage."""
    print("\n🔧 Example: Command Line Usage")
    print("=" * 50)
    print(
        """
# Basic usage - lint current directory
python lint_runner.py .

# With custom line length
python lint_runner.py . 100

# From a different directory
python lint_runner.py /path/to/your/repo 88

# The script will:
# 1. Run flake8 on all Python files
# 2. Run black formatting on all Python files  
# 3. Run yamllint on all YAML files
# 4. Run prettier formatting on all YAML files
# 5. Provide a summary of results
"""
    )


if __name__ == "__main__":
    example_command_line_usage()

    # Uncomment to run programmatic example
    # example_programmatic_usage()
