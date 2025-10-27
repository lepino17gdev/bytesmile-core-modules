import os, sys
from core.db import Base, engine
from sqlalchemy.exc import InvalidRequestError

def install(app=None):
    """Minimal install: register model, create table once, then unregister."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, "models")
    sys.path.insert(0, models_dir)

    try:
        from model_invites import Invites
        # ✅ Create table if it doesn’t exist yet
        try:
            Base.metadata.create_all(bind=engine, tables=[Invites.__table__])
            print("✅ Invites table created (if not existing).")
        except InvalidRequestError:
            print("ℹ️ Table already exists; skipping create_all().")

        # ✅ Unregister after installation to avoid re-import metadata issues
        if Invites.__name__ in Base.metadata.tables:
            Base.metadata.remove(Invites.__table__)
            print("🧹 Model unregistered from metadata after install.")

    except Exception as e:
        print(f"⚠️ Failed during install: {e}")

    finally:
        if models_dir in sys.path:
            sys.path.remove(models_dir)
