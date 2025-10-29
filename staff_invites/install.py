import os, sys
from core.db import Base, engine
from sqlalchemy.exc import InvalidRequestError

def install(app=None):
    """Robust install: register model, create table once, unregister cleanly to avoid reimport issues."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, "models")
    sys.path.insert(0, models_dir)

    try:
        from model_staff_invites import Invites

        # 🧹 Remove stale class definitions in ORM registry (safe re-install)
        class_registry = getattr(Base.registry, "_class_registry", {})
        if "Invites" in class_registry:
            del class_registry["Invites"]
            print("🧹 Removed old Invites ORM class from registry.")

        # 🧹 Remove any existing table reference before re-creation
        table_name = Invites.__table__.fullname
        if table_name in Base.metadata.tables:
            Base.metadata.remove(Base.metadata.tables[table_name])
            print(f"🧹 Removed stale table reference: {table_name}")

        # ✅ Create table if it doesn’t exist yet
        try:
            Base.metadata.create_all(bind=engine, tables=[Invites.__table__])
            print("✅ Invites table created (if not existing).")
        except InvalidRequestError:
            print("ℹ️ Table already exists; skipping create_all().")

        # ✅ Immediately unregister to prevent “already defined” errors later
        if table_name in Base.metadata.tables:
            Base.metadata.remove(Base.metadata.tables[table_name])
            print("🧹 Model unregistered from metadata after install.")

        print("✅ Invites module installed successfully.")

    except Exception as e:
        print(f"⚠️ Failed during install: {e}")

    finally:
        if models_dir in sys.path:
            sys.path.remove(models_dir)
