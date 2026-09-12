"""Python binding re-export of the installable package API.

Prefer: `pip install -e .` then `import mystilink_ziwei`.

This module also offers a CLI-spawn helper for parity with other language bindings.
"""

from __future__ import annotations

import json
import os
import subprocess
from typing import Any

# Re-export core API when installed / on PYTHONPATH from repo root
try:
    from mystilink_ziwei import (  # noqa: F401
        ChartInput,
        __version__,
        compute_chart,
        parse_local_datetime,
        print_chart,
    )
except ImportError:  # pragma: no cover
    ChartInput = None  # type: ignore
    compute_chart = None  # type: ignore
    parse_local_datetime = None  # type: ignore
    print_chart = None  # type: ignore
    __version__ = "0.1.0"


def _cli() -> str:
    return os.environ.get("MYSTILINK_ZIWEI_CLI") or "mystilink-ziwei"


def chart_via_cli(
    datetime: str,
    timezone: str,
    gender: str,
    *,
    midnight_zi: str = "same-day",
    si_hua: bool = False,
    year: int | None = None,
    longitude: float | None = None,
) -> dict[str, Any]:
    """Spawn mystilink-ziwei chart and return parsed JSON."""
    argv = [
        _cli(),
        "chart",
        "--datetime",
        datetime,
        "--timezone",
        timezone,
        "--gender",
        gender,
        "--midnight-zi",
        midnight_zi,
    ]
    if si_hua:
        argv.append("--si-hua")
    if year is not None:
        argv.extend(["--year", str(year)])
    if longitude is not None:
        argv.extend(["--longitude", str(longitude)])
    proc = subprocess.run(argv, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or f"exit {proc.returncode}")
    return json.loads(proc.stdout)


def version_via_cli() -> dict[str, Any]:
    proc = subprocess.run([_cli(), "version"], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or f"exit {proc.returncode}")
    return json.loads(proc.stdout)
