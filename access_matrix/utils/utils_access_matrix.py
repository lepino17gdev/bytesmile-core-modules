from core.db import SessionLocal
from core.utils.safe_import import safe_import

def user_has_access(user, module_name: str, permission: str = "view"):
    """
    Returns True if user has access to given module/permission.
    Wildcards in AccessMatrix are respected (*).
    Falls back to True if AccessMatrix not found.
    """
    AccessMatrix = safe_import("model_access_matrix", "models", "AccessMatrix")
    if not AccessMatrix:
        return True

    db = SessionLocal()
    role_id = getattr(user, "role_id", None)
    user_id = getattr(user, "id", None)

    try:
        rows = db.query(AccessMatrix).filter(
            (AccessMatrix.role_id == role_id) | (AccessMatrix.user_id == user_id)
        ).all()
        for r in rows:
            if (
                r.module in ("*", module_name)
                and (r.permission in ("*", permission))
            ):
                db.close()
                return True
        db.close()
        return False
    except Exception as e:
        print(f"⚠️ Access check failed: {e}")
        db.close()
        return True
