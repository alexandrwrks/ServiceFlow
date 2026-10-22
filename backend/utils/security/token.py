import hashlib
import uuid
from datetime import datetime, timezone, timedelta
from typing import Tuple


def hashed_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def verify_token(hash_token: str, token: str) -> bool:
    return hashlib.sha256(token.encode()).hexdigest() == hash_token

def create_invitation_token() -> Tuple[str, str, datetime]:
    token = uuid.uuid4().hex
    token_hash = hashed_token(token)
    expired_at = datetime.now(timezone.utc) + timedelta(days=3)

    return token, token_hash, expired_at