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

