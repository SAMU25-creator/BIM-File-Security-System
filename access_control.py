"""
access_control.py

Role-based access control (RBAC) for the BIM File Security System.

Access matrix (from the README):
    Architect          -> view, edit
    Engineer           -> view, edit
    Contractor         -> view
    Client             -> view
    Unauthorised user  -> denied (no view, no edit)

Covers:
    AC-001 - Architect can view and edit.
    AC-002 - Engineer can view and edit.
    AC-003 - Contractor can view, but is denied edit.
    AC-004 - Client can view, but is denied edit.
    AC-005 - An unregistered/unknown user is denied both view and edit.
"""

from audit_log import log_access

# Which actions each role is permitted to perform.
ROLE_PERMISSIONS = {
    "Architect": {"view", "edit"},
    "Engineer": {"view", "edit"},
    "Contractor": {"view"},
    "Client": {"view"},
}

USER_ROLES = {
    "architect": "Architect",
    "engineer": "Engineer",
    "contractor": "Contractor",
    "client": "Client",
}

def check_access(username, action):
    """
    Check whether a user is permitted to perform an action.
 
    Returns True only when the user is registered with a role, and that
    role is permitted to perform the given action. Returns False for
    every other case - unknown user, unknown/invalid action, or bad
    input (None, wrong type, etc.) - it never raises.
 
    This is the single gate every file operation must go through: a
    denied result here means the action must not happen, not just be
    hidden from a UI.
    """
    
    if not isinstance(username, str) or not isinstance(action, str):
        return False
 
    role = USER_ROLES.get(username)
    if role is None:
        # Unregistered/unauthorised user - always denied.
        return False
 
    return action in ROLE_PERMISSIONS.get(role, set())

def access_file(username, action, filename):
    """
    Check file access and record the result in the audit log.
    Return True if access is allowed, otherwise False.
    """
    allowed = check_access(username, action)
    log_access(username, action, filename, allowed)
    return allowed
