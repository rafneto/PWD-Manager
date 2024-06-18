from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import getpass

def create_key():
    """
    Prompt the user to enter the encryption key and derive it using PBKDF2.

    Returns:
        bytes: The derived key from the entered passphrase.
    """
    password = getpass.getpass("Enter the encryption key: ")
    salt = generate_salt()
    key = PBKDF2(password, salt, dkLen=32)
    
    # Save the derived key to a file
    with open("key.bin", "wb") as f:
        f.write(key)
    
    return key

def get_key():
    """
    Retrieve the encryption key from the saved file.

    Returns:
        bytes: The encryption key.
    """
    with open("key.bin", "rb") as f:
        return f.read()

def generate_salt():
    """
    Generate a random salt for key derivation.

    Returns:
        bytes: The generated salt.
    """
    return get_random_bytes(16)

def encrypt_password(password, key):
    """
    Encrypt a password.

    Args:
        password (str): The plain text password to encrypt.
        key (bytes): The encryption key.

    Returns:
        str: The encrypted password encoded in base64.
    """
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(password.encode())
    return b64encode(nonce + tag + ciphertext).decode('utf-8')

def decrypt_password(encrypted_password, key):
    """
    Decrypt an encrypted password.

    Args:
        encrypted_password (str): The encrypted password encoded in base64.
        key (bytes): The encryption key.

    Returns:
        str: The decrypted password.
    """
    encrypted_data = b64decode(encrypted_password)
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_password = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_password.decode('utf-8')
