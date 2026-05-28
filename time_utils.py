from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo


WEEKDAYS = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
MONTHS = [
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember",
]


def _parse_datetime(value: str, timezone: str) -> datetime | None:
    if not value:
        return None

    normalized_value = str(value).strip()
    if not normalized_value:
        return None

    if normalized_value.endswith("Z"):
        normalized_value = normalized_value[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(normalized_value)
    except ValueError:
        return None

    local_zone = ZoneInfo(timezone)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=local_zone)
    return parsed.astimezone(local_zone)


def _parse_date(value: str) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(str(value).strip()[:10])
    except ValueError:
        return None


def format_human_time(
    created_at: str | None,
    timezone: str = "Asia/Jakarta",
    journal_date: str | None = None,
) -> str:
    local_zone = ZoneInfo(timezone)
    now = datetime.now(local_zone)
    local_time = _parse_datetime(str(created_at or ""), timezone)

    if not local_time:
        fallback_date = _parse_date(str(journal_date or ""))
        if fallback_date:
            return f"{fallback_date.day} {MONTHS[fallback_date.month - 1]} {fallback_date.year}"
        return "-"

    entry_date = local_time.date()
    time_text = local_time.strftime("%H:%M")

    if entry_date == now.date():
        return f"Hari ini, {time_text}"

    if entry_date == now.date() - timedelta(days=1):
        return f"Kemarin, {time_text}"

    start_of_week = now.date() - timedelta(days=now.weekday())
    if start_of_week <= entry_date <= now.date():
        return f"{WEEKDAYS[entry_date.weekday()]}, {time_text}"

    return f"{entry_date.day} {MONTHS[entry_date.month - 1]} {entry_date.year}, {time_text}"
