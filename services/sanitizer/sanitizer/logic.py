import re

def scrub_values(data: dict) -> dict:
    pattern_map = {
        r"\b\d{1,3}(?:\.\d{1,3}){3}\b": "<IP_ADDR>",
        r"\b(?:[a-zA-Z0-9_\-\.]+@\S+)\b": "<EMAIL>",
        r"/(?:[\w\-]+/)*[\w\-]+\.\w+": "<FILE_PATH>",
        r"\bns-\w+\b": "<NAMESPACE>",
        r"\berror-[a-f0-9]{6,}\b": "<ERROR_ID>",
        r"\b(?:[a-z]{2,10}\.[a-z]{2,6})\b": "<DOMAIN>"
    }

    def replace_all(text):
        for pat, repl in pattern_map.items():
            text = re.sub(pat, repl, text)
        return text

    def _clean_str(s):
        """Enhanced string cleaning for solution entries"""
        if not isinstance(s, str):
            return s
        
        # Basic redaction patterns
        s = s.replace("prod", "[redacted]")
        s = s.replace("password", "[redacted]")
        s = s.replace("secret", "[redacted]")
        s = s.replace("token", "[redacted]")
        s = s.replace("key", "[redacted]")
        
        # Apply regex patterns
        s = replace_all(s)
        
        return s

    def _sanitize_solution_entry(payload: dict) -> dict:
        """Special handling for solution_entry type"""
        if isinstance(payload, dict):
            # Clean all string values
            payload = {
                k: _clean_str(v) if isinstance(v, str) else v
                for k, v in payload.items()
            }

            # Handle solution path entries specifically
            if "solution_path" in payload and isinstance(payload["solution_path"], list):
                payload["solution_path"] = [_clean_str(step) for step in payload["solution_path"]]

        return payload

    # Check if this is a solution entry
    if isinstance(data, dict) and data.get("input_type") == "solution_entry":
        return _sanitize_solution_entry(data.get("payload", data))
    
    # Apply replacement to all string fields for other types
    return {k: replace_all(str(v)) if isinstance(v, str) else v for k, v in data.items()} 