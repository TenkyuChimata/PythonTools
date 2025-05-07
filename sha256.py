# -*- coding: utf-8 -*-
import time
import uuid
import hashlib

def encrypt_string_sha256(string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(string.encode("utf-8"))
    encrypted_string = sha256_hash.hexdigest()
    return encrypted_string

for i in range(50):
    print(encrypt_string_sha256(str(uuid.uuid4())))

time.sleep(999)
