from sanitizer.logic import scrub_values

PROFANITY_LIST = ["badword1", "badword2"]  # Extend as needed
GARBAGE_SYMBOLS = ["#$%&*~"]


def remove_profanity(text):
    for word in PROFANITY_LIST:
        text = text.replace(word, "[censored]")
    return text


def remove_garbage(text):
    for symbol in GARBAGE_SYMBOLS:
        text = text.replace(symbol, "")
    return text


def remove_duplicates(lines):
    seen = set()
    result = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            result.append(line)
    return result


def sanitize_input(input_type: str, payload: dict):
    if input_type == "youtube":
        raw_text = payload.get("raw_text", "")
        topic = payload.get("topic")
        source = payload.get("source", "youtube")
        metadata = payload.get("metadata", {})

        # Remove garbage symbols and profanity
        cleaned = remove_garbage(remove_profanity(raw_text))
        # Split into lines, remove duplicates, join back
        lines = cleaned.splitlines()
        lines = [line.strip() for line in lines if line.strip()]
        lines = remove_duplicates(lines)
        cleaned_text = "\n".join(lines)
        # Scrub PII and normalize
        cleaned_text = scrub_values({"text": cleaned_text})["text"]

        # Save to data lake or queue
        from utils.file_writer import write_clean_log

        write_clean_log(
            input_type,
            {
                "cleaned_text": cleaned_text,
                "topic": topic,
                "source": source,
                "metadata": metadata,
            },
        )
        return {
            "cleaned_text": cleaned_text,
            "topic": topic,
            "source": source,
            "metadata": metadata,
            "sanitization_stats": {
                "lines": len(lines),
                "original_length": len(raw_text),
                "cleaned_length": len(cleaned_text),
            },
        }
    else:
        cleaned = scrub_values(payload)
        # Save or emit for Whis
        from utils.file_writer import write_clean_log

        write_clean_log(input_type, cleaned)
        return cleaned
