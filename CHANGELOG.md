# Changelog

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
