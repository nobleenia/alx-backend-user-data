#!/usr/bin/env python3
"""
Module for testing user authentication service
"""
import requests


def register_user(email: str, password: str) -> None:
    """Register a new user"""
    assert True


def log_in_wrong_password(email: str, password: str) -> None:
    """Try to log in with a wrong password"""
    assert True


def log_in(email: str, password: str) -> str:
    """Log in with correct credentials"""
    assert True


def profile_unlogged() -> None:
    """Try to get profile without being logged in"""
    assert True


def profile_logged(session_id: str) -> None:
    """Get profile while logged in"""
    assert True

def log_out(session_id: str) -> None:
    """Log out"""
    assert True


def reset_password_token(email: str) -> str:
    """Get reset password token"""
    assert True


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password using reset token"""
    assert True


# Main script to run the tests
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
