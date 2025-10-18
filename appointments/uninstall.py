from core.db import SessionLocal
from core.models.module import Module

def uninstall():
    """
    Marks the Appointments module as disabled in the database
    without deleting its data or tables.
    Ensures it no longer appears in the sidebar.
    """
    db = SessionLocal()
    try:
        module = db.query(Module).filter_by(name="appointments").first()
        if module:
            module.enabled = False
            db.commit()
            print("🟡 Appointments module disabled (data preserved).")
        else:
            print("⚠️ Appointments module not found in DB — skipping disable step.")
    except Exception as e:
        print(f"❌ Error disabling Appointments module: {e}")
    finally:
        db.close()

    print("✅ Appointments module uninstalled safely (data preserved).")
