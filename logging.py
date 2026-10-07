"""
audit_log.py

Reference implementation of the logging module the logging tests assume.
(Named audit_log.py, not logging.py, because a file called logging.py would
shadow Python's built-in logging module and break pytest.)

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
