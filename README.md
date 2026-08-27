# BIM File Security System

A Python-based role-based access control (RBAC) system for securing Building Information Modelling (BIM) files.

The system is designed to protect sensitive construction project information such as architectural drawings, engineering models, site plans, and related project files. Different user roles receive different levels of access based on their responsibilities.

The project focuses on authentication, role-based access control, access logging, encryption, and session security.

## Access Model

| Role              | Permission  |
| ----------------- | ----------- |
| Architect         | View / Edit |
| Engineer          | View / Edit |
| Contractor        | View        |
| Client            | View        |
| Unauthorised user | Denied      |

Every access attempt — whether successful or denied — must be recorded with the user, action, file, result, and timestamp.

## Features

* **Authentication** — users provide credentials and only registered users with correct credentials are accepted.
* **Role-Based Access Control** — file actions are checked against the user's assigned role.
* **Access Logging** — successful and denied access attempts are recorded for auditing.
* **Encryption** — sensitive BIM files and protected data are encrypted where required.
* **Session Security** — sessions expire and cannot be reused after logout.
* **Terminal-Based Execution** — system operations and results can be executed and viewed from the terminal.

## Getting Started

### Requirements

* Python 3.11+
* Git

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

Install the project dependencies:

```bash
pip install -r requirements.txt
```

If environment variables are required, create a `.env` file from the provided example:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

## Running the System

The system is designed to run through Python modules and terminal commands rather than through a web application.

Individual system components can be executed and tested from the terminal.

For example:

```bash
python authentication.py
```

As additional security components are implemented, corresponding modules and commands will be documented here.

## Sample Users

The system will contain test users representing the supported roles:

| Username   | Role       |
| ---------- | ---------- |
| architect  | Architect  |
| engineer   | Engineer   |
| contractor | Contractor |
| client     | Client     |

Unauthorised users must not be granted access.

Sample user data will be maintained separately from the application logic.

## Project Structure

```text
BIM-File-Security-System/
│
├── authentication.py       Authentication logic
├── access_control.py       Role and permission logic
├── logging_system.py       Access logging
├── encryption.py           Encryption functionality
├── session.py              Session management
├── test_data/              Sample users and BIM file data
├── requirements/           Project requirements
├── README.md               Project documentation
└── .gitignore              Git exclusions
```

The structure may expand as additional functionality is implemented.

## What is Tested

The separate QA repository independently verifies the behaviour of the Development system.

| Area                | Expected Behaviour                                            |
| ------------------- | ------------------------------------------------------------- |
| Authentication      | Only registered users with correct credentials can log in     |
| Access Control      | Users can only perform actions permitted by their role        |
| Unauthorised Access | Unregistered or invalid users are denied                      |
| Access Logging      | Every access attempt is recorded                              |
| Encryption          | Protected BIM files and sensitive data are securely encrypted |
| Session Security    | Sessions expire and cannot be reused after logout             |

## Authentication Requirements

The authentication component must satisfy the following requirements:

### AUTH-001 — Valid Credentials

A registered user providing the correct password must be authenticated successfully.

### AUTH-002 — Invalid Username

An unregistered username must be rejected.

### AUTH-003 — Incorrect Password

A registered username with an incorrect password must be rejected.

### AUTH-004 — Empty or Missing Credentials

Empty or missing credentials must be rejected without causing the system to crash.

### AUTH-005 — Injection-Safe Authentication

Basic injection-style input in the username or password fields must be safely rejected without exposing internal errors or sensitive implementation details.

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

Requirements are assigned unique IDs so that each requirement can be linked to one or more test cases.

Current requirement groups include:

* `AUTH-001` to `AUTH-005` — Authentication
* `AC-001` onward — Access Control
* `LOG-001` onward — Logging
* `ENC-001` onward — Encryption
* `SESS-001` onward — Session Security

Each QA test should identify the requirement it verifies.

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
