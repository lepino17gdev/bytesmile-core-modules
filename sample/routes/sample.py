from fastapi import APIRouter

router = APIRouter(prefix="/api/sample", tags=["Sample"])

@router.get("/")
def list_sample():
    return {"message": "This is the Sample API endpoint."}
