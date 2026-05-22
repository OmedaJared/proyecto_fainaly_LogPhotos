from datetime import datetime, timedelta
import secrets

RESET_TOKEN_TTL_MINUTES = 30

def create_reset_token(email: str) -> str:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_TTL_MINUTES)
    return token, expires_at

def validate_reset_token(token: str, expires_at: datetime) -> bool:
    return datetime.utcnow() < expires_at