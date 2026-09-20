# Changelog

## 0.2.2

- Optional `[lunar]` extra (`mystilink-lunar>=0.1.0a3`, Python 3.10+)
- CLI `--calendar-engine builtin|lunar|external_basis` (default `builtin` / zhdate)
- CLI `--calendar-basis` and optional `--envelope` / `--locale`
- Output always includes `calendar_engine`; lunar/external may embed `calendar_basis`
- Python binding defaults to short CLI `ziwei` with long-name fallback

## 0.2.1

- Primary CLI entry point is `ziwei`; alias `mystilink-ziwei` remains installed
- Bindings default to spawning `ziwei` (override with `MYSTILINK_ZIWEI_CLI`)


## 0.2.1

- Primary CLI command is now `ziwei` (long alias `mystilink-ziwei` still installed)
- Bindings default to resolving `ziwei` on `PATH`

## 0.2.0

- Chart JSON includes `schema_version` (`mystilink.ziwei.chart/0.1`)
- CLI `chart` accepts optional `--birth-json` (mystilink.birth/0.1 BirthProfile)
- Legacy `--datetime` / `--timezone` / `--gender` remain supported

## 0.1.0

- Initial San He Zi Wei chart JSON CLI
