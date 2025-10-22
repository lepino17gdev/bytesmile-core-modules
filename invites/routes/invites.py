from fastapi import APIRouter

router = APIRouter(prefix="/api/invites", tags=["Invites"])

@router.get("/")
def list_invites():
    return {"message": "This is the Invites API endpoint."}
