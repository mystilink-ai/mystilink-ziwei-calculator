"""Command-line interface for MystiLink Zi Wei calculator.

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
from .chart import ChartInput, compute_chart, parse_local_datetime


def _emit_json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def cmd_chart(args: argparse.Namespace) -> int:
    try:
        local_dt = parse_local_datetime(args.datetime, args.timezone)
    except Exception as exc:
        print(json.dumps({"error": f"invalid datetime/timezone: {exc}"}, ensure_ascii=False), file=sys.stderr)
        return 2

    if args.gender not in ("male", "female"):
        print(json.dumps({"error": "gender must be male or female"}, ensure_ascii=False), file=sys.stderr)
        return 2

    chart = compute_chart(
        ChartInput(
            local_dt=local_dt,
            midnight_zi=args.midnight_zi,
            gender=args.gender,
            include_si_hua=bool(args.si_hua),
            target_year=args.year,
            longitude=args.longitude,
        )
    )
    _emit_json(chart)
    return 0


def cmd_version(_: argparse.Namespace) -> int:
    _emit_json({"name": "mystilink-ziwei-calculator", "version": __version__})
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="mystilink-ziwei",
        description="Zi Wei Dou Shu chart calculator (JSON CLI)",
    )
    sub = p.add_subparsers(dest="command", required=True)

    chart = sub.add_parser("chart", help="Compute a Zi Wei chart")
    chart.add_argument("--datetime", required=True, help='Local time "YYYY-MM-DD HH:MM"')
    chart.add_argument("--timezone", required=True, help="IANA timezone, e.g. Asia/Shanghai")
    chart.add_argument("--gender", required=True, choices=["male", "female"], help="Gender")
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
