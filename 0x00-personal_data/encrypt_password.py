#!/usr/bin/env python3
"""
Module for password hashing
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password with a salt using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted, hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate a password against a hashed password using bcrypt.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The password to validate.

    Returns:
        bool: True if the password matches the hashed password,
        False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
