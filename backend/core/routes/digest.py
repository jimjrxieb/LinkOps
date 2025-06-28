from fastapi import APIRouter

router = APIRouter()

@router.get("/api/whis/digest")
async def get_digest():
    """Stub: Get Whis training digest (no DB)"""
    return {
        "date": "2024-01-01T00:00:00Z",
        "approved_today": 0,
        "pending_approvals": 0,
        "recent_approved": []
    } 