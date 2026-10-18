# BIM File Security System

A Python-based role-based access control (RBAC) system for securing Building Information Modelling (BIM) files.

The system is designed to protect sensitive construction project information such as architectural drawings, engineering models, site plans, and related project files. Different user roles receive different levels of access based on their responsibilities.

The project covers five areas: authentication, role-based access control, access logging, encryption, and session security.

## Access Model

| Role              | Permission  |
| ----------------- | ----------- |
| Architect         | View / Edit |
| Engineer          | View / Edit |
| Contractor        | View        |
| Client            | View        |
| Unauthorised user | Denied      |

Every access attempt, whether successful or denied, is recorded with the user, action, file, result, and timestamp.

## Features

* **Authentication**: users provide credentials and only registered users with correct credentials are accepted. Every login attempt is logged.
* **Role-Based Access Control**: file actions are checked against the user's assigned role. Every file access attempt is logged.
* **Access Logging**: successful and denied attempts are recorded for auditing. Passwords are never logged.
* **Encryption**: BIM files are encrypted before they are saved and decrypted when they are read.
* **Session Security**: sessions expire after inactivity and cannot be reused after logout.
* **Terminal-Based Execution**: components are plain Python modules that can be run and checked from the terminal.

## Current Status

| Component        | Module                | Status                                                              |
| ---------------- | --------------------- | ------------------------------------------------------------------- |
| Authentication   | `authentication.py`   | Implemented (`login`, logs every attempt)                           |
| Access Control   | `access_control.py`   | Implemented (`check_access`, `access_file` which logs every attempt) |
| Access Logging   | `audit_log.py`        | Implemented (in-memory log)                                         |
| Encryption       | `encryption.py`       | Implemented (`store_file`, `read_file`)                             |
| Session Security | `session_security.py` | Implemented                                                         |

## Getting Started

### Requirements

* Python 3.11+
* Git
* The `cryptography` package (used by `encryption.py`)

Clone the repository:

```bash
git clone git@github.com:<org>/bim-file-security-system.git
cd bim-file-security-system
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

Install the dependency:

```bash
pip install cryptography
```

### Environment variables

Encryption reads two environment variables every time it is used:

| Variable             | Purpose                                    |
| -------------------- | ------------------------------------------ |
| `BIM_ENCRYPTION_KEY` | The encryption key                         |
| `BIM_STORAGE_DIR`    | The folder where encrypted files are saved |

Create a key:

```bash
python -c "from encryption import generate_key; print(generate_key())"
```

Set the variables.

**Windows PowerShell:**

```powershell
$env:BIM_ENCRYPTION_KEY = "<the key from above>"
$env:BIM_STORAGE_DIR = ".\storage"
```

**Linux/macOS:**

```bash
export BIM_ENCRYPTION_KEY="<the key from above>"
export BIM_STORAGE_DIR="./storage"
```

Keep the key private and never commit it to Git. Files encrypted with one key cannot be read with another.

## Running the System

The system runs through Python modules and terminal commands rather than a web application. Start Python in the project folder and import the component you want to check.

**Authentication**

```python
from authentication import login

login("valid_user", "correct_password")   # True
login("valid_user", "wrong_password")     # False
login(None, None)                         # False (no crash)
```

**Access control**

```python
from access_control import check_access, access_file

check_access("architect", "edit")         # True
check_access("contractor", "edit")        # False
check_access("unknown_user", "view")      # False

# access_file() does the same check and also writes a log entry
access_file("contractor", "edit", "plan.bim")   # False, logged as denied
```

**Sessions**

```python
from session_security import create_session, validate_session, logout

token = create_session("architect")
validate_session(token)                   # True
logout(token)
validate_session(token)                   # False
```

**Encryption** (needs the environment variables above)

```python
from encryption import store_file, read_file

store_file("plan.bim", b"floor plan data")   # saved encrypted on disk
read_file("plan.bim")                        # b"floor plan data"
```

**Logging**

```python
from audit_log import get_log_entries, clear_log

clear_log()
access_file("contractor", "edit", "plan.bim")
get_log_entries()
# [{'username': 'contractor', 'action': 'edit', 'file': 'plan.bim',
#   'timestamp': ..., 'result': 'denied'}]
```

Each log entry has these fields:

| Field       | Meaning                                                              |
| ----------- | -------------------------------------------------------------------- |
| `username`  | Who made the attempt                                                 |
| `action`    | What they tried to do (`login`, `view`, `edit`, ...)                 |
| `file`      | Which file was involved (`None` for a login)                         |
| `timestamp` | When it happened (seconds since the epoch)                           |
| `result`    | `success` / `failure` for logins, `allowed` / `denied` for file access |

## Sample Users

Access control recognises these users:

| Username   | Role       |
| ---------- | ---------- |
| architect  | Architect  |
| engineer   | Engineer   |
| contractor | Contractor |
| client     | Client     |

Any other username is treated as an unauthorised user and is denied.

Authentication currently has a single test account for login checks:

| Username     | Password           |
| ------------ | ------------------ |
| `valid_user` | `correct_password` |

This account is for testing only. Real credentials must never be stored in the source code.

## Project Structure

```text
BIM-File-Security-System/
│
├── authentication.py       Login check (logs every attempt)
├── access_control.py       Roles, permissions, check_access() and access_file()
├── audit_log.py            Access log (log_event, log_login, log_access, get_log_entries, clear_log)
├── encryption.py           Encrypt, decrypt, store and read files
├── session_security.py     Session creation, expiry and logout
└── README.md               Project documentation
```

The structure may expand as additional functionality is implemented.

## Known Limitations

* Logging is kept in memory, so the log is lost when the program stops.
* The user list and the test account are stored in the source code, for testing only.
* `login()` does not create a session yet, and file access does not check for a valid session. The components work on their own and are not yet connected into one flow.
* `store_file()` and `read_file()` do not check the user's role. Role checks happen in `check_access()` / `access_file()`.

## What is Tested

The separate QA repository independently verifies the behaviour of the Development system.

| Area                | Expected Behaviour                                                 |
| ------------------- | ------------------------------------------------------------------ |
| Authentication      | Only registered users with correct credentials can log in          |
| Access Control      | Users can only perform actions permitted by their role             |
| Unauthorised Access | Unregistered or invalid users are denied                           |
| Access Logging      | Every login and file access attempt is recorded                    |
| Encryption          | Stored files are encrypted, and wrong keys or changes are rejected |
| Session Security    | Sessions expire and cannot be reused after logout                  |

## Requirements

Every requirement has a unique ID so it can be linked to test cases.

### Authentication

| ID       | Requirement                                                                                                                                  |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| AUTH-001 | A registered user providing the correct password must be authenticated successfully.                                                         |
| AUTH-002 | An unregistered username must be rejected.                                                                                                   |
| AUTH-003 | A registered username with an incorrect password must be rejected.                                                                           |
| AUTH-004 | Empty or missing credentials must be rejected without causing the system to crash.                                                           |
| AUTH-005 | Basic injection-style input in the username or password must be safely rejected, without exposing internal errors or implementation details. |

### Access Control

| ID     | Requirement                                                                                     |
| ------ | ----------------------------------------------------------------------------------------------- |
| AC-001 | Architects can view and edit BIM files.                                                         |
| AC-002 | Engineers can view and edit BIM files.                                                          |
| AC-003 | Contractors can view BIM files but cannot edit them.                                            |
| AC-004 | Clients can view BIM files but cannot edit them.                                                |
| AC-005 | Unregistered users, missing usernames, missing actions and unrecognised actions must be denied. |

### Logging

| ID      | Requirement                                                        |
| ------- | ------------------------------------------------------------------ |
| LOG-001 | Every login attempt, successful or failed, creates a log entry.    |
| LOG-002 | Every file access attempt, allowed or denied, creates a log entry. |
| LOG-003 | Log entries contain who, what action, which file, and when.        |
| LOG-004 | Denied actions are logged as denied, not silently dropped.         |

### Encryption

| ID      | Requirement                                                                                                   |
| ------- | ------------------------------------------------------------------------------------------------------------- |
| ENC-001 | Files are stored encrypted. The file on disk must not contain the original content.                           |
| ENC-002 | A stored file must decrypt back to exactly the original content.                                              |
| ENC-003 | A wrong key, changed data, or a cut-off file must be rejected, and errors must not reveal the key or content. |
| ENC-004 | Bad input (wrong data type, unsafe file names, missing file, missing or invalid key) must be rejected safely. |

### Session Security

| ID       | Requirement                                                         |
| -------- | ------------------------------------------------------------------- |
| SESS-001 | A created session is valid and has a unique token.                  |
| SESS-002 | Logging out ends the session, and the old token stops working.      |
| SESS-003 | Sessions expire after 30 minutes of inactivity.                     |
| SESS-004 | Expired or logged-out tokens are always rejected when reused.       |
| SESS-005 | Missing, unknown or malformed tokens are rejected without crashing. |

## QA Integration

The Development and QA repositories are separate.

The **Development repository** contains the actual BIM File Security System.

The **QA repository** contains the independent automated test suite.

The QA tests interact with the Development system and verify that its behaviour matches the documented requirements.

```text
Development Repository
        │
        │ System functionality
        ▼
BIM File Security System
        ▲
        │
        │ Independent testing
        │
QA Repository
        │
        ▼
pytest
        │
        ▼
Terminal Results
PASS / FAIL
```

The QA repository must not duplicate the Development implementation simply to make its tests pass.

## Traceability

Each QA test identifies the requirement it verifies, so every requirement can be linked to one or more test cases.

| Prefix  | Area             | Range                    |
| ------- | ---------------- | ------------------------ |
| `AUTH-` | Authentication   | `AUTH-001` to `AUTH-005` |
| `AC-`   | Access Control   | `AC-001` to `AC-005`     |
| `LOG-`  | Logging          | `LOG-001` to `LOG-004`   |
| `ENC-`  | Encryption       | `ENC-001` to `ENC-004`   |
| `SESS-` | Session Security | `SESS-001` to `SESS-005` |

## Development and QA Workflow

The project follows this workflow:

```text
Requirement
     ↓
Test Case
     ↓
Development Implementation
     ↓
QA Automated Test
     ↓
Test Execution
     ↓
PASS / FAIL
     ↓
Defect Investigation
     ↓
Fix
     ↓
Retest
```

A feature is considered complete when:

* The requirement is documented.
* The Development implementation is completed.
* QA tests have been created.
* Tests pass.
* Any defects have been fixed and retested.
* Appropriate evidence and test reports have been collected.

## Out of Scope

The following are outside the scope of this project:

* Penetration testing
* Load and performance testing
* Production deployment
* Physical site security
* BIM file rendering or viewing functionality beyond access control
* Building a graphical user interface or web application

## Team Responsibilities

### Project / Business

Defines the BIM security requirements, user roles, permissions, and expected behaviour.

### Development

Implements authentication, access control, logging, encryption, and session security.

### QA

Creates and executes independent tests, records results, identifies defects, collects evidence, and verifies fixes.

## Project Goal

The goal is to demonstrate a secure, testable BIM file security system while maintaining a clear separation between **Development implementation** and **QA verification**.