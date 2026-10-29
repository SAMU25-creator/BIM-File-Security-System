"""Demo for the BIM File Security System video.
Run from the dev folder:  python demo.py
Press Enter to move to the next section."""
import os
import session_security
from authentication import login
from access_control import check_access, access_file
from audit_log import get_log_entries, clear_log
from encryption import store_file, read_file, generate_key, EncryptionError
from session_security import create_session, validate_session, logout


def section(title):
    input(f"\n\n>>> Press Enter for: {title}")
    print("=" * 60)
    print(title)
    print("=" * 60)


def show(code):
    """Print the line, then run it and print the result."""
    print(f"\n>>> {code}")
    print(eval(code))


clear_log()

section("1. AUTHENTICATION")
show('login("valid_user", "correct_password")')
show('login("valid_user", "wrong_password")')
show('''login("' OR '1'='1", "x")''')
show('login(None, None)')

section("2. ACCESS CONTROL")
print("\nuser          view    edit")
for u in ["architect", "engineer", "contractor", "client", "stranger"]:
    print(f"{u:<13} {str(check_access(u, 'view')):<7} {check_access(u, 'edit')}")

section("3. AUDIT LOG")
show('access_file("contractor", "edit", "building_model.ifc")')
print("\nLog entries so far:")
for e in get_log_entries():
    print(e)

section("4. ENCRYPTION")
show('store_file("plan.bim", b"Level 2 floor plan - CONFIDENTIAL")')
path = os.path.join(os.environ["BIM_STORAGE_DIR"], "plan.bim")
print("\nWhat is really on disk (first 60 bytes):")
print(open(path, "rb").read()[:60])
show('read_file("plan.bim")')

print("\nNow with a DIFFERENT key:")
real_key = os.environ["BIM_ENCRYPTION_KEY"]
os.environ["BIM_ENCRYPTION_KEY"] = generate_key()
try:
    read_file("plan.bim")
except EncryptionError as err:
    print("Rejected safely ->", err)
os.environ["BIM_ENCRYPTION_KEY"] = real_key

print("\nUnsafe file name:")
try:
    store_file("../escape.bim", b"x")
except EncryptionError as err:
    print("Rejected safely ->", err)

section("5. SESSIONS")
t = create_session("architect")
print("\nSession created. Token starts:", t[:8] + "...")
show("validate_session(t)")
logout(t)
print("\nAfter logout:")
show("validate_session(t)")

print("\nExpiry (simulated: moving the clock forward 31 minutes):")
t2 = create_session("client")
session_security._SESSIONS[t2]["last_active"] -= 31 * 60
show("validate_session(t2)")

print("\n\nDone. Thank you!")