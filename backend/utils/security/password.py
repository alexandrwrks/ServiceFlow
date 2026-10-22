from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()


def hashed_password(password: str) -> str:
    return ph.hash(password)

def verify_password(hash_password: str, password: str) -> bool:
    try:
        return ph.verify(hash_password, password)
    except VerifyMismatchError:
        return False