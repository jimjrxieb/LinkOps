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

    # Apply replacement to all string fields
    return {k: replace_all(str(v)) if isinstance(v, str) else v for k, v in data.items()} 