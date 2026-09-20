"""Tests for optional Zi Wei calendar engines."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from datetime import datetime
from zoneinfo import ZoneInfo

from mystilink_ziwei.calendar_engine import (
    CalendarEngineError,
    compute_chart_from_calendar_basis,
    compute_chart_with_lunar,
    lunar_available,
)
from mystilink_ziwei.chart import ChartInput, compute_chart

FIXTURES = Path(__file__).parent / "fixtures"


def _inp() -> ChartInput:
    return ChartInput(
        local_dt=datetime(1990, 5, 15, 12, 0, tzinfo=ZoneInfo("Asia/Shanghai")),
        midnight_zi="same-day",
        gender="male",
        include_si_hua=False,
    )


def test_builtin_has_calendar_engine() -> None:
    out = compute_chart(_inp())
    assert out["calendar_engine"] == "builtin"
    assert "calendar_basis" not in out
    assert out["schema_version"] == "mystilink.ziwei.chart/0.1"


def test_external_basis_lunar() -> None:
    basis = json.loads((FIXTURES / "calendar.basis.v0.json").read_text(encoding="utf-8"))
    out = compute_chart_from_calendar_basis(basis, inp=_inp())
    assert out["calendar_engine"] == "external_basis"
    assert out["lunar"]["year"] == 1990
    assert out["lunar"]["month"] == 4
    assert out["lunar"]["day"] == 21
    assert out["calendar_basis"]["schema_version"] == "mystilink.calendar_basis/0.1"


def test_external_basis_missing_lunar() -> None:
    with pytest.raises(CalendarEngineError, match="lunar"):
        compute_chart_from_calendar_basis(
            {
                "schema_version": "mystilink.calendar_basis/0.1",
                "solar": {
                    "datetime": "1990-05-15T12:00:00+08:00",
                    "timezone": "Asia/Shanghai",
                },
            },
            inp=_inp(),
        )


@pytest.mark.skipif(not lunar_available(), reason="mystilink-lunar not installed")
def test_lunar_engine_runs() -> None:
    out = compute_chart_with_lunar(_inp())
    assert out["calendar_engine"] == "lunar"
    assert "calendar_basis" in out
    assert out["lunar"]["year"] >= 1989
