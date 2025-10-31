from fastapi import APIRouter, HTTPException
from core.db import SessionLocal
from core.utils.safe_import import safe_import
from core.models.role import Role
from core.models.user import User 

AccessMatrix = safe_import("model_access_matrix", "models", "AccessMatrix")
router = APIRouter(prefix="/api/access_matrix", tags=["Access Matrix"])

@router.get("/")
def list_access():
    db = SessionLocal()

    # 🧠 Join with roles and users if they exist
    query = (
        db.query(
            AccessMatrix.id,
            AccessMatrix.role_id,
            Role.name.label("role_name"),
            AccessMatrix.user_id,
            User.username.label("user_name"),
            User.email.label("user_email"),
            AccessMatrix.module,
            AccessMatrix.permission,
        )
        .outerjoin(Role, Role.id == AccessMatrix.role_id)
        .outerjoin(User, User.id == AccessMatrix.user_id)
    )

    rows = query.all()

    data = []
    for r in rows:
        data.append(
            dict(
                id=r.id,
                role_id=r.role_id,
                role_name=r.role_name,
                user_id=r.user_id,
                user_name=r.user_name,
                user_email=r.user_email,
                module=r.module,
                permission=r.permission,
                subject=(
                    r.role_name
                    or r.user_name
                    or r.user_email
                    or f"Role #{r.role_id}" if r.role_id else f"User #{r.user_id}"
                ),
                subject_type="role" if r.role_id else "user",
            )
        )

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
