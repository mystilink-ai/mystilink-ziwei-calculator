# -*- coding: utf-8 -*-
"""Validate ziwei chart against shared mystilink-metaphysics-schema when present."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from mystilink_ziwei.chart import ChartInput, compute_chart

SCHEMA_ROOT = (
    Path(__file__).resolve().parents[2] / "mystilink-metaphysics-schema" / "schemas" / "v0"
)


def _shared_available() -> bool:
    return (SCHEMA_ROOT / "systems" / "ziwei.chart.schema.json").is_file()


@pytest.mark.skipif(not _shared_available(), reason="sibling mystilink-metaphysics-schema not present")
def test_compute_chart_validates_shared_schema() -> None:
    pytest.importorskip("jsonschema")
    pytest.importorskip("referencing")
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012

    registry = Registry()
    for path in SCHEMA_ROOT.rglob("*.schema.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        registry = registry.with_resource(
            data["$id"],
            Resource.from_contents(data, default_specification=DRAFT202012),
        )
    schema = json.loads(
        (SCHEMA_ROOT / "systems" / "ziwei.chart.schema.json").read_text(encoding="utf-8")
    )
    inp = ChartInput(
        local_dt=datetime(1990, 5, 15, 14, 30, tzinfo=ZoneInfo("Asia/Shanghai")),
        gender="male",
        midnight_zi="same-day",
        include_si_hua=False,
    )
    out = compute_chart(inp)
    Draft202012Validator(schema, registry=registry).validate(out)
