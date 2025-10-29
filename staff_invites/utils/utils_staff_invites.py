"""
core/utils/utils_staff_invites.py
--------------------------
Utilities for invite-only registration tokens.
"""

from datetime import datetime, timedelta
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
INVITE_TOKEN_EXPIRE_HOURS = 24


def create_invite_token(email: str, role: str):
    """Create a short-lived invite token."""
    expire = datetime.utcnow() + timedelta(hours=INVITE_TOKEN_EXPIRE_HOURS)
    payload = {"email": email, "role": role, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_invite_token(token: str):
    """Decode and verify an invite token."""
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return data
    except JWTError:
        return None
