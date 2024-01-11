#!/usr/bin/env python3
""" Encrypting passwords """

import bcrypt


def hash_password(password: str) -> bytes:
    """Return a saled, hashed password"""

    pwd_encoded = password.encode()
    hashed = bcrypt.hashpw(pwd_encoded, bcrypt.gensalt())

    return hashed
