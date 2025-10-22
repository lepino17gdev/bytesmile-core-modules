
import os, sys
from core.db import Base, engine

# Ensure local 'models' directory is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
models_path = os.path.join(current_dir, "models")
if models_path not in sys.path:
    sys.path.insert(0, models_path)

from model_sample import Sample

def install(app=None):
    """Register Sample model and create its table."""
    Base.metadata.create_all(bind=engine, tables=[Sample.__table__])
    print("✅ Sample module installed successfully.")

