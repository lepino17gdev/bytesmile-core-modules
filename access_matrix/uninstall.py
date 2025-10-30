import os, sys
from core.db import Base

def uninstall():
    """Unregister the AccessMatrix model cleanly (data retained)."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, "models")
    sys.path.insert(0, models_dir)

    try:
        from model_access_matrix import AccessMatrix

        table_name = AccessMatrix.__table__.fullname
        if table_name in Base.metadata.tables:
            Base.metadata.remove(Base.metadata.tables[table_name])
            print(f"🧹 Unregistered {table_name} model from SQLAlchemy metadata.")
        else:
            print(f"ℹ️ Table {table_name} not found in metadata (already unregistered).")

        print("🗑️ AccessMatrix module uninstalled successfully (data retained).")

    except Exception as e:
        print(f"⚠️ Error during uninstall: {e}")

    finally:
        if models_dir in sys.path:
            sys.path.remove(models_dir)