from fastapi import APIRouter

router = APIRouter(prefix="/api/ficknury", tags=["Credentials"])


@router.post("/credentials")
def save_creds(payload: dict):
    # Save securely (stub)
    return {"status": "saved"}


@router.get("/credentials")
def get_creds():
    return {"status": "not_implemented"}
