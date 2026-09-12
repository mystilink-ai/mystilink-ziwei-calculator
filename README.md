# Mystilink Zi Wei Calculator

> Languages: [English](README.md) | [简体中文](README.zh-CN.md)

## Overview

Computes a San He style Zi Wei Dou Shu (Purple Star) natal chart from a local civil datetime, timezone, and gender. Output covers fourteen major stars, auxiliary stars, twelve gods, decade ranges (大限), optional annual fortune (流年), four pillars, and optional si-hua with palace attribution. Results are emitted as JSON.

## Platforms and languages

| Target | Delivery |
|--------|----------|
| Python | Installable package `mystilink-ziwei-calculator` and CLI `mystilink-ziwei` |
| C | Header + library that runs the CLI and returns JSON |
| C++ | Thin wrapper over the C API |
| C# | Process wrapper around the CLI |
| Java | ProcessBuilder wrapper around the CLI |
| JavaScript / Node | Same npm package; Node spawns CLI by default; browser injects a `runCli` function |

Contract for non-Python bindings: invoke the `mystilink-ziwei` executable (or path from env `MYSTILINK_ZIWEI_CLI`) and parse JSON on stdout.

## Requirements

- Python 3.9+
- Dependency: `zhdate` (declared in `pyproject.toml`)

## Install

```bash
cd mystilink-ziwei-calculator
python3 -m pip install -e .
```

Verify:

```bash
mystilink-ziwei version
```

## CLI

Always prints JSON to stdout on success.

### Chart

```bash
mystilink-ziwei chart \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --gender male \
  --midnight-zi same-day \
  --si-hua \
  --year 2026 \
  --longitude 121.5
```

| Flag | Required | Description |
|------|----------|-------------|
| `--datetime` | yes | Local civil time `YYYY-MM-DD HH:MM` |
| `--timezone` | yes | IANA timezone name |
| `--gender` | yes | `male` or `female` |
| `--midnight-zi` | no | `same-day` (default) or `next-day` for late 子时 lunar day rule |
| `--si-hua` | no | Include birth-year si-hua with palace |
| `--year` | no | Gregorian year for annual fortune labels |
| `--longitude` | no | East-positive degrees; enables true solar time correction |

### Version

```bash
mystilink-ziwei version
```

Also: `python -m mystilink_ziwei …`

## Python API

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from mystilink_ziwei import ChartInput, compute_chart

chart = compute_chart(
    ChartInput(
        local_dt=datetime(1990, 5, 15, 14, 30, tzinfo=ZoneInfo("Asia/Shanghai")),
        midnight_zi="same-day",
        gender="male",
        include_si_hua=True,
        target_year=2026,
        longitude=121.5,
    )
)
```

## Examples

Minimal runnable samples live under `examples/`:

- `examples/python/`
- `examples/node/`
- `examples/js/`
- `examples/c/`
- `examples/cpp/`
- `examples/csharp/`
- `examples/java/`

All examples use fictional datetimes only.

## Schema

JSON Schema drafts for CLI input/output shapes are under `schema/`.

## Bindings

Source under `bindings/{c,cpp,csharp,java,js,python}/`. Set `MYSTILINK_ZIWEI_CLI` if the executable is not on `PATH`.

## License

MIT. See [LICENSE](LICENSE).
