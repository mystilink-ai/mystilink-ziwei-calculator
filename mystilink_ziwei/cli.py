"""Command-line interface for Mystilink Zi Wei calculator.

Subcommands:
  chart    Compute a San He Zi Wei chart; print JSON to stdout
  version  Print package version as JSON
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from . import __version__
from .birth import BirthProfileError, load_json_arg, parse_birth_profile
from .chart import ChartInput, compute_chart, parse_local_datetime


def _emit_json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _emit_error(message: str, code: int = 2) -> int:
    print(json.dumps({"error": message}, ensure_ascii=False), file=sys.stderr)
    return code


def cmd_chart(args: argparse.Namespace) -> int:
    datetime_str = args.datetime
    timezone = args.timezone
    gender = args.gender
    longitude = args.longitude

    if args.birth_json:
        try:
            profile = parse_birth_profile(load_json_arg(args.birth_json))
        except (BirthProfileError, OSError) as exc:
            return _emit_error(str(exc))
        datetime_str = profile.datetime_str
        if timezone is None:
            timezone = profile.timezone
        if gender is None:
            gender = profile.gender
        if longitude is None:
            longitude = profile.longitude

    if not datetime_str or not timezone:
        return _emit_error("either --datetime/--timezone/--gender or --birth-json is required")
    if gender not in ("male", "female"):
        return _emit_error("gender must be male or female (set via --gender or BirthProfile)")

    try:
        local_dt = parse_local_datetime(datetime_str, timezone)
    except Exception as exc:
        return _emit_error(f"invalid datetime/timezone: {exc}")

    chart = compute_chart(
        ChartInput(
            local_dt=local_dt,
            midnight_zi=args.midnight_zi,
            gender=gender,
            include_si_hua=bool(args.si_hua),
            target_year=args.year,
            longitude=longitude,
        )
    )
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
        help='Local time "YYYY-MM-DD HH:MM" (required unless --birth-json)',
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
        help="Late-zi hour lunar day rule (default: same-day)",
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
