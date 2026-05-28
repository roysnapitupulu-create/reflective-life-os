from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import secrets
from typing import Any

try:
    from streamlit_local_storage import LocalStorage
except Exception:
    LocalStorage = None


SESSION_DAYS = 14
STORAGE_USER_ID = "rlos_user_id"
STORAGE_TRUSTED_UNTIL = "rlos_trusted_until"
STORAGE_TRUST_SIG = "rlos_trust_sig"


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


def _query_get(st: Any, name: str) -> str:
    try:
        value = st.query_params.get(name, "")
    except Exception:
        return ""
    if isinstance(value, list):
        return str(value[0]) if value else ""
    return str(value or "")


def _query_set(st: Any, name: str, value: str) -> None:
    try:
        st.query_params[name] = value
    except Exception:
        pass


def _local_storage_available() -> bool:
    return LocalStorage is not None


def _storage_get(key: str, component_key: str) -> str:
    if LocalStorage is None:
        return ""
    try:
        value = LocalStorage().getItem(key, key=component_key)
    except TypeError:
        value = LocalStorage().getItem(key)
    except Exception:
        return ""
    return str(value or "")


def _storage_set(key: str, value: str, component_key: str) -> None:
    if LocalStorage is None:
        return
    try:
        LocalStorage().setItem(key, value, key=component_key)
    except TypeError:
        LocalStorage().setItem(key, value)
    except Exception:
        return


def _storage_ready(st: Any) -> bool:
    return True


def get_or_create_user_id(st: Any) -> tuple[str | None, bool]:
    if not _storage_ready(st):
        return None, False

    user_id = _storage_get(STORAGE_USER_ID, "rlos_get_user_id")
    if not user_id:
        user_id = _query_get(st, "rid")
    if not user_id:
        user_id = st.session_state.get("user_id", "")
    if not user_id:
        user_id = generate_user_id()

    st.session_state["user_id"] = user_id
    _storage_set(STORAGE_USER_ID, user_id, "rlos_set_user_id")
    _query_set(st, "rid", user_id)
    return user_id, True


def is_access_trusted(st: Any, access_code: str) -> tuple[bool, str | None, bool]:
    if not _storage_ready(st):
        return False, None, False

    user_id = _storage_get(STORAGE_USER_ID, "rlos_get_trusted_user_id") or _query_get(st, "rid")
    trusted_until = _storage_get(STORAGE_TRUSTED_UNTIL, "rlos_get_trusted_until") or _query_get(
        st, "trusted_until"
    )
    trust_sig = _storage_get(STORAGE_TRUST_SIG, "rlos_get_trust_sig") or _query_get(st, "trust_sig")

    trusted = is_trusted_session_valid(user_id, trusted_until, trust_sig, access_code)
    if trusted:
        st.session_state["access_granted"] = True
        st.session_state["user_id"] = user_id
        _query_set(st, "rid", user_id)
        _query_set(st, "trusted_until", trusted_until)
        _query_set(st, "trust_sig", trust_sig)
    return trusted, user_id or None, True


def mark_access_trusted(st: Any, user_id: str, access_code: str) -> None:
    trusted_until = trusted_until_iso()
    trust_sig = make_trust_signature(user_id, trusted_until, access_code)

    st.session_state["access_granted"] = True
    st.session_state["user_id"] = user_id
    _storage_set(STORAGE_USER_ID, user_id, "rlos_mark_user_id")
    _storage_set(STORAGE_TRUSTED_UNTIL, trusted_until, "rlos_mark_trusted_until")
    _storage_set(STORAGE_TRUST_SIG, trust_sig, "rlos_mark_trust_sig")
    _query_set(st, "rid", user_id)
    _query_set(st, "trusted_until", trusted_until)
    _query_set(st, "trust_sig", trust_sig)


def get_current_user_context(st: Any, access_code: str) -> dict[str, Any]:
    trusted, trusted_user_id, ready = is_access_trusted(st, access_code)
    if not ready:
        return {"storage_ready": False, "access_trusted": False, "user_id": None}
    if trusted:
        return {"storage_ready": True, "access_trusted": True, "user_id": trusted_user_id}

    user_id, user_ready = get_or_create_user_id(st)
    return {
        "storage_ready": user_ready,
        "access_trusted": bool(st.session_state.get("access_granted")),
        "user_id": user_id,
    }
