"""
audit_log.py

Interface used by the tests:

    log_event(username, action, file, result)  -> writes one log entry
    get_log_entries()                          -> list of entries, oldest first
    clear_log()                                -> empties the log

Each entry is a dict with these fields:
    username   who made the attempt
    action     what they tried to do ("login", "view", "edit", ...)
    file       which file was involved (None for a login)
    timestamp  when it happened (seconds since the epoch)
    result     "success" / "failure" for logins,
               "allowed" / "denied" for file access

Passwords are never passed to or stored by this module.

How the other modules are expected to use it:

    authentication.login()     calls log_login(username, succeeded)
    access_control.access_file() calls log_access(username, action, filename, allowed)
"""
import time

RESULT_SUCCESS = "success"
RESULT_FAILURE = "failure"
RESULT_ALLOWED = "allowed"
RESULT_DENIED = "denied"

# In-memory log, oldest entry first.
_entries = []


def log_event(username, action, file, result):
    """Write one log entry. Missing (None) values are stored as given, never raise."""
    _entries.append(
        {
            "username": username,
            "action": action,
            "file": file,
            "timestamp": time.time(),
            "result": result,
        }
    )


def log_login(username, succeeded):
    """Log a login attempt as a success or a failure."""
    log_event(username, "login", None, RESULT_SUCCESS if succeeded else RESULT_FAILURE)


def log_access(username, action, filename, allowed):
    """Log a file access attempt as allowed or denied."""
    log_event(username, action, filename, RESULT_ALLOWED if allowed else RESULT_DENIED)


def get_log_entries():
    """Return a copy of the log, so callers cannot change it by accident."""
    return [dict(entry) for entry in _entries]


def clear_log():
    """Empty the log."""
    _entries.clear()