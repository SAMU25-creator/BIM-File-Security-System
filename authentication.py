"""
authentication.py

Simple authentication check for the BIM File Security System.

Covers:
    AUTH-001 - Valid credentials are accepted.
    AUTH-002 - Unregistered usernames are rejected.
    AUTH-003 - Registered usernames with the wrong password are rejected.
    AUTH-004 - Empty / missing (None) credentials are rejected, no crash.
    AUTH-005 - Injection-style input is safely rejected (it's just a
               dictionary lookup, so it can't be interpreted as code).
"""


"""
authentication.py

Simple authentication check for the BIM File Security System.
"""

from audit_log import log_login

USERS = {
    "valid_user": "correct_password"
}


def login(username, password):
    """Validate credentials and log every login attempt."""

    # Reject invalid input safely.
    if not isinstance(username, str) or not isinstance(password, str):
        log_login(username, False)
        return False

    if not username or not password:
        log_login(username, False)
        return False

    # Check the credentials.
    succeeded = USERS.get(username) == password

    # Record the outcome without ever logging the password.
    log_login(username, succeeded)

    return succeeded
