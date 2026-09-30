#!/usr/bin/python3
"""Read legacy Electron v11 device keys through the desktop's Secret Service.

The request and response are base64-encoded on stdin/stdout so key material is
never placed in process arguments or diagnostics. No key material is persisted
outside the Secret Service and the existing device-key store.
"""

import base64
import hashlib
import json
import os
import sys

import gi

gi.require_version("Secret", "1")
from gi.repository import Secret  # noqa: E402
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # noqa: E402
from cryptography.hazmat.primitives.padding import PKCS7  # noqa: E402


SCHEMA = Secret.Schema.new(
    "chrome_libsecret_os_crypt_password_v2",
    Secret.SchemaFlags.DONT_MATCH_NAME,
    {"application": Secret.SchemaAttributeType.STRING},
)
ATTRIBUTES = {"application": "ChatGPT"}
IV = b" " * 16


def password(create):
    value = Secret.password_lookup_sync(SCHEMA, ATTRIBUTES, None)
    if value is None and create:
        value = base64.b64encode(os.urandom(16)).decode("ascii")
        if not Secret.password_store_sync(
            SCHEMA, ATTRIBUTES, Secret.COLLECTION_DEFAULT,
            "Chromium Safe Storage", value, None,
        ):
            raise RuntimeError("Secret Service did not save the encryption key")
    if value is None:
        raise RuntimeError("ChatGPT Secret Service key is unavailable")
    return value


def main():
    request = json.loads(sys.stdin.buffer.read(65537))
    operation = request.get("operation")
    if operation not in ("probe", "encrypt", "decrypt"):
        raise ValueError("invalid operation")
    if operation == "probe":
        password(True)
        sys.stdout.write("ok\n")
        return
    value = base64.b64decode(request["data"], validate=True)
    if len(value) > 32768:
        raise ValueError("input is too large")
    key = hashlib.pbkdf2_hmac("sha1", password(operation == "encrypt").encode(), b"saltysalt", 1, 16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(IV))
    if operation == "encrypt":
        padder = PKCS7(128).padder()
        padded = padder.update(value) + padder.finalize()
        encryptor = cipher.encryptor()
        result = b"v11" + encryptor.update(padded) + encryptor.finalize()
    else:
        if not value.startswith(b"v11") or (len(value) - 3) % 16:
            raise ValueError("unsupported ciphertext")
        decryptor = cipher.decryptor()
        padded = decryptor.update(value[3:]) + decryptor.finalize()
        unpadder = PKCS7(128).unpadder()
        result = unpadder.update(padded) + unpadder.finalize()
    sys.stdout.write(base64.b64encode(result).decode("ascii") + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"libsecret bridge failed: {type(error).__name__}", file=sys.stderr)
        sys.exit(1)
