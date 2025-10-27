import os, sys
from core.db import Base

def uninstall():
    """Unregister the Invites model cleanly (data retained)."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, "models")
    sys.path.insert(0, models_dir)

    try:
        from model_invites import Invites

        if Invites.__table__.fullname in Base.metadata.tables:
            Base.metadata.remove(Invites.__table__)
            print("🧹 Unregistered Invites model from SQLAlchemy metadata.")

        print("🗑️ Invites module uninstalled successfully (data retained).")

    except Exception as e:
        print(f"⚠️ Error during uninstall: {e}")

    finally:
        if models_dir in sys.path:
            sys.path.remove(models_dir)
