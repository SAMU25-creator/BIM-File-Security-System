# BIM File Security System

A role-based access control (RBAC) system for securing Building Information Modelling (BIM) files. Different user roles get different levels of access to construction project files — with authentication, access logging, and encryption protecting the data.

This project addresses a real construction-industry problem: BIM files (architectural drawings, engineering models, site plans) contain sensitive project information that must only be accessible to the right people, at the right permission level.

## Access model


| Role | Permission |
|---|---|
| Architect | View / Edit |
| Engineer | View / Edit |
| Contractor | View |
| Client | View |
| Unauthorised user | Denied |

Every access attempt — successful or denied — is logged with the user, action, file, and timestamp.

## Features

- **Authentication** — users log in with credentials; unregistered/invalid users are rejected.
- **Role-based access control** — each file action (view, edit) is checked against the requesting user's role.
- **Access logging** — every attempt (allowed or denied) is recorded for audit purposes.
- **Encryption** — files are encrypted at rest; data in transit is protected.
- **Session security** — sessions expire and cannot be reused after logout.

## Getting started

Requires Python 3.11+ and Git.

```bash
git clone git@github.com:<org>/bim-file-security-system.git
cd bim-file-security-system
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # set SECRET_KEY, DATABASE_URL, encryption key
```

## Running the app

```bash
flask run                        # starts the server (default: http://localhost:5000)
```

Seed sample users and roles:

```bash
python seed_data.py              # creates one user per role (architect, engineer, contractor, client)
```

## Running tests

```bash
pytest                           # full suite
pytest -m access                 # access-control tests only
pytest tests/test_auth.py        # one file
pytest -k "unauthorised"         # one test
```

Markers: `auth`, `access`, `logging`, `encryption`, `session`, `negative`.

## Project structure

```
app/              Application code (routes, models, auth, permissions)
tests/            pytest suite
test_data/        Seed users, roles, sample BIM files
requirements/     Documented requirements, one file per area
reports/          Test results
evidence/         Failure evidence
```

## What is tested

| Area | Expected behaviour |
|---|---|
| Authentication | Only registered users can log in |
| Access control | Each role can only perform actions it's permitted to (view/edit/denied) |
| Unauthorised access | Users without an account, or with an invalid role, are denied and logged |
| Access logging | Every file access attempt is recorded with user, action, file, and timestamp |
| Encryption | Files are encrypted at rest; sensitive data is protected in transit |
| Session security | Sessions expire, invalidate on logout, and cannot be reused |

## Traceability

Requirements use IDs (`AUTH-001`, `AC-001`, `LOG-001`, `ENC-001`, `SESS-001`) defined under `requirements/`. Every test links to the requirement it covers:

```python
@pytest.mark.access
@pytest.mark.requirement("AC-002")
def test_contractor_cannot_edit_file(api, access_log):
    """AC-002: Contractors have view-only access and must not be able to edit files."""
    response = api.edit_file(role="contractor", file_id="bim_001")
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert access_log.latest(action="edit_attempt")["result"] == "denied"
```

Example manual test case:

> **Test:** Try accessing the construction-site dashboard using an unauthorised account.
> **Expected:** Access denied and event logged.
> **Actual:** Access denied and event logged.
> **Result:** PASS ✅

## Workflow

Requirement → test case → automated test → execution. On failure, a defect is raised with reproduction steps, expected vs actual result, and evidence, then retested after the fix.

A feature is done when the requirement is documented, tests are automated and passing, defects are closed and retested, and evidence is collected.

## Out of scope

Penetration testing, load testing, production deployment, physical site security, and BIM file *rendering/viewing* functionality beyond access control.

## Team

- 🏗️ **Project/Business** — defines requirements (who needs what access, and why)
- 🔐 **Development** — builds authentication, access control, logging, and encryption
- 🧪 **QA** — writes and runs tests, documents results, tracks defects to closure