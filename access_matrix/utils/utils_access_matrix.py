import importlib
import os

def safe_import_access_matrix():
    """
    Safely import AccessMatrix model.
    Priority 1: core/models/model_access_matrix.py
    Priority 2: modules/access_matrix/models/model_access_matrix.py
    Returns the AccessMatrix class or None if not found.
    """
    possible_paths = [
        ("core.models.model_access_matrix", "core/models/model_access_matrix.py"),
        ("modules.access_matrix.models.model_access_matrix", "modules/access_matrix/models/model_access_matrix.py"),
    ]

    for module_name, file_path in possible_paths:
        if os.path.exists(file_path):
            try:
                mod = importlib.import_module(module_name)
                return getattr(mod, "AccessMatrix", None)
            except Exception as e:
                print(f"⚠️ Failed to import AccessMatrix from {module_name}: {e}")
                return None
    print("⚠️ AccessMatrix model not found in core or modules.")
    return None
