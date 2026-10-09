"""
encryption.py

Encrypts BIM file data before it is written to disk, and decrypts it again
when it is read back.

Interface (matches tests/pytest/test_encryption.py and
tests/Unit_test/test_encryption.py):

    generate_key()              -> new key (str)
    encrypt_data(data: bytes)   -> ciphertext (bytes)
    decrypt_data(token: bytes)  -> original bytes
    store_file(name, data)      -> path of the encrypted file on disk
    read_file(name)             -> original bytes
    EncryptionError             -> raised for every failure

Configuration (read every time a function is called, never cached):

    BIM_ENCRYPTION_KEY   the key, as produced by generate_key()
    BIM_STORAGE_DIR      the folder encrypted files are stored in

How it works:

    Fernet (from the "cryptography" package) is used for the encryption.
    It encrypts with AES-128 and signs the result with HMAC-SHA256, so:
      - the same data encrypts differently every time (random IV),
      - a wrong key, a changed byte, or a cut-off file is detected and
        rejected instead of returning garbage.

    Install the dependency with:   pip install cryptography

Safety rules:

    - Every failure raises EncryptionError. Messages never contain the key
      or the file content.
    - File names must be plain names. Anything that could point outside the
      storage folder (../, /, \\, ., ..) is rejected.
    - Files are written to a temporary file first and then moved into place,
      so a failed store never leaves a half-written or plaintext file.
    - Stored files are readable only by the owner (mode 0600).
"""

