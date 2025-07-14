import hashlib

def hash_file(filename):
    return hashlib.sha256(filename.encode()).hexdigest()
