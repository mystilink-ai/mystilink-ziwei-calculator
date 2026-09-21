# Mystilink 紫微斗數排盤

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概述

根據本地民用日期時間、時區與性別，計算三合派紫微斗數本命盤。結果包含十四主星、輔星、十二神、大限區間、可選流年、四柱，以及可選的生年干四化（含落宮）。輸出為 JSON。

## 平台與語言

| 目標 | 交付 |
|------|------|
| Python | 可安裝套件 `mystilink-ziwei-calculator` 與 CLI `ziwei` |
| C | 標頭檔 + 執行 CLI 並回傳 JSON 的函式庫 |
| C++ | 對 C API 的薄封裝 |
| C# | 呼叫 CLI 的行程封裝 |
| Java | ProcessBuilder 封裝 |
| JavaScript / Node | 同一 npm 套件；Node 預設 spawn CLI；瀏覽器注入 `runCli` 函式 |

非 Python 綁定的契約：呼叫可執行檔 `ziwei`（或環境變數 `MYSTILINK_ZIWEI_CLI` 指定路徑），解析標準輸出中的 JSON。別名 `mystilink-ziwei` 仍會安裝。

## 環境需求

- Python 3.9+
- 相依性：`zhdate`（寫在 `pyproject.toml`）

## 安裝

```bash
cd mystilink-ziwei-calculator
python3 -m pip install -e .
# optional lunar engine (Python 3.10+)
python3 -m pip install -e '.[lunar]'
```

驗證：

```bash
ziwei version
```

## CLI

成功時始終向標準輸出列印 JSON。

### Chart

```bash
ziwei chart \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --gender male \
  --midnight-zi same-day \
  --si-hua \
  --year 2026 \
  --longitude 121.5

ziwei chart --birth-json tests/fixtures/birth.profile.v0.json
```

| 旗標 | 必填 | 說明 |
|------|------|------|
| `--datetime` | 除非 `--birth-json` | 本地民用時間 `YYYY-MM-DD HH:MM` |
| `--timezone` | 除非 `--birth-json` | IANA 時區名稱 |
| `--gender` | 除非 BirthProfile | `male` 或 `female` |
| `--birth-json` | 否 | BirthProfile（`mystilink.birth/0.1`）：檔案、`-` 或內嵌 JSON |
| `--midnight-zi` | 否 | 晚子時換日規則：`same-day`（預設）或 `next-day` |
| `--si-hua` | 否 | 包含生年干四化及落宮 |
| `--year` | 否 | 流年公曆年份標籤 |
| `--longitude` | 否 | 東經為正的度數；啟用真太陽時修正 |
| `--calendar-engine` | 否 | `builtin`（zhdate，預設）、`lunar`（可選 extra）或 `external_basis` |
| `--calendar-basis` | 否 | 外部 calendar-basis / lunar convert JSON（檔案、`-` 或內嵌） |
| `--envelope` | 否 | 包裝為 `mystilink.envelope/0.1`（預設：裸盤） |
| `--locale` | 否 | 信封的 BCP 47 語系 |

盤面 JSON 含 `schema_version`：`mystilink.ziwei.chart/0.1` 與 `calendar_engine`。
lunar/external 引擎可能內嵌 `calendar_basis`。

### Version

```bash
ziwei version
```

亦可：`python -m mystilink_ziwei …`

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

## 範例

最小可執行範例位於 `examples/`：

- `examples/python/`
- `examples/node/`
- `examples/js/`
- `examples/c/`
- `examples/cpp/`
- `examples/csharp/`
- `examples/java/`

所有範例僅使用虛構日期時間。

## Schema

CLI 輸入/輸出形狀的 JSON Schema 草稿位於 `schema/`。

## 綁定

原始碼位於 `bindings/{c,cpp,csharp,java,js,python}/`。若可執行檔不在 `PATH`，請設定 `MYSTILINK_ZIWEI_CLI`。

## 授權

MIT。見 [LICENSE](../../LICENSE)。
