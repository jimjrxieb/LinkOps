from fastapi import APIRouter
from utils.io import get_pending_approvals

router = APIRouter(prefix="/api/whis", tags=["Approvals"])


@router.get("/approvals")
def get_approvals():
    return get_pending_approvals()


@router.post("/approve/{approval_id}")
def approve_item(approval_id: str):
    # TODO: Implement approval logic
    return {"status": "approved", "id": approval_id}
