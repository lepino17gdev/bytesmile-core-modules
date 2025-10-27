import os, importlib.util
from core.db import Base, engine

def install(app=None):
    """Dynamically register models and create tables without duplication."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, "models")

    created_tables = []

    for filename in os.listdir(models_dir):
        if not filename.endswith(".py"):
            continue
        model_path = os.path.join(models_dir, filename)

        spec = importlib.util.spec_from_file_location(f"modules.invites.models.{filename[:-3]}", model_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        for obj in mod.__dict__.values():
            if hasattr(obj, "__table__"):
                # Avoid duplicate metadata registration
                if obj.__table__.fullname not in Base.metadata.tables:
                    Base.metadata.create_all(bind=engine, tables=[obj.__table__])
                    created_tables.append(obj.__tablename__)

    print(f"✅ Invites module installed successfully (tables: {', '.join(created_tables) or 'none'})")
