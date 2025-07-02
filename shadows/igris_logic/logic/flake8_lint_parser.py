import subprocess
import re
import logging
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class Flake8LintParser:
    def __init__(self):
        self.error_patterns = {
            "F841": "unused variable",
            "E401": "multiple imports on one line",
            "E501": "line too long",
            "E302": "expected 2 blank lines",
            "E303": "too many blank lines",
            "E225": "missing whitespace around operator",
            "E226": "missing whitespace around arithmetic operator",
            "E227": "missing whitespace around bitwise or shift operator",
            "E228": "missing whitespace around modulo operator",
            "E231": "missing whitespace after ','",
            "E241": "multiple spaces after ','",
            "E242": "tab after ','",
            "E251": "unexpected spaces around keyword / parameter equals",
            "E261": "at least two spaces before inline comment",
            "E262": "inline comment should start with '# '",
            "E265": "block comment should start with '# '",
            "E266": "too many leading '#' for block comment",
            "E271": "multiple spaces after keyword",
            "E272": "multiple spaces before keyword",
            "E273": "tab after keyword",
            "E274": "tab before keyword",
            "E275": "missing whitespace after keyword",
            "E301": "expected 1 blank line",
            "E304": "blank lines found after function decorator",
            "E305": "expected 2 blank lines after class or function definition",
            "E306": "expected 1 blank line before a nested definition",
            "E401": "multiple imports on one line",
            "E402": "module level import not at top of file",
            "E501": "line too long",
            "E502": "the backslash is redundant between brackets",
            "E701": "multiple statements on one line (colon)",
            "E702": "multiple statements on one line (semicolon)",
            "E703": "statement ends with a semicolon",
            "E711": "comparison to None should be 'if cond is None:'",
            "E712": "comparison to True should be 'if cond is True:' or 'if cond:'",
            "E713": "test for membership should be 'not in'",
            "E714": "test for object identity should be 'is not'",
            "E721": "do not compare types, use 'isinstance()'",
            "E722": "do not use bare except, specify exception instead",
            "E731": "do not assign a lambda expression, use a def",
            "E741": "ambiguous variable name",
            "E742": "ambiguous class definition",
            "E743": "ambiguous function definition",
            "E901": "SyntaxError or IndentationError",
            "E902": "IOError (file not found, permission denied, etc.)",
            "W191": "indentation contains tabs",
            "W291": "trailing whitespace",
            "W292": "no newline at end of file",
            "W293": "blank line contains whitespace",
            "W391": "Remove blank line at end of file",
            "W503": "line break before binary operator",
            "W504": "line break after binary operator",
            "W505": "doc line too long",
            "W601": ".has_key() is deprecated, use 'in'",
            "W602": "deprecated form of raising exception",
            "W603": "'<>' is deprecated, use '!='",
            "W604": "backticks are deprecated, use 'repr()'",
            "W605": "invalid escape sequence",
            "W606": "'async' and 'await' are reserved keywords starting with Python 3.7",
        }

    def run_flake8(self, path: str, max_line_length: int = 88) -> List[Dict[str, Any]]:
        """Run flake8 on the specified path and return parsed results"""
        try:
            # Run flake8 command
            result = subprocess.run(
                [
                    "flake8",
                    "--max-line-length",
                    str(max_line_length),
                    "--format",
                    "default",
                    path,
                ],
                capture_output=True,
                text=True,
                cwd=Path(path).parent,
            )

            # Parse the output
            return self.parse_flake8_output(result.stdout, result.stderr)

        except Exception as e:
            logger.error(f"Failed to run flake8: {str(e)}")
            return []

    def parse_flake8_output(self, stdout: str, stderr: str) -> List[Dict[str, Any]]:
        """Parse flake8 output into structured error data"""
        errors = []

        # Parse each line of output
        for line in stdout.strip().split("\n"):
            if not line.strip():
                continue

            # Parse flake8 output format: file:line:col: code message
            match = re.match(r"^(.+):(\d+):(\d+):\s*([A-Z]\d+)\s+(.+)$", line)
            if match:
                file_path, line_num, col_num, error_code, message = match.groups()

                error_info = {
                    "file": file_path,
                    "line": int(line_num),
                    "column": int(col_num),
                    "error_code": error_code,
                    "message": message,
                    "description": self.error_patterns.get(error_code, "Unknown error"),
                    "fix_suggestion": self.generate_fix_suggestion(
                        error_code, message, line_num
                    ),
                }

                errors.append(error_info)

        return errors

    def generate_fix_suggestion(
        self, error_code: str, message: str, line_num: str
    ) -> str:
        """Generate fix suggestions based on error code"""
        suggestions = {
            "F841": f"Remove unused variable on line {line_num}",
            "E401": f"Separate imports on line {line_num}",
            "E501": f"Break long line {line_num} into multiple lines",
            "E302": f"Add 2 blank lines before function/class on line {line_num}",
            "E303": f"Remove extra blank lines around line {line_num}",
            "E225": f"Add spaces around operator on line {line_num}",
            "E226": f"Add spaces around arithmetic operator on line {line_num}",
            "E227": f"Add spaces around bitwise/shift operator on line {line_num}",
            "E228": f"Add spaces around modulo operator on line {line_num}",
            "E231": f"Add space after comma on line {line_num}",
            "E241": f"Remove extra spaces after comma on line {line_num}",
            "E251": f"Remove spaces around '=' on line {line_num}",
            "E261": f"Add 2 spaces before inline comment on line {line_num}",
            "E262": f"Add space after '#' in comment on line {line_num}",
            "E265": f"Add space after '#' in block comment on line {line_num}",
            "E271": f"Remove extra spaces after keyword on line {line_num}",
            "E272": f"Remove extra spaces before keyword on line {line_num}",
            "E275": f"Add space after keyword on line {line_num}",
            "E301": f"Add blank line before function/class on line {line_num}",
            "E304": f"Remove blank lines after decorator on line {line_num}",
            "E305": f"Add 2 blank lines after class/function definition on line {line_num}",
            "E306": f"Add blank line before nested definition on line {line_num}",
            "E402": f"Move import to top of file (line {line_num})",
            "E502": f"Remove redundant backslash on line {line_num}",
            "E701": f"Split multiple statements on line {line_num}",
            "E702": f"Remove semicolon on line {line_num}",
            "E703": f"Remove semicolon on line {line_num}",
            "E711": f"Use 'is None' instead of '== None' on line {line_num}",
            "E712": f"Use 'is True' or simplify comparison on line {line_num}",
            "E713": f"Use 'not in' instead of 'not ... in' on line {line_num}",
            "E714": f"Use 'is not' instead of '!= ...' on line {line_num}",
            "E721": f"Use 'isinstance()' instead of 'type()' on line {line_num}",
            "E722": f"Specify exception type instead of bare except on line {line_num}",
            "E731": f"Use 'def' instead of lambda assignment on line {line_num}",
            "E741": f"Rename ambiguous variable on line {line_num}",
            "E742": f"Rename ambiguous class on line {line_num}",
            "E743": f"Rename ambiguous function on line {line_num}",
            "E901": f"Fix syntax error on line {line_num}",
            "E902": f"Fix file I/O error on line {line_num}",
            "W191": f"Replace tabs with spaces on line {line_num}",
            "W291": f"Remove trailing whitespace on line {line_num}",
            "W292": "Add newline at end of file",
            "W293": f"Remove whitespace from blank line {line_num}",
            "W391": "Remove blank line at end of file",
            "W503": f"Move line break after binary operator on line {line_num}",
            "W504": f"Move line break before binary operator on line {line_num}",
            "W505": f"Break long docstring on line {line_num}",
            "W601": f"Use 'in' instead of '.has_key()' on line {line_num}",
            "W602": "Use 'raise Exception()' instead of 'raise Exception, value' on line {line_num}",
            "W603": f"Use '!=' instead of '<>' on line {line_num}",
            "W604": f"Use 'repr()' instead of backticks on line {line_num}",
            "W605": f"Fix invalid escape sequence on line {line_num}",
            "W606": f"Use 'async'/'await' keywords properly on line {line_num}",
        }

        return (
            suggestions.get(error_code, f"Fix {error_code} error on line {line_num}")
            if error_code != "W602"
            else suggestions["W602"].format(line_num=line_num)
        )

    def create_cursor_prompt(self, errors: List[Dict[str, Any]]) -> str:
        """Create a Cursor prompt for fixing lint errors"""
        if not errors:
            return "No lint errors found."

        prompt = "Fix the following flake8 lint errors:\n\n"

        for error in errors:
            prompt += f"File: {error['file']}\n"
            prompt += f"Line: {error['line']}\n"
            prompt += f"Error: {error['error_code']} - {error['message']}\n"
            prompt += f"Fix: {error['fix_suggestion']}\n\n"

        prompt += (
            "Please provide the corrected code for each file that needs to be updated."
        )

        return prompt

    def get_error_summary(self, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get a summary of lint errors"""
        if not errors:
            return {
                "total_errors": 0,
                "files_affected": 0,
                "error_types": {},
                "status": "clean",
            }

        files_affected = len(set(error["file"] for error in errors))
        error_types = {}

        for error in errors:
            error_code = error["error_code"]
            error_types[error_code] = error_types.get(error_code, 0) + 1

        return {
            "total_errors": len(errors),
            "files_affected": files_affected,
            "error_types": error_types,
            "status": "has_errors",
            "most_common_errors": sorted(
                error_types.items(), key=lambda x: x[1], reverse=True
            )[:5],
        }
