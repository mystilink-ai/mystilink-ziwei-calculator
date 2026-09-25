# -*- coding: utf-8 -*-
"""BirthProfile and schema_version tests for Zi Wei calculator."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mystilink_ziwei.birth import parse_birth_profile
from mystilink_ziwei.chart import ChartInput, compute_chart, parse_local_datetime

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "mystilink_ziwei", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def test_parse_birth_profile_fixture() -> None:
    data = json.loads((FIXTURES / "birth.profile.v0.json").read_text(encoding="utf-8"))
    fields = parse_birth_profile(data)
    assert fields.datetime_str == "1990-05-15 14:30"
    assert fields.timezone == "Asia/Shanghai"
    assert fields.gender == "male"
    assert fields.longitude == 121.47


def test_compute_chart_has_schema_version() -> None:
    local = parse_local_datetime("1990-05-15 14:30", "Asia/Shanghai")
    out = compute_chart(
        ChartInput(
            local_dt=local,
            midnight_zi="same-day",
            gender="male",
            include_si_hua=False,
        )
    )
    assert out["schema_version"] == "mystilink.ziwei.chart/0.1"
    assert out["ming_gong_branch"]
    assert len(out["palaces"]) == 12


def test_cli_legacy_chart() -> None:
    proc = _run(
        "chart",
        "--datetime",
        "1990-05-15 14:30",
        "--timezone",
        "Asia/Shanghai",
        "--gender",
        "male",
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["schema_version"] == "mystilink.ziwei.chart/0.1"


def test_cli_birth_json() -> None:
    path = FIXTURES / "birth.profile.v0.json"
    proc = _run("chart", "--birth-json", str(path))
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["schema_version"] == "mystilink.ziwei.chart/0.1"
    assert data["gender"] == "male"


def test_cli_version() -> None:
    proc = _run("version")
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["version"] == "0.2.3"
    assert data.get("cli") == "ziwei"
