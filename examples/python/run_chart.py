#!/usr/bin/env python3
"""Minimal Python example (fictional datetime)."""

from mystilink_ziwei import ChartInput, compute_chart, parse_local_datetime

local_dt = parse_local_datetime("1990-05-15 14:30", "Asia/Shanghai")
chart = compute_chart(
    ChartInput(
        local_dt=local_dt,
        midnight_zi="same-day",
        gender="male",
        include_si_hua=True,
        target_year=2026,
        longitude=121.5,
    )
)
print(f"ming={chart['ming_gong_branch']} frame={chart['five_element_frame']}")
print(f"ziwei={chart['ziwei_branch']} palaces={len(chart['palaces'])}")
