# modules/appointments/install.py
import importlib.util
import os

def install(app):
    """
    Module-specific installation logic.
    Registers models dynamically to avoid ImportError during install.
    """
    module_dir = os.path.dirname(__file__)
    model_path = os.path.join(module_dir, "models", "appointment_model.py")

    if os.path.exists(model_path):
        spec = importlib.util.spec_from_file_location("appointments_model", model_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("✅ Appointments model loaded successfully.")
    else:
        print("⚠️ appointments_model.py not found; skipping model load.")

    print("🎯 Appointments module installation complete.")
