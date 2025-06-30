from sanitizer.logic import scrub_values


def sanitize_input(input_type: str, payload: dict):
    cleaned = scrub_values(payload)
    # Save or emit for Whis
    from utils.file_writer import write_clean_log

    write_clean_log(input_type, cleaned)
    return cleaned
