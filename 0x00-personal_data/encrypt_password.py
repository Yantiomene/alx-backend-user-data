#!/usr/bin/env python3
""" Encrypting passwords """

import bcrypt


def hash_password(password: str) -> bytes:
    """Return a saled, hashed password"""

    pwd_encoded = password.encode()
    hashed = bcrypt.hashpw(pwd_encoded, bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate that the provided password matches the hashed password"""

    return bcrypt.checkpw(password.encode(), hashed_password)
