"""
encryption.py

File encryption for the BIM File Security System.

BIM files are encrypted before they are written to disk, so what sits in
storage is never readable plaintext. Uses Fernet from the `cryptography`
package (AES-128-CBC + HMAC-SHA256), which is authenticated: tampered or
corrupted data is detected on decrypt rather than returned as garbage.

Covers:
    ENC-001 - Files are stored encrypted on disk, never as plaintext.
    ENC-002 - A stored file decrypts back to the exact original bytes
              when the correct key is used.
    ENC-003 - A wrong key, or tampered/corrupted data, is rejected and
              never returns data.
    ENC-004 - Bad input (None, wrong type, unsafe filenames, missing or
              invalid key) is rejected safely with an EncryptionError that
              does not leak internal details.

Configuration (environment variables, e.g. from .env):
    BIM_ENCRYPTION_KEY  Fernet key. Create one with generate_key().
                        Never commit a real key to the repository.
    BIM_STORAGE_DIR     Folder for encrypted files.
                        Default: "encrypted_storage" next to this file.

Note: the system has no network layer (it runs from the terminal), so
there is no "data in transit" code here. Encryption covers data at rest.
"""

import os
import tempfile

from cryptography.fernet import Fernet, InvalidToken

KEY_ENV_VAR = "BIM_ENCRYPTION_KEY"
STORAGE_ENV_VAR = "BIM_STORAGE_DIR"
DEFAULT_STORAGE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "encrypted_storage"
)


class EncryptionError(Exception):
    """Raised for any encryption/decryption failure.

    Messages are deliberately generic so they never expose keys, file
    contents, or internal paths.
    """


def generate_key():
    """Return a new random key (str) suitable for BIM_ENCRYPTION_KEY."""
    return Fernet.generate_key().decode()


def _get_fernet():
    """Build a Fernet object from the configured key."""
    key = os.environ.get(KEY_ENV_VAR)
    if not key:
        raise EncryptionError("Encryption key is not configured.")
    try:
        return Fernet(key.encode())
    except (ValueError, TypeError):
        raise EncryptionError("Encryption key is invalid.") from None


def _storage_dir():
    return os.environ.get(STORAGE_ENV_VAR) or DEFAULT_STORAGE_DIR


def _storage_path(filename):
    """Validate a filename and return its full path inside the storage dir.

    Only plain file names are allowed: no folders, no '..', no empty or
    non-string values. This stops a caller writing or reading outside the
    storage folder.
    """
    if not isinstance(filename, str) or not filename.strip():
        raise EncryptionError("Invalid filename.")
    if "\x00" in filename or filename in (".", ".."):
        raise EncryptionError("Invalid filename.")
    if os.path.basename(filename) != filename or "/" in filename or "\\" in filename:
        raise EncryptionError("Invalid filename.")
    return os.path.join(_storage_dir(), filename)


def encrypt_data(data):
    """Encrypt bytes and return the ciphertext (bytes)."""
    if not isinstance(data, (bytes, bytearray)):
        raise EncryptionError("Data must be bytes.")
    return _get_fernet().encrypt(bytes(data))


def decrypt_data(token):
    """Decrypt ciphertext produced by encrypt_data and return the bytes.

    Raises EncryptionError for a wrong key or tampered/corrupted data.
    """
    if not isinstance(token, (bytes, bytearray)):
        raise EncryptionError("Encrypted data must be bytes.")
    try:
        return _get_fernet().decrypt(bytes(token))
    except InvalidToken:
        raise EncryptionError("Decryption failed.") from None


def store_file(filename, data):
    """Encrypt data and write it to storage. Returns the stored file's path.

    The plaintext is never written to disk. The ciphertext is written to a
    temporary file first and then moved into place, so a crash can't leave
    a half-written file under the real name.
    """
    path = _storage_path(filename)
    ciphertext = encrypt_data(data)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as tmp:
            tmp.write(ciphertext)
        os.replace(tmp_path, path)
    except OSError:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise EncryptionError("Could not store file.") from None
    return path


def read_file(filename):
    """Read an encrypted file from storage and return the decrypted bytes."""
    path = _storage_path(filename)
    try:
        with open(path, "rb") as f:
            ciphertext = f.read()
    except OSError:
        raise EncryptionError("Could not read file.") from None
    return decrypt_data(ciphertext)


if __name__ == "__main__":
    # Quick terminal demo: python encryption.py
    if not os.environ.get(KEY_ENV_VAR):
        os.environ[KEY_ENV_VAR] = generate_key()
        print(f"{KEY_ENV_VAR} not set - using a temporary key for this demo.")

    sample = b"Level 2 floor plan - CONFIDENTIAL"
    saved_to = store_file("demo_floor_plan.bim", sample)

    with open(saved_to, "rb") as f:
        on_disk = f.read()

    print("Stored at:      ", saved_to)
    print("Plaintext on disk?", sample in on_disk)
    print("Round trip OK?  ", read_file("demo_floor_plan.bim") == sample)