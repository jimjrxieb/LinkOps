from fastapi import APIRouter
from utils.io import get_training_digest

router = APIRouter(prefix="/api/whis", tags=["Digest"])

@router.get("/digest")
def get_digest():
    return get_training_digest() 