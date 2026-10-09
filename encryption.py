"""
encryption.py

Encrypts BIM file data before it is saved, and decrypts it when it is read.

    generate_key()              -> new key (str)
    encrypt_data(data: bytes)   -> ciphertext (bytes)
    decrypt_data(token: bytes)  -> original bytes
    store_file(name, data)      -> path of the encrypted file on disk
    read_file(name)             -> original bytes
    EncryptionError             -> raised for every failure

Settings are read from environment variables each time a function is called:

    BIM_ENCRYPTION_KEY   the key (create one with generate_key())
    BIM_STORAGE_DIR      the folder where encrypted files are saved

Uses Fernet from the "cryptography" package (pip install cryptography).
Fernet gives us two things for free: the same data encrypts differently every
time, and a wrong key or a changed file is detected instead of giving garbage.
"""

import os

from cryptography.fernet import Fernet, InvalidToken

KEY_ENV_VAR = "BIM_ENCRYPTION_KEY"
STORAGE_ENV_VAR = "BIM_STORAGE_DIR"


class EncryptionError(Exception):
    """Raised for every encryption, decryption, or file failure."""


# --- Key ---

def generate_key():
    """Return a new random key as a string."""
    return Fernet.generate_key().decode()


def _get_cipher():
    """Build the Fernet cipher from the key in the environment."""
    key = os.environ.get(KEY_ENV_VAR)
    if not key:
        raise EncryptionError("No encryption key is set.")

    try:
        return Fernet(key.encode())
    except ValueError:
        # The message never includes the key.
        raise EncryptionError("The encryption key is invalid.") from None


# --- Encrypt and decrypt bytes ---

def encrypt_data(data):
    """Encrypt bytes and return the ciphertext."""
    if not isinstance(data, bytes):
        raise EncryptionError("Data must be bytes.")

    return _get_cipher().encrypt(data)


def decrypt_data(token):
    """Decrypt ciphertext and return the original bytes."""
    if not isinstance(token, bytes):
        raise EncryptionError("Encrypted data must be bytes.")

    try:
        return _get_cipher().decrypt(token)
    except InvalidToken:
        # Wrong key, changed data, cut-off data, or data that was never encrypted.
        raise EncryptionError("Could not decrypt: wrong key or damaged data.") from None


# --- Store and read files ---

def _check_filename(name):
    """Allow plain file names only, so a file can never be saved outside the storage folder."""
    if not isinstance(name, str) or not name.strip():
        raise EncryptionError("The file name must be a non-empty string.")
    if name in (".", "..") or any(char in name for char in "/\\\0"):
        raise EncryptionError("The file name is not allowed.")


def _get_storage_folder():
    folder = os.environ.get(STORAGE_ENV_VAR)
    if not folder:
        raise EncryptionError("No storage folder is set.")
    return folder


def store_file(name, data):
    """Encrypt data and save it as <storage folder>/<name>. Returns the path."""
    _check_filename(name)
    token = encrypt_data(data)  # encrypt first, so a failure writes nothing
    folder = _get_storage_folder()
    path = os.path.join(folder, name)

    try:
        os.makedirs(folder, exist_ok=True)
        with open(path, "wb") as file:
            file.write(token)
    except OSError:
        raise EncryptionError("Could not save the file.") from None

    return path


def read_file(name):
    """Read <storage folder>/<name> and return the decrypted bytes."""
    _check_filename(name)
    path = os.path.join(_get_storage_folder(), name)

    try:
        with open(path, "rb") as file:
            token = file.read()
    except OSError:
        raise EncryptionError("Could not read the file.") from None

    return decrypt_data(token)