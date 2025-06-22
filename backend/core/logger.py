from models.log import LogEntry
from config.database import get_db
from sqlalchemy.orm import Session

def log_to_whis(entry: dict, db: Session):
    log = LogEntry(
        input_type=entry["input_type"],
        source=entry["source"],
        sanitized=entry["sanitized"],
    )
    db.add(log)
    db.commit()
    db.refresh(log)
