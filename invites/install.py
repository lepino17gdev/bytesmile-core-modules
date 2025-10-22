import os, sys, importlib.util
from core.db import Base, engine

def install(app=None):
    """Safely register module models without duplicate metadata."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_path = os.path.join(current_dir, "models", "model_invites.py")

    # Dynamically import model file
    spec = importlib.util.spec_from_file_location("modules.invites.models.model_invites", models_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Find model classes that have __table__ defined
    created_tables = []
    for obj in mod.__dict__.values():
        if hasattr(obj, "__table__"):
            Base.metadata.create_all(bind=engine, tables=[obj.__table__])
            created_tables.append(obj.__tablename__)

    print(f"✅ Invites module installed successfully (tables: {', '.join(created_tables)})")
