from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import secrets


SESSION_DAYS = 14


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def generate_user_id() -> str:
    return f"user_{secrets.token_hex(4)}"


def trusted_until_iso(days: int = SESSION_DAYS) -> str:
    return (datetime.now(timezone.utc) + timedelta(days=days)).isoformat(timespec="seconds")


def make_trust_signature(user_id: str, trusted_until: str, access_code: str) -> str:
    message = f"{user_id}:{trusted_until}".encode("utf-8")
    secret = access_code.encode("utf-8")
    return hmac.new(secret, message, hashlib.sha256).hexdigest()


def is_trusted_until_valid(value: str | None) -> bool:
    if not value:
        return False

    normalized_value = str(value).strip()
    if normalized_value.endswith("Z"):
        normalized_value = normalized_value[:-1] + "+00:00"

    try:
        trusted_until = datetime.fromisoformat(normalized_value)
    except ValueError:
        return False

    if trusted_until.tzinfo is None:
        trusted_until = trusted_until.replace(tzinfo=timezone.utc)

    return trusted_until > datetime.now(timezone.utc)


def is_trusted_session_valid(
    user_id: str | None,
    trusted_until: str | None,
    signature: str | None,
    access_code: str,
) -> bool:
    if not user_id or not trusted_until or not signature or not access_code:
        return False
    if not is_trusted_until_valid(trusted_until):
        return False

    expected_signature = make_trust_signature(user_id, trusted_until, access_code)
    return hmac.compare_digest(str(signature), expected_signature)
