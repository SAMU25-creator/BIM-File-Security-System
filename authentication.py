"""
authentication.py

Authentication component of the BIM File Security System.

Responsible for verifying that a set of supplied credentials (username,
password) belongs to a registered user before any access-control,
logging, or session logic is allowed to run.

Covers:
    AUTH-001 - Valid credentials are accepted.
    AUTH-002 - Unregistered usernames are rejected.
    AUTH-003 - Registered usernames with the wrong password are rejected.
    AUTH-004 - Empty / missing (None) credentials are rejected without
               crashing the system.
    AUTH-005 - Basic injection-style input is safely rejected and never
               triggers an internal error or leaks implementation details.
"""

USERS = {
    "valid_user": "correct_password"
}


def login(username, password):
    if username in USERS and USERS[username] == password:
        return True

    return False