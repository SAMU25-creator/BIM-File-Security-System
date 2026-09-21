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
