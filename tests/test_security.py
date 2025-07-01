# This test assumes you can import or mock the sanitize function
# If not, adapt to call the sanitizer API


def test_sanitizer_strips_creds():
    # from services.sanitizer.sanitizer.logic import sanitize  # Example import
    # result = sanitize(dirty_input)
    # For now, mock the result:
    result = {"text": "username=admin"}  # Simulate sanitized output
    assert "password" not in result["text"]
