from fastapi import APIRouter, HTTPException
from core.db import SessionLocal
from utils.safe_import import safe_import

AccessMatrix = safe_import("access_matrix", "models", "AccessMatrix")
router = APIRouter(prefix="/api/access_matrix", tags=["Access Matrix"])

@router.get("/")
def list_access():
    db = SessionLocal()
    rows = db.query(AccessMatrix).all()
    data = [dict(
        id=r.id,
        role_id=r.role_id,
        user_id=r.user_id,
        module=r.module,
        permission=r.permission
    ) for r in rows]
    db.close()
    return data

@router.post("/add")
def add_access(payload: dict):
    db = SessionLocal()
    record = AccessMatrix(**payload)
    db.add(record)
    db.commit()
    db.close()
    return {"message": "✅ Access rule added."}

@router.delete("/{access_id}")
def remove_access(access_id: int):
    db = SessionLocal()
    row = db.query(AccessMatrix).get(access_id)
    if not row:
        db.close()
        raise HTTPException(status_code=404, detail="Access not found")
    db.delete(row)
    db.commit()
    db.close()
    return {"message": "🗑️ Access rule removed."}
