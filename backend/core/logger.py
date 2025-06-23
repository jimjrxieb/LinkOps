from backend.models.log import LogEntry
from backend.config.database import get_db
from sqlalchemy.orm import Session

def log_to_whis(entry: dict, db: Session = None):
    """Log to Whis with optional database connection"""
    if db is None:
        # Fallback for development when database is not available
        print(f"[LOG:WHIS] {entry}")
        return
    
    try:
        log = LogEntry(
            input_type=entry.get("input_type", "unknown"),
            source=entry.get("source", "unknown"),
            sanitized=entry.get("sanitized", ""),
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        print(f"[LOG:WHIS] Saved to database: {entry}")
    except Exception as e:
        print(f"[LOG:WHIS] Database error, falling back to console: {e}")
        print(f"[LOG:WHIS] {entry}")
