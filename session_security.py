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

