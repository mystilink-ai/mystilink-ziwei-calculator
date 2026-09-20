"""Optional calendar engines: builtin (zhdate), lunar, external_basis."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from zoneinfo import ZoneInfo

from .chart import ChartInput, _assemble_chart_from_lunar, apply_true_solar_time


class CalendarEngineError(ValueError):
    """Invalid calendar engine selection or calendar-basis payload."""


LUNAR_MISSING_MSG = (
    "calendar_engine=lunar requires optional dependency mystilink-lunar. "
    "Install with: python3 -m pip install 'mystilink-ziwei-calculator[lunar]' "
    "(Python 3.10+). Or pass --calendar-basis from mystilink-lunar convert JSON."
)


def lunar_available() -> bool:
    try:
        import mystilink_lunar  # noqa: F401
    except ImportError:
        return False
    return True


def _require_lunar() -> None:
    if not lunar_available():
        raise CalendarEngineError(LUNAR_MISSING_MSG)


def _basis_subset(data: Dict[str, Any]) -> Dict[str, Any]:
    keys = (
        "schema_version",
        "solar",
        "lunar",
        "ganzhi",
        "zodiac",
        "rules",
        "solar_term",
        "provider",
    )
    out = {k: data[k] for k in keys if k in data}
    if "schema_version" not in out and "lunar" in out and "solar" in out:
        out["schema_version"] = "mystilink.calendar_basis/0.1"
    return out


def _parse_local_from_basis(basis: Dict[str, Any], inp: Optional[ChartInput]) -> datetime:
    if inp is not None:
        return inp.local_dt
    solar = basis.get("solar")
    if not isinstance(solar, dict):
        raise CalendarEngineError("calendar-basis.solar object is required when ChartInput is omitted")
    tz_name = solar.get("timezone")
    if not isinstance(tz_name, str) or not tz_name.strip():
        raise CalendarEngineError("calendar-basis.solar.timezone is required when ChartInput is omitted")
    dt_raw = solar.get("datetime")
    if not isinstance(dt_raw, str) or not dt_raw.strip():
        raise CalendarEngineError("calendar-basis.solar.datetime is required when ChartInput is omitted")
    normalized = dt_raw.strip().replace("Z", "+00:00")
    try:
        instant = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise CalendarEngineError(f"invalid calendar-basis.solar.datetime: {dt_raw!r}") from exc
    if instant.tzinfo is None:
        instant = instant.replace(tzinfo=ZoneInfo(tz_name))
    return instant


def _true_solar(inp: ChartInput) -> tuple[datetime, bool, float]:
    tst_enabled = False
    tst_delta = 0.0
    effective_dt = inp.local_dt
    if inp.longitude is not None:
        try:
            effective_dt, tst_delta = apply_true_solar_time(inp.local_dt, inp.longitude)
            tst_enabled = True
        except ValueError:
            pass
    return effective_dt, tst_enabled, tst_delta


def compute_chart_with_lunar(inp: ChartInput) -> Dict[str, Any]:
    """Convert civil time via mystilink-lunar, then assemble the Zi Wei chart."""
    _require_lunar()
    from mystilink_lunar import LunarCalendar

    if inp.local_dt.tzinfo is None:
        raise CalendarEngineError("ChartInput.local_dt must be timezone-aware for lunar engine")
    tz_name = str(inp.local_dt.tzinfo)
    # ZoneInfo str may be the key; prefer key if available
    key = getattr(inp.local_dt.tzinfo, "key", None)
    if isinstance(key, str) and key:
        tz_name = key

    cal = LunarCalendar.from_solar(
        inp.local_dt.year,
        inp.local_dt.month,
        inp.local_dt.day,
        inp.local_dt.hour,
        inp.local_dt.minute,
        timezone=tz_name,
    )
    basis = cal.to_dict()
    basis["schema_version"] = "mystilink.calendar_basis/0.1"
    if "provider" in basis and isinstance(basis["provider"], str):
        if not str(basis["provider"]).startswith("mystilink-lunar"):
            basis["provider"] = f"mystilink-lunar@{basis['provider']}"

    lunar = basis.get("lunar")
    if not isinstance(lunar, dict):
        raise CalendarEngineError("mystilink-lunar convert result missing lunar block")
    leap = bool(lunar.get("is_leap_month") or lunar.get("leap_month"))
    effective_dt, tst_enabled, tst_delta = _true_solar(inp)
    return _assemble_chart_from_lunar(
        inp,
        lunar_year=int(lunar["year"]),
        lunar_month=int(lunar["month"]),
        lunar_day=int(lunar["day"]),
        leap=leap,
        solar_used_for_lunar=inp.local_dt,
        effective_dt=effective_dt,
        tst_enabled=tst_enabled,
        tst_delta=tst_delta,
        calendar_engine="lunar",
        calendar_basis=_basis_subset(basis),
    )


def compute_chart_from_calendar_basis(
    basis: Dict[str, Any],
    *,
    inp: Optional[ChartInput] = None,
) -> Dict[str, Any]:
    """
    Build a Zi Wei chart from external calendar-basis / lunar convert JSON.

    Does not import mystilink-lunar. Requires basis['lunar'] with year/month/day.
    Gender and chart options come from ``inp`` when provided; otherwise gender
    defaults to male and other options use ChartInput defaults.
    """
    if not isinstance(basis, dict):
        raise CalendarEngineError("calendar-basis must be a JSON object")

    lunar = basis.get("lunar")
    if not isinstance(lunar, dict):
        raise CalendarEngineError("calendar-basis.lunar with year/month/day is required")
    for key in ("year", "month", "day"):
        if key not in lunar:
            raise CalendarEngineError(f"calendar-basis.lunar.{key} is required")

    local_dt = _parse_local_from_basis(basis, inp)
    if inp is None:
        chart_inp = ChartInput(
            local_dt=local_dt,
            midnight_zi="same-day",
            gender="male",
            include_si_hua=False,
            target_year=None,
            longitude=None,
        )
    else:
        chart_inp = inp

    leap = bool(lunar.get("is_leap_month") or lunar.get("leap_month"))
    effective_dt, tst_enabled, tst_delta = _true_solar(chart_inp)
    return _assemble_chart_from_lunar(
        chart_inp,
        lunar_year=int(lunar["year"]),
        lunar_month=int(lunar["month"]),
        lunar_day=int(lunar["day"]),
        leap=leap,
        solar_used_for_lunar=local_dt,
        effective_dt=effective_dt,
        tst_enabled=tst_enabled,
        tst_delta=tst_delta,
        calendar_engine="external_basis",
        calendar_basis=_basis_subset(basis),
    )
