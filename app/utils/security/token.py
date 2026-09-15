import hashlib


def hashed_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def verify_token(hash_token: str, token: str) -> bool:
    return hashlib.sha256(token.encode()).hexdigest() == hash_token