import os, sys, importlib.util
from core.db import Base, engine
from sqlalchemy.exc import InvalidRequestError

def install(app=None):
    """Register the Invites model and safely create its table once."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, "models")
    model_file = os.path.join(models_dir, "model_invites.py")

    if not os.path.exists(model_file):
        print("⚠️ Model file not found:", model_file)
        return

    # --- Load the model dynamically ---
    spec = importlib.util.spec_from_file_location("modules.invites.models.model_invites", model_file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["modules.invites.models.model_invites"] = mod
    sys.modules["core.models.model_invites"] = mod  # ✅ fallback for backward compatibility
    spec.loader.exec_module(mod)

    # --- Register model with SQLAlchemy ---
    if hasattr(mod, "Invites"):
        Invites = mod.Invites

        # Prevent duplicate table registration
        if Invites.__table__.fullname not in Base.metadata.tables:
            try:
                Base.metadata.create_all(bind=engine, tables=[Invites.__table__])
                print("✅ Invites module installed successfully (table created).")
            except InvalidRequestError as e:
                print(f"⚠️ Table already exists, skipping create_all(): {e}")
        else:
            print("ℹ️ Invites table already registered, skipping create_all().")

    else:
        print("⚠️ No Invites model found in model_invites.py.")
