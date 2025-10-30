from datetime import datetime, timedelta
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def access_matrix_helper(variable1: str, variable2: str):
    """Helper function for Access Matrix module."""
    return variable1 + variable2

