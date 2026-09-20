"""Command-line interface for Mystilink Zi Wei calculator.

Subcommands:
  chart    Compute a San He Zi Wei chart; print JSON to stdout
  version  Print package version as JSON
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from . import __version__
from .birth import BirthProfileError, load_json_arg, parse_birth_profile
from .calendar_engine import (
    CalendarEngineError,
    compute_chart_from_calendar_basis,
    compute_chart_with_lunar,
)
from .chart import ChartInput, compute_chart, parse_local_datetime
from .envelope import build_subject, structured_error, wrap_envelope


def _emit_json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _emit_error(message: str, code: int = 2, *, envelope: bool = False) -> int:
    if envelope:
        print(json.dumps(structured_error("error", message), ensure_ascii=False), file=sys.stderr)
    else:
        print(json.dumps({"error": message}, ensure_ascii=False), file=sys.stderr)
    return code


def _load_basis(raw: str) -> Dict[str, Any]:
    if raw == "-":
        text = sys.stdin.read()
    else:
        path = Path(raw)
        if path.is_file():
            text = path.read_text(encoding="utf-8")
        else:
            text = raw
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("calendar-basis JSON root must be an object")
    return data


def cmd_chart(args: argparse.Namespace) -> int:
    datetime_str = args.datetime
    timezone = args.timezone
    gender = args.gender
    longitude = args.longitude
    birth_profile: Optional[Dict[str, Any]] = None
    use_envelope = bool(args.envelope)

    if args.birth_json:
        try:
            birth_profile = load_json_arg(args.birth_json)
            profile = parse_birth_profile(birth_profile)
        except (BirthProfileError, OSError, ValueError) as exc:
            return _emit_error(str(exc), envelope=use_envelope)
        datetime_str = profile.datetime_str
        if timezone is None:
            timezone = profile.timezone
        if gender is None:
            gender = profile.gender
        if longitude is None:
            longitude = profile.longitude

    engine = args.calendar_engine or "builtin"
    if args.calendar_basis:
        engine = "external_basis"

    local_dt = None
    if datetime_str and timezone:
        try:
            local_dt = parse_local_datetime(datetime_str, timezone)
        except Exception as exc:
            return _emit_error(f"invalid datetime/timezone: {exc}", envelope=use_envelope)

    try:
        if engine == "external_basis":
            if not args.calendar_basis:
                return _emit_error(
                    "calendar_engine=external_basis requires --calendar-basis JSON",
                    envelope=use_envelope,
                )
            if gender not in ("male", "female"):
                return _emit_error(
                    "gender must be male or female (set via --gender or BirthProfile)",
                    envelope=use_envelope,
                )
            basis = _load_basis(args.calendar_basis)
            from .calendar_engine import _parse_local_from_basis

            resolved_dt = local_dt if local_dt is not None else _parse_local_from_basis(basis, None)
            chart = compute_chart_from_calendar_basis(
                basis,
                inp=ChartInput(
                    local_dt=resolved_dt,
                    midnight_zi=args.midnight_zi,
                    gender=gender,
                    include_si_hua=bool(args.si_hua),
                    target_year=args.year,
                    longitude=longitude,
                ),
            )
            local_dt = resolved_dt
        elif engine == "lunar":
            if local_dt is None or not timezone:
                return _emit_error(
                    "either --datetime/--timezone/--gender or --birth-json is required",
                    envelope=use_envelope,
                )
            if gender not in ("male", "female"):
                return _emit_error(
                    "gender must be male or female (set via --gender or BirthProfile)",
                    envelope=use_envelope,
                )
            chart = compute_chart_with_lunar(
                ChartInput(
                    local_dt=local_dt,
                    midnight_zi=args.midnight_zi,
                    gender=gender,
                    include_si_hua=bool(args.si_hua),
                    target_year=args.year,
                    longitude=longitude,
                )
            )
        elif engine == "builtin":
            if local_dt is None or not timezone:
                return _emit_error(
                    "either --datetime/--timezone/--gender or --birth-json is required",
                    envelope=use_envelope,
                )
            if gender not in ("male", "female"):
                return _emit_error(
                    "gender must be male or female (set via --gender or BirthProfile)",
                    envelope=use_envelope,
                )
            chart = compute_chart(
                ChartInput(
                    local_dt=local_dt,
                    midnight_zi=args.midnight_zi,
                    gender=gender,
                    include_si_hua=bool(args.si_hua),
                    target_year=args.year,
                    longitude=longitude,
                ),
                calendar_engine="builtin",
            )
        else:
            return _emit_error(f"unknown calendar_engine: {engine!r}", envelope=use_envelope)
    except (CalendarEngineError, ValueError, OSError, json.JSONDecodeError) as exc:
        return _emit_error(str(exc), envelope=use_envelope)

    if use_envelope:
        subject = build_subject(
            birth_profile=birth_profile,
            datetime_iso=local_dt.isoformat() if local_dt is not None else chart.get("solar_local"),
            timezone_name=timezone,
            gender=gender,
            longitude=longitude,
        )
        payload = wrap_envelope(
            system="ziwei",
            chart=chart,
            subject=subject,
            calendar_basis=chart.get("calendar_basis"),
            locale=args.locale,
            produced_by=f"mystilink-ziwei-calculator@{__version__}",
        )
        _emit_json(payload)
    else:
        _emit_json(chart)
    return 0


def cmd_version(_: argparse.Namespace) -> int:
    _emit_json({"name": "mystilink-ziwei-calculator", "version": __version__, "cli": "ziwei"})
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ziwei",
        description="Zi Wei Dou Shu chart calculator (JSON CLI)",
    )
    sub = p.add_subparsers(dest="command", required=True)

    chart = sub.add_parser("chart", help="Compute a Zi Wei chart")
    chart.add_argument(
        "--datetime",
        required=False,
        default=None,
        help='Local time "YYYY-MM-DD HH:MM" (required unless --birth-json / --calendar-basis)',
    )
    chart.add_argument(
        "--timezone",
        required=False,
        default=None,
        help="IANA timezone, e.g. Asia/Shanghai (required unless --birth-json)",
    )
    chart.add_argument(
        "--gender",
        required=False,
        default=None,
        choices=["male", "female"],
        help="Gender (required unless BirthProfile provides it)",
    )
    chart.add_argument(
        "--midnight-zi",
        choices=["same-day", "next-day"],
        default="same-day",
        help="Late-zi hour lunar day rule (default: same-day; builtin only)",
    )
    chart.add_argument("--si-hua", action="store_true", help="Include birth-year si-hua with palace")
    chart.add_argument("--year", type=int, default=None, help="Annual fortune target year (Gregorian)")
    chart.add_argument(
        "--longitude",
        type=float,
        default=None,
        help="Birth longitude in degrees (east positive); enables true solar time",
    )
    chart.add_argument(
        "--birth-json",
        type=str,
        default=None,
        help=(
            "BirthProfile JSON (mystilink.birth/0.1): file path, '-' for stdin, "
            "or inline JSON"
        ),
    )
    chart.add_argument(
        "--calendar-engine",
        type=str,
        default="builtin",
        choices=["builtin", "lunar", "external_basis"],
        help="Lunar source: builtin zhdate (default), lunar extra, or external_basis",
    )
    chart.add_argument(
        "--calendar-basis",
        type=str,
        default=None,
        help="External calendar-basis / lunar convert JSON (file, '-', or inline)",
    )
    chart.add_argument(
        "--envelope",
        action="store_true",
        help="Wrap chart as mystilink.envelope/0.1 (default: bare chart JSON)",
    )
    chart.add_argument("--locale", type=str, default=None, help="BCP 47 locale for envelope")
    chart.set_defaults(func=cmd_chart)

    ver = sub.add_parser("version", help="Print version JSON")
    ver.set_defaults(func=cmd_version)

    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    code = args.func(args)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
