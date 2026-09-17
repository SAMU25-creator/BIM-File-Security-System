"""
session.py

Session management for the BIM File Security System.

Covers:
    SESS-001 - A created session is valid and has a unique token.
    SESS-002 - Logging out ends the session; the old token stops working.
    SESS-003 - Sessions expire after a period of inactivity.
    SESS-004 - Expired or logged-out tokens are always rejected on reuse.
    SESS-005 - Missing/unknown/malformed tokens are rejected, never a crash.
"""

import secrets
import time

# Seconds of inactivity before a session expires.
SESSION_TIMEOUT = 30 * 60

# token -> {"username": str, "last_active": float}
_SESSIONS = {}


def create_session(username):
    """Create a session for a user and return its token."""
    token = secrets.token_urlsafe(32)
    _SESSIONS[token] = {"username": username, "last_active": time.time()}
    return token


def validate_session(token):
    """
    Return True only if the token belongs to an active session.

    A valid check counts as activity and resets the inactivity timer.
    Expired sessions are removed, so an expired token can never work again.
    Never raises.
    """
    if not isinstance(token, str) or not token:
        return False

    session = _SESSIONS.get(token)
    if session is None:
        return False

    now = time.time()
    if now - session["last_active"] > SESSION_TIMEOUT:
        del _SESSIONS[token]
        return False

    session["last_active"] = now
    return True


def logout(token):
    """End a session. Unknown or invalid tokens are ignored safely."""
    if isinstance(token, str):
        _SESSIONS.pop(token, None)
