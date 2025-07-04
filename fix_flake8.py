import subprocess
import os

TARGET_DIR = "shadows"


def find_python_files(path):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)


def autoflake_cleanup(filepath):
    print(f"🧹 Running autoflake on: {filepath}")
    subprocess.run(
        [
            "autoflake",
            "--in-place",
            "--remove-unused-variables",
            "--remove-all-unused-imports",
            filepath,
        ]
    )


def auto_fix_file(filepath):
    print(f"🛠️  Running autopep8 on: {filepath}")
    subprocess.run(["autopep8", "--in-place", "--aggressive", "--aggressive", filepath])


def run_flake8(filepath):
    result = subprocess.run(["flake8", filepath], capture_output=True, text=True)
    if result.stdout:
        print(f"❌ Still issues in {filepath}:\n{result.stdout}")
    else:
        print(f"✅ Clean: {filepath}")


def main():
    print("🔍 Scanning for Python files to auto-fix Flake8 issues...\n")
    for py_file in find_python_files(TARGET_DIR):
        autoflake_cleanup(py_file)
        auto_fix_file(py_file)
        run_flake8(py_file)


if __name__ == "__main__":
    main()
