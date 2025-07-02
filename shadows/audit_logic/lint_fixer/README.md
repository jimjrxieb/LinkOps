# Lint Fixer Tools

This directory contains comprehensive linting and formatting tools for the LinkOps-MLOps project.

## 🛠️ Tools Included

### `lint_runner.py`
A comprehensive Python script that automatically runs linting and formatting tools on your codebase.

**Features:**
- ✅ **flake8** - Python linting with configurable line length (default: 88)
- ✅ **black** - Python code formatting
- ✅ **yamllint** - YAML file linting
- ✅ **prettier** - YAML file formatting
- ✅ **Smart directory skipping** - Automatically skips `.git`, `__pycache__`, `node_modules`, etc.
- ✅ **Error handling** - Graceful handling of missing tools
- ✅ **Detailed reporting** - Summary of all linting results
- ✅ **Configurable** - Custom line lengths and skip patterns

## 🚀 Quick Start

### Command Line Usage

```bash
# Lint current directory with default settings (88 char line length)
python lint_runner.py .

# Lint with custom line length
python lint_runner.py . 100

# Lint a specific repository
python lint_runner.py /path/to/your/repo 88
```

### Programmatic Usage

```python
from lint_runner import lint_and_fix_repo

# Basic usage
results = lint_and_fix_repo(".", max_line_length=88)

# With custom skip patterns
results = lint_and_fix_repo(
    ".", 
    max_line_length=88,
    skip_patterns=["test_", "temp_", "draft_"]
)

print(f"Processed {results['python_files']} Python files")
print(f"Processed {results['yaml_files']} YAML files")
```

## 📋 Prerequisites

Install the required tools:

```bash
# Python tools
pip install flake8 black yamllint

# Node.js tools (for prettier)
npm install -g prettier
```

## ⚙️ Configuration

### Line Length
The default line length is **88 characters** (matching black's default). You can customize this:

```python
# In code
results = lint_and_fix_repo(".", max_line_length=100)

# Command line
python lint_runner.py . 100
```

### Skip Patterns
Skip specific files or directories:

```python
results = lint_and_fix_repo(
    ".",
    skip_patterns=[
        "test_",      # Skip files starting with "test_"
        "temp_",      # Skip files starting with "temp_"
        "draft_",     # Skip files starting with "draft_"
        "/vendor/",   # Skip vendor directory
    ]
)
```

### Auto-Skipped Directories
The following directories are automatically skipped:
- `.git`
- `__pycache__`
- `node_modules`
- `.venv`, `venv`
- `build`, `dist`
- `.pytest_cache`
- `.mypy_cache`

## 📊 Output Example

```
🚨 Starting full lint/fix pass on: /path/to/repo
📏 Max line length: 88
⏭️ Skip patterns: []

📄 Processing Python file: /path/to/repo/main.py
🔎 Running flake8 on /path/to/repo/main.py...
✅ flake8 passed
🧼 Auto-formatting with black on /path/to/repo/main.py...
✅ black formatting complete

📄 Processing YAML file: /path/to/repo/config.yaml
🔎 Running yamllint on /path/to/repo/config.yaml...
✅ yamllint passed
🧼 Auto-formatting YAML using Prettier on /path/to/repo/config.yaml...
✅ prettier formatting complete

📊 Linting Summary:
   Python files: 15 processed, 15 successful
   YAML files: 3 processed, 3 successful

✅ All files processed successfully!
```

## 🔧 Integration

### CI/CD Pipeline
Add to your CI/CD pipeline:

```yaml
# .github/workflows/lint.yml
name: Lint and Format
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install flake8 black yamllint
          npm install -g prettier
      - name: Run linting
        run: python shadows/audit_logic/lint_fixer/lint_runner.py .
```

### Pre-commit Hook
Add to your pre-commit configuration:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: lint-runner
        name: Lint Runner
        entry: python shadows/audit_logic/lint_fixer/lint_runner.py
        language: system
        types: [python, yaml]
        pass_filenames: false
```

## 🐛 Troubleshooting

### Missing Tools
If you see "❌ tool not found" messages:

```bash
# Install Python tools
pip install flake8 black yamllint

# Install Node.js tools
npm install -g prettier
```

### Permission Issues
If you get permission errors:

```bash
# Make script executable
chmod +x lint_runner.py

# Or run with python explicitly
python lint_runner.py .
```

### Large Repositories
For large repositories, consider using skip patterns:

```python
results = lint_and_fix_repo(
    ".",
    skip_patterns=[
        "/node_modules/",
        "/.git/",
        "/build/",
        "/dist/",
        "*.min.js",
        "*.min.css"
    ]
)
```

## 📝 Example Files

- `example_usage.py` - Demonstrates programmatic usage
- `lint_runner.py` - Main linting script
- `README.md` - This documentation

## 🤝 Contributing

When adding new linting tools:

1. Add the tool to the appropriate function (`run_python_lint` or `run_yaml_lint`)
2. Update the results dictionary
3. Add error handling for missing tools
4. Update this README with usage instructions
5. Test with various file types and configurations

## 📄 License

This tool is part of the LinkOps-MLOps project and follows the same licensing terms. 